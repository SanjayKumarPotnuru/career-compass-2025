from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from ml_model.job_predictor import predict_jobs
import json
import os
import re
from flask import flash  # optionally use flash for messages

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///careercompass.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# --------------------- ROUTES ---------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    salary = float(request.form['salary'])
    top_jobs = list(set(predict_jobs(salary)))[:4]
    return render_template('results.html', jobs=top_jobs)

@app.route('/about')
def about():
    return render_template('about.html')

USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_]{3,20}$')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        # ✅ Check for existing email
        if User.query.filter_by(email=email).first():
            return 'Email already registered'

        # ✅ Username format validation
        if not USERNAME_REGEX.fullmatch(username):
            return 'Username must be 3–20 characters long and contain only letters, numbers, or underscores.'

        # ✅ Create and save new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        salary = float(request.form['salary'])
        top_jobs = list(set(predict_jobs(salary)))
        return render_template('results.html', jobs=top_jobs)

    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/job/<job_name>')
def job_detail(job_name):
    # ✅ Load job info from correct path
    job_info_path = os.path.join("ml_model", "data", "job_info.json")

    with open(job_info_path, "r", encoding="utf-8") as f:
        job_info = json.load(f)

    info = job_info.get(job_name)
    if not info:
        return f"<h3>❌ Job data not found for '{job_name}'</h3><a href='/dashboard'>🔙 Back to Dashboard</a>"

    return render_template('job_detail.html', job=job_name, info=info)

# --------------------- MAIN ---------------------
if __name__ == '__main__':
    app.run(debug=True)
