from django.urls import path
from .views import dashboard_view, upload_csv, download_csv , view_transactions

from django.conf.urls import handler404  # 👈 required for custom error handling

from . import views

urlpatterns = [
    path("upload/", views.upload_transactions, name="upload_transactions"),
    path('fraud/dashboard/', dashboard_view, name='dashboard'),
    path('fraud/view/', view_transactions, name='view_transactions'),
    path('fraud/upload/', upload_csv, name='upload_csv'),
    path('fraud/download/', download_csv, name='download_csv'),
    path('reports/', views.reports_view, name='reports'),        # already added
    path('settings/', views.settings_view, name='settings'),     # ✅ add this
    path('transactions/<int:txn_id>/', views.transaction_detail_view, name='transaction_detail'),

    # ✅ new routes
    path('transactions/<int:txn_id>/mark-fraud/', views.mark_as_fraud, name='mark_as_fraud'),
    path('transactions/<int:txn_id>/mark-not-fraud/', views.mark_as_not_fraud, name='mark_as_not_fraud'),
]


# 👇 This must be outside the urlpatterns list
handler404 = 'backend.views.custom_404_view'