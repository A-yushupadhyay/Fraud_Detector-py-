import pandas as pd
from django.shortcuts import render, redirect
from .models import Transaction
from .ml_model import predict_fraud_scores
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail  # ✅ Email support
from django.utils.timezone import now
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import csv
from django.http import HttpResponse
from datetime import datetime  # gives you datetime directly

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Count
import pandas as pd
from django.utils.timezone import now
import json
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404
from .models import Transaction
from django.http import HttpResponseRedirect
from django.urls import reverse






def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def upload_transactions(request):
    if request.method == "POST":
        csv_file = request.FILES["file"]
        df = pd.read_csv(csv_file)

        # Predict fraud score for each row
        fraud_scores = predict_fraud_scores(df)
        df['fraud_probability'] = fraud_scores
        print("LEN DF:", len(df))
        print("LEN FRAUD SCORES:", len(fraud_scores))  # <-- This is most likely the mismatch

        high_risk_count = 0

        for _, row in df.iterrows():
            Transaction.objects.create(
                user=request.user,  # ✅ link transaction to user
                customer_id=row['customer_id'],
                order_id=row['order_id'],
                amount=row['amount'],
                payment_method=row['payment_method'],
                timestamp=row['timestamp'],
                device=row['device'],
                location=row['location'],
                fraud_probability=row['fraud_probability']
            )
            if row['fraud_probability'] > 0.8:
                high_risk_count += 1

        # ✅ Send alert if high-risk transactions are found
        if high_risk_count > 0:
            send_mail(
                subject='🚨 Fraud Alert: High-Risk Transactions Detected',
                message=f'{high_risk_count} high-risk transaction(s) were detected during upload.',
                from_email='your_email@gmail.com',          # ✅ Change to your email
                recipient_list=['your_email@gmail.com'],    # ✅ Add actual recipients (admin, analyst, etc.)
                fail_silently=False
            )

        return redirect('view_transactions')

    return render(request, "fraudml/upload.html")

@login_required
@user_passes_test(is_admin)
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')  # ✅ FIXED
    # Calculate risk levels
    high = transactions.filter(fraud_probability__gt=0.8).count()
    low = transactions.filter(fraud_probability__lte=0.5).count()
    total = transactions.count()
    medium = total - high - low

    context = {
        'transactions': transactions,
        'fraud_chart': json.dumps({
            'High Risk': high,
            'Medium Risk': medium,
            'Low Risk': low
      })
 }
    return render(request, 'fraudml/view.html', context)






