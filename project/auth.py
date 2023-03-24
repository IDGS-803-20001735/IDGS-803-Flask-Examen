from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from . models import User
from . import db, userDataStore
import logging
import datetime

auth = Blueprint('auth', __name__, url_prefix = '/security')

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods = ['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    fecha_actual = datetime.datetime.now()

    user = User.query.filter_by(email = email).first()

    if not user or not check_password_hash(user.password, password):
      flash('El usuario y/o la contraseña son incorrectos')
      
      logging.basicConfig(filename = 'app.log', level = logging.ERROR)
      logging.error('INICIO DE SESION ERRONEO PARA: %s, CONTRASENIA: %s, EL DIA: %s', email, password,fecha_actual)

      return redirect(url_for('auth.login'))
    
    logging.basicConfig(filename = 'app.log', level = logging.INFO)
    logging.info(
        'INICIO DE SESION CORRECTO PARA: %s, CONTRASENIA: %s, EL DIA: %s', email, password,fecha_actual
        )

    login_user(user, remember = remember)
    return redirect(url_for('main.profile'))

@auth.route('/register')
def register():
    return render_template('/security/register.html')

@auth.route('/register', methods = ['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    fecha_actual = datetime.datetime.now()

    user = User.query.filter_by(email = email).first()

    if user:
        flash('El correo electrónico ya existe')
        
        logging.basicConfig(filename = 'app.log', level = logging.ERROR)
        logging.error(
            'REGISTRO ERRONEO PARA: %s, CONTRASENIA: %s, EL DIA: %s', email, password,fecha_actual
            )

        return redirect(url_for('auth.register'))
    
    logging.basicConfig(filename = 'app.log', level = logging.INFO)
    logging.info(
        'REGISTRO CORRECTO PARA: %s, CONTRASENIA: %s, EL DIA: %s', email, password,fecha_actual
        )

    userDataStore.create_user(
        name = name, email = email, password = generate_password_hash(password, method = 'sha256')
    )

    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
