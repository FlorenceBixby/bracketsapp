from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brackets.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Bracket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    items = db.Column(db.Text, nullable=False)
    is_private = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    brackets = Bracket.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', brackets=brackets)

@app.route('/create_bracket', methods=['GET', 'POST'])
def create_bracket():
    if request.method == 'POST':
        size = int(request.form['size'])
        items = request.form['items'].split(',')
        is_private = 'is_private' in request.form
        if 'random' in request.form:
            random.shuffle(items)
        new_bracket = Bracket(user_id=session['user_id'], size=size, items=','.join(items), is_private=is_private)
        db.session.add(new_bracket)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_bracket.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
