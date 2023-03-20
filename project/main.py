from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . models import Manga
from . import db

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
    mangas = Manga.query.all()
    return render_template('profile.html', name = current_user.name, mangas = mangas)

@main.route('/admin')
@login_required
@roles_required('admin')
def admin():
    mangas = Manga.query.all()
    return render_template('admin.html', mangas = mangas)

@main.route('/insertManga', methods = ['GET', 'POST'])
@login_required
@roles_required('admin')
def insert_manga():
  if request.method == 'POST':
    manga = Manga (
        name = request.form.get('nombre'),
        author = request.form.get('autor'),
        tomo = request.form.get('tomo'),
        price = request.form.get('precio'),
        exist = request.form.get('estatus')
    )
            
    db.session.add(manga)
    db.session.commit()
    flash("Manga agregado satisfactoriamente")
    return redirect(url_for('main.admin'))
  return render_template('insert_manga.html')

@main.route('/updateManga', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def update_manga():
    if request.method == 'GET':
        id = request.args.get('id')
        manga = db.session.query(Manga).filter(Manga.id == id).first()

        nombre = request.form.get('nombre', manga.name)
        autor = request.form.get('autor', manga.author)
        tomo = request.form.get('tomo', manga.tomo)
        precio = request.form.get('precio', manga.price)
        estatus = request.form.get('estatus', manga.exist)
        return render_template('update_manga.html', id = id, nombre = nombre, autor = autor, tomo = tomo, precio = precio, estatus = estatus)
    
    if request.method == 'POST':
        id = request.form.get('id')
        manga = db.session.query(Manga).filter(Manga.id == id).first()

        manga.name = request.form.get('nombre')
        manga.author = request.form.get('autor')
        manga.tomo = request.form.get('tomo')
        manga.price = request.form.get('precio')
        manga.exist = request.form.get('estatus')

        db.session.add(manga)
        db.session.commit()
        flash("Manga actualizado satisfactoriamente")
        return redirect(url_for('main.admin'))
    return render_template('update_manga.html')

@main.route('/deleteManga', methods = ['GET'])
@login_required
@roles_required('admin')
def delete_manga():
   id = request.args.get('id')
   alumno = db.session.query(Manga).filter(Manga.id == id).first()

   db.session.delete(alumno)
   db.session.commit()
   flash("Manga eliminado satisfactoriamente")
   return redirect(url_for('main.admin'))