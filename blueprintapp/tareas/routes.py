# Librerias a usar en el modulo
from flask import request,render_template,redirect,url_for,Blueprint

# Referencia a la base de datos
from blueprintapp.app import db
# Modelos con los que interactura el modulo
from blueprintapp.tareas.models import Tarea

bp_tarea = Blueprint('bp_tarea',__name__,template_folder='templates')

@bp_tarea.route("/")
def index():
    tareas = Tarea.query.all()
    return render_template('tareas/index.html',tareas=tareas)

@bp_tarea.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('tareas/create.html')
    elif request.method == 'POST':
        descripcion = request.form.get('descripcion')
        completado = True if 'completado' in request.form.keys() else False
        # Crear un objeto miembro
        tarea = Tarea(descripcion=descripcion,completado=completado)
        # Insertar en la bd a traves del ORM
        db.session.add(tarea)
        db.session.commit()
        # Redireccion al listado de miembros
        return redirect(url_for('bp_tarea.index'))
        
#  Nueva ruta: Editar tarea
@bp_tarea.route("/editar/<int:id>", methods=['GET', 'POST'])
def editar(id):
    tarea = Tarea.query.get_or_404(id)
    if request.method == 'POST':
        tarea.descripcion = request.form.get('descripcion')
        tarea.completado = True if 'completado' in request.form.keys() else False
        db.session.commit()
        return redirect(url_for('bp_tarea.index'))
    return render_template('tareas/editar.html', tarea=tarea)

#  Nueva ruta: Eliminar tarea
@bp_tarea.route("/eliminar/<int:id>", methods=['POST'])
def eliminar(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for('bp_tarea.index'))