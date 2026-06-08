from flask import Flask
from blueprintapp.extensions import db,bcrypt,login_Manager
from flask_migrate import Migrate
from blueprintapp.models import User

migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = "mi-clave-super-secreta"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_equipo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_Manager.init_app(app)
    
    migrate.init_app(app,db)
    
    @login_Manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
       
    #1. Imnportacion del blueprint (para cada modulo)
    from blueprintapp.miembros.routes import bp_miembro
    from blueprintapp.core.routes import bp_core
    from blueprintapp.tareas.routes import bp_tarea
    from blueprintapp.main import main_bp
    from blueprintapp.auth import auth_bp   
    
    #2. Registro el blueprint (para cada modulo)
    app.register_blueprint(bp_miembro, url_prefix="/miembros")
    app.register_blueprint(bp_core, url_prefix="/")
    app.register_blueprint(bp_tarea, url_prefix="/tareas")
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    

    with app.app_context():
        db.create_all()    

    return app