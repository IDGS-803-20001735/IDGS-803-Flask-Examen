from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . models import Manga
from . import db
import logging
import datetime

main = Blueprint('main',__name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/profile')
@login_required
def profile():
  try:
    mangas = Manga.query.all()
  except Exception as exception:
    flash('ERROR AL TRAER LOS REGISTROS DE LA BD' + str(exception), 'error')
  return render_template('profile.html', name = current_user.name, mangas = mangas)

@main.route('/admin')
@login_required
@roles_required('admin')
def admin():
  try:
     mangas = Manga.query.all()
  except Exception as exception:
    flash('ERROR AL TRAER LOS REGISTROS DE LA BD' + str(exception), 'error')
  return render_template('admin.html', mangas = mangas)

@main.route('/insertManga', methods = ['GET', 'POST'])
@login_required
@roles_required('admin')
def insert_manga():
    try:
        if request.method == 'POST':
            manga = Manga(
                name = request.form.get('nombre'),
                author = request.form.get('autor'),
                tomo = request.form.get('tomo'),
                price = request.form.get('precio'),
                exist = request.form.get('estatus'),
                image = request.form.get('cover')
            )

            db.session.add(manga)
            db.session.commit()
            flash("EL VOLUMEN NO. {} DEL MANGA {} SE AGREGÓ SATISFACTORIAMENTE!".format(manga.tomo, manga.name), 'warning')
            return redirect(url_for('main.admin'))
    except Exception as exception:
        flash('NO FUE POSIBLE INSERTAR UN NUEVO MANGA A LA BD: ' + str(exception), 'error')
    return render_template('insert_manga.html')

@main.route('/updateManga', methods = ['GET', 'POST'])
@login_required
@roles_required('admin')
def update_manga():
   try:
    if request.method == 'GET':
      id = request.args.get('id')
      manga = db.session.query(Manga).filter(Manga.id == id).first()

      nombre = manga.name
      autor = manga.author
      tomo =  manga.tomo
      precio = manga.price
      estatus = manga.exist
      imagen = manga.image

      return render_template('update_manga.html', id = id, nombre = nombre, autor = autor, tomo = tomo, precio = precio, estatus = estatus, imagen = imagen)
    
    if request.method == 'POST':
      id = request.form.get('id')
      manga = db.session.query(Manga).filter(Manga.id == id).first()

      manga.name = request.form.get('nombre')
      manga.author = request.form.get('autor')
      manga.tomo = request.form.get('tomo')
      manga.price = request.form.get('precio')
      manga.exist = request.form.get('estatus')
    
      imagen = request.form.get('cover')
      manga.image = imagen

      db.session.add(manga)
      db.session.commit()

      flash("EL VOLUMEN NO. {} DEL MANGA {} SE ACTUALIZÓ SATISFACTORIAMENTE!".format(manga.tomo, manga.name), 'warning')
      return redirect(url_for('main.admin'))
   except Exception as exception:
    flash('NO FUE POSIBLE ACTUALIZAR EL MANGA: ' + str(exception), 'error')
    return render_template('update_manga.html')

@main.route('/deleteManga', methods = ['GET'])
@login_required
@roles_required('admin')
def delete_manga():
   try:
      id = request.args.get('id')
      manga = db.session.query(Manga).filter(Manga.id == id).first()

      db.session.delete(manga)
      db.session.commit()
      flash("EL MANGA SE ELIMINÓ SATISFACTORIAMENTE!", 'warning')
   except Exception as exception:
      flash('NO FUE POSIBLE ELIMINAR EL MANGA DE LA BD: ' + str(exception), 'error')
   return redirect(url_for('main.admin'))

@main.route('/selectManga', methods = ['GET', 'POST'])
@login_required
def select_manga():
   try:
      if request.method == 'GET':
         mangas = db.session.query(Manga).all()
         return render_template('profile.html', mangas = mangas, name = current_user.name)

      elif request.method == 'POST':
         nombre = request.form.get('nombre')
         
         if nombre:
            manga = db.session.query(Manga).filter(Manga.name == nombre).all()
         else:
            manga = db.session.query(Manga).all()

         return render_template('profile.html', mangas = manga, name = current_user.name)

   except Exception as exception:
      flash('NO FUE POSIBLE SELECCIONAR EL MANGA: ' + str(exception), 'error')
      return render_template('profile.html', name = current_user.name)
