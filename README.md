# 💼 Fraud Detector using Django + Machine Learning

An end-to-end **Fraud Detection System** built with **Django**, integrated with a trained **ML model** to analyze transaction data and identify suspicious activities. This project is deployable on Render and designed for production-ready workflows.

---


🌍 Live Demo
🔗 Live Site: fraud-detector-py.onrender.com


![Screenshot (300)](https://github.com/user-attachments/assets/f81bd386-9cc5-4786-839a-b7ec661d9b3b)


![Screenshot (301)](https://github.com/user-attachments/assets/9330cf94-1c5e-4506-ad32-518631dd21f7)





![Screenshot (302)](https://github.com/user-attachments/assets/f2af35fb-b323-42a3-9435-a7593f0cacb6)



![Screenshot (303)](https://github.com/user-attachments/assets/84f6fbb4-9de6-4aa3-b47e-8590aa01270f)






![Screenshot (304)](https://github.com/user-attachments/assets/60c85d89-c93b-4ddb-9b18-035a08d1a293)



![Screenshot (305)](https://github.com/user-attachments/assets/5db79076-50f3-456a-9d05-9cd87da22d22)


![Screenshot (306)](https://github.com/user-attachments/assets/34c80979-cfde-4d5b-92ea-77cfde835709)

![Screenshot (307)](https://github.com/user-attachments/assets/d8187a78-60ae-4053-8edb-b5f1e17060ff)


![Screenshot (308)](https://github.com/user-attachments/assets/bf58e0ac-cdae-4fd1-ba31-f1065af4f818)



## 🚀 Features

- 🧠 ML-Powered Fraud Score Prediction
- 📄 Upload & Analyze Transaction CSVs
- 📥 Download Scored Transactions
- 🔐 User Registration, Login & Logout
- 🛡️ Role-based Views (Admin/User)
- 🌐 Deployed on Render
- 🎯 Clean UI with Routing & Error Handling

---

## 🛠️ Tech Stack

| Category      | Tools Used                             |
|---------------|-----------------------------------------|
| Backend       | Python, Django                         |
| Frontend      | HTML, CSS (Django Templates)           |
| ML Model      | `scikit-learn`, `joblib`               |
| Data Handling | Pandas, CSV                            |
| Deployment    | Render.com                             |
| Server        | Gunicorn (WSGI)                        |
| Python Env    | Python 3.13 in `.venv`                 |
| DataBase      |  PostgreSQL                            |
---

## 📁 Project Structure


fraud_detector/
│
├── backend/
│ ├── settings.py
│ ├── urls.py ← Redirects '/' to '/users/register/'
│ └── wsgi.py
│
├── fraudml/
│ ├── views.py
│ ├── urls.py
│ ├── ml_model.py ← Loads trained model.pkl
│ ├── templates/
│ └── fraud_model/
│ └── model.pkl ← Trained ML model file (joblib)
│
├── users/
│ ├── views.py
│ ├── urls.py ← Handles login/register/logout
│ └── templates/
│
├── templates/
│ └── base.html, etc.
│
├── static/
│ └── css/, js/
│
├── manage.py
├── requirements.txt
└── README.md


Create and activate virtual environment

bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Run migrations

bash
python manage.py makemigrations
python manage.py migrate
Run the server

bash
python manage.py runserver
Visit: http://127.0.0.1:8000/
👉 Redirects to: http://127.0.0.1:8000/users/register/

🧠 Machine Learning Model
Trained on a public dataset of transaction frauds

Features include transaction amount, location, device ID, etc.

Binary classification model (Fraud / Not Fraud)

Deployed with joblib and loaded in Django view

📤 CSV Upload Format
transaction_id	amount	location	device_id	...
100001	542.00	NY	D12345	...

Accepts .csv file

Auto-calculates fraud scores

Option to download predictions

📦 Deployment Notes (Render)
Uses gunicorn backend.wsgi:application

model.pkl should not be in .gitignore

App detects port dynamically on Render

render.yaml or manual setup supports environment binding


🤝 Contributing
Fork this repo

Create a branch: git checkout -b feature-name

Commit your changes: git commit -m "add feature"

Push to your branch: git push origin feature-name

Open a PR!

🙌 Acknowledgements
Built with 💙 using Django & ML

Special thanks to mentors, friends, and OpenAI for technical guidance

-------------------------------
👨‍💻 Author
Ayush Upadhyay
Email - puskaru202@gmail.com


-------------------------------




