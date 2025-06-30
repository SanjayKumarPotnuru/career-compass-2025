# 💼 Career Compass 2025

Career Compass is a smart web application that helps Computer Science Engineering (CSE) students discover suitable job roles based on their **expected salary** and **desired job rating**. It uses machine learning models to recommend the **top 4 best-matching CSE job roles**, with detailed information for each.

---

## 🚀 Features

- 🔐 User Login & Registration
- 💸 Input expected salary & rating to get job suggestions
- 🎯 ML-powered prediction using ensemble models (RandomForest, XGBoost, GradientBoost)
- 📚 Detailed job info: description, qualifications, future scope, location-based salary, and companies offering that job
- 🌐 Clean and responsive web UI (HTML/CSS/Flask)

---

## 📊 Machine Learning Model

- Used `VotingClassifier` ensemble of:
  - `RandomForestClassifier`
  - `GradientBoostingClassifier`
  - `XGBoostClassifier`
- Trained on cleaned dataset with fields like:
  - Job Title
  - Salary
  - Company Rating
  - Employment Type
- Output: Top 4 most relevant **core job roles**

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, Jinja (Flask templating)
- **Backend**: Python + Flask
- **Machine Learning**: scikit-learn, xgboost, pandas
- **Database**: SQLite
- **APIs/Storage**: Alpha Vantage (used earlier), Alpha, Quandl (deprecated), GitHub for deployment

---

## 📁 Folder Structure
Career-Compass/
│
├── static/ # CSS, JS, images
├── templates/ # HTML files (home, dashboard, job details)
├── ml_model/ # Trained model (pkl)
├── data/ # Raw & cleaned CSV datasets
├── app.py # Flask app
├── train_model.py # ML model training script
├── job_info.json # Info for each job role
├── requirements.txt # Required Python libraries
└── README.md


---

## 🧪 Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/SanjayKumarPotnuru/career-compass-2025.git
   cd career-compass-2025

2.Create a virtual environment
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

3.Install requirements
pip install -r requirements.txt

4.Run The App
python app.py

