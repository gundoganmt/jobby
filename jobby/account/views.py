from flask import render_template, request, Blueprint, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from jobby.models import Users, Notification
from datetime import datetime
from jobby import db, login_manager, mail
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message

account = Blueprint('account',__name__)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@account.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('public.index'))
            else:
                flash('Email veya şifre yanlış')
                return render_template('pages-login.html')
        else:
            flash('Email veya şifre yanlış')
            return render_template('pages-login.html')
    return render_template('pages-login.html')

def send_confirmation_email(user):
    token = user.get_confirmation_token()
    msg = Message('Email doğrulama linki',
        sender="mahmut@jobby.net",
        recipients=[user.email])
    msg.body = f"""Mail adresinizi doğrulamak için lutfen aşağıdaki linke tıklayın.
    {url_for('account.confirm_email', token=token, _external=True)}
    Eğer bu mail size yanlışlıkla geldiyse herhangi birşey yapmanıza gerek yoktur.
    """
    mail.send(msg)

@account.route('/confirm_email/<token>')
def confirm_email(token):
    user = Users.verify_confirmation_token(token)
    user.email_approved = True
    db.session.commit()
    flash("Email adresiniz doğrulandı", "info")
    return redirect(url_for('public.index'))

@account.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    if request.method == 'POST':
        name = request.form['name'].lower()
        surname = request.form['surname'].lower()
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        hashed_password = generate_password_hash(password, method='sha256')
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user is None:
            user = Users(name=name, surname=surname, email=email, password=hashed_password,
                member_since=datetime.utcnow())
            notif = Notification(notification_to=user, not_type=2)
            db.session.add(user)
            db.session.add(notif)
            db.session.commit()
            login_user(user)
            #send_confirmation_email(user)
            return render_template('email_confirmation_notification.html')
        flash('Email adresi kullanılıyor')
        return render_template('pages-register.html')
    return render_template('pages-register.html')

@account.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))
