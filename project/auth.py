from flask import Blueprint, render_template, url_for,flash, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        
        if password == password2:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('User already exist!', 'info')
                return redirect(url_for('auth.register'))
            else:
                new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('You have entered wrong credentials')
            return redirect(url_for('auth.login'))
        else:
            login_user(user, remember= remember)
            return redirect(url_for('main.profile'))
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))