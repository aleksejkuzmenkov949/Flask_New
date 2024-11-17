from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

users_bp = Blueprint('users', __name__)


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        # Создание нового пользователя
        new_user = User(username=data['username'])

        # Установим пароль
        new_user.set_password(data['password'])

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.login'))

    return render_template('register.html')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            login_user(user)
            return redirect(url_for('notes.notes_list'))

        flash('Неверные данные для входа!')

    return render_template('login.html')


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