@login_required
@user_passes_test(is_admin)
def dashboard_view(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)

    total_orders = transactions.count()
    high_fraud_count = transactions.filter(fraud_probability__gt=0.8).count()
    last_upload = transactions.latest('timestamp').timestamp if transactions.exists() else "No uploads yet"

    suspicious_locations_qs = (
        transactions
        .filter(fraud_probability__gt=0.8)
        .values_list('location', flat=True)
    )
    suspicious_locations = list(set(suspicious_locations_qs))[:5]

    top_fraud_devices = (
        transactions
        .filter(fraud_probability__gt=0.8)
        .values('device')
        .annotate(count=Count('device'))
        .order_by('-count')[:5]
    )

    avg_amount = transactions.aggregate(avg=Avg('amount')).get('avg') or 0

    last_7_days = transactions.filter(
        fraud_probability__gt=0.8,
        timestamp__date__gte=now().date() - pd.Timedelta(days=6)
    ).annotate(
        date=TruncDate('timestamp')
    ).values('date').annotate(count=Count('id')).order_by('date')

    date_map = {entry['date'].strftime('%d %b'): entry['count'] for entry in last_7_days}
    all_dates = [(now().date() - pd.Timedelta(days=i)).strftime('%d %b') for i in range(6, -1, -1)]
    fraud_labels = all_dates
    fraud_data = [date_map.get(date, 0) for date in all_dates]

    fraud_by_customer = (
        transactions
        .values('customer_id')
        .annotate(avg_fraud=Avg('fraud_probability'))
        .order_by('-avg_fraud')[:10]
    )
    fraud_customers = [entry['customer_id'] for entry in fraud_by_customer]
    fraud_scores = [round(entry['avg_fraud'], 2) for entry in fraud_by_customer]
    suspicious_users = (
        Transaction.objects
        .filter(fraud_probability__gt=0.8)
        .values('customer_id')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    context = {
        'total_orders': total_orders,
        'high_fraud_count': high_fraud_count,
        'last_upload_time': last_upload.strftime('%d %b %Y, %I:%M %p') if isinstance(last_upload, datetime) else last_upload,
        'suspicious_locations': suspicious_locations,
        'top_fraud_devices': top_fraud_devices,
        'avg_amount': avg_amount,
        'transactions': transactions[:20],
        'fraud_labels': json.dumps(fraud_labels),
        'fraud_data': json.dumps(fraud_data),
        'fraud_customers': json.dumps(fraud_customers),
        'fraud_scores': json.dumps(fraud_scores),
        'suspicious_users': suspicious_users,
    }

    return render(request, 'fraudml/dashboard.html', context)



@login_required
@user_passes_test(is_admin)
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        file = request.FILES['csv_file']
        try:
            df = pd.read_csv(file)

            # Clean column names (strip extra spaces)
            df.columns = df.columns.str.strip()

            # Ensure required columns exist
            required_columns = {'order_id', 'customer_id', 'amount', 'payment_method', 'timestamp', 'device', 'location'}
            if not required_columns.issubset(df.columns):
                messages.error(request, f"Missing required columns in CSV. Found: {list(df.columns)}")
                return render(request, 'fraudml/upload.html')

        except Exception as e:
            messages.error(request, f"Invalid CSV file: {e}")
            return render(request, 'fraudml/upload.html')

        # ✅ Run fraud prediction model
        try:
            fraud_scores = predict_fraud_scores(df)
            df['fraud_probability'] = fraud_scores
        except Exception as e:
            messages.error(request, f"Prediction failed: {e}")
            return render(request, 'fraudml/upload.html')

        # ✅ Save transactions to DB
        try:
            for _, row in df.iterrows():
                fraud_score = float(row['fraud_probability'])

                # Handle timestamp if in string format
                timestamp = row['timestamp']
                if isinstance(timestamp, str):
                    try:
                        timestamp = pd.to_datetime(timestamp)
                    except Exception as e:
                        messages.error(request, f"Invalid timestamp format: {timestamp}")
                        return render(request, 'fraudml/upload.html')

                txn = Transaction.objects.create(
                    user=request.user,
                    order_id=row['order_id'],
                    customer_id=row['customer_id'],
                    amount=row['amount'],
                    payment_method=row['payment_method'],
                    timestamp=timestamp,
                    device=row['device'],
                    location=row['location'],
                    fraud_probability=fraud_score
                )

                # 🚨 Trigger alert if fraud is very likely
                if fraud_score > 0.90:
                    send_fraud_alert_email(txn)

        except Exception as e:
            messages.error(request, f"Database save failed: {e}")
            return render(request, 'fraudml/upload.html')

        # ✅ Upload successful
        messages.success(request, f'File "{file.name}" uploaded successfully! {len(df)} records processed.')
        return redirect('dashboard')  # 🛠️ Redirect to dashboard instead of transactions

    return render(request, 'fraudml/upload.html')





@login_required
@user_passes_test(is_admin)
def send_fraud_alert_email(txn):
    print(f"🚨 Triggering fraud alert email for order: {txn.order_id}, probability: {txn.fraud_probability:.4f}")

    subject = f"🚨 High Fraud Alert - Order #{txn.order_id}"
    html_message = render_to_string('fraudml/email_alert.html', {'txn': txn})
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        'puskaru202@gmail.com',
        ['puskaru202@gmail.com'],
        html_message=html_message,
    )

    print(f"✅ Fraud alert email sent for order #{txn.order_id}!")


@login_required
@user_passes_test(is_admin)
def download_csv(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')  # ✅ FIXED

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fraud_transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer ID', 'Amount', 'Timestamp', 'Fraud Probability'])

    for txn in transactions:
        writer.writerow([
            txn.order_id,
            txn.customer_id,
            txn.amount,
            txn.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            f"{txn.fraud_probability:.2f}"
        ])

    return response




@login_required
@user_passes_test(is_admin)
def reports_view(request):
    # dummy view or real logic
    return render(request, 'fraudml/reports.html')



@login_required
@user_passes_test(is_admin)
def settings_view(request):
    return render(request, 'fraudml/settings.html')


@login_required
@user_passes_test(is_admin)
def transaction_detail_view(request, txn_id):
    txn = get_object_or_404(Transaction, id=txn_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        txn.is_fraud = True if action == 'fraud' else False
        txn.reviewed_by = request.user
        txn.save()
        messages.success(request, "Transaction updated successfully.")
        return redirect('view_transactions')
    return render(request, 'fraudml/transaction_detail.html', {'txn': txn})



@login_required
@user_passes_test(is_admin)
def mark_as_fraud(request, txn_id):
    txn = get_object_or_404(Transaction, id=txn_id, user=request.user)
    txn.is_fraud = True
    txn.save()
    return HttpResponseRedirect(reverse('view_transactions'))

@login_required
@user_passes_test(is_admin)
def mark_as_not_fraud(request, txn_id):
    txn = get_object_or_404(Transaction, id=txn_id, user=request.user)
    txn.is_fraud = False
    txn.save()
    return HttpResponseRedirect(reverse('view_transactions'))



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


