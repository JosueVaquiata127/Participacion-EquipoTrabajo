# Librerias a usar en el modulo
from flask import request,render_template,redirect,url_for,Blueprint
from flask_login import login_required

# Referencia a la base de datos
from blueprintapp.app import db
# Modelos con los que interactura el modulo
from blueprintapp.miembros.models import Miembro

bp_miembro = Blueprint('bp_miembro',__name__,template_folder='templates')

@bp_miembro.route("/")
@login_required
def index():
    miembros = Miembro.query.all()
    return render_template('miembro/index.html',miembros=miembros)

@bp_miembro.route("/create",methods=['GET','POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('miembro/create.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        # Crear un objeto miembro
        miembro = Miembro(nombre=nombre,email=email)
        # Insertar en la bd a traves del ORM
        db.session.add(miembro)
        db.session.commit()
        # Redireccion al listado de miembros
        return redirect(url_for('bp_miembro.index'))
        
# Nueva ruta: Editar miembro
@bp_miembro.route("/editar/<int:id>", methods=['GET','POST'])
@login_required
def editar(id):
    miembro = Miembro.query.get_or_404(id)
    if request.method == 'POST':
        miembro.nombre = request.form.get('nombre')
        miembro.email = request.form.get('email')
        db.session.commit()
        return redirect(url_for('bp_miembro.index'))
    return render_template('miembro/editar.html', miembro=miembro)

# Nueva ruta: Eliminar miembro
@bp_miembro.route("/eliminar/<int:id>", methods=['POST'])
@login_required
def eliminar(id):
    miembro = Miembro.query.get_or_404(id)
    db.session.delete(miembro)
    db.session.commit()
    return redirect(url_for('bp_miembro.index'))   