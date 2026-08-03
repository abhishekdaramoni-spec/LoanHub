import os
from flask import Flask, render_template
from app.config import Config
from app.extensions import db, login_manager, mail, csrf
from app.models import User
from app.routes import auth_bp, main_bp, admin_bp

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'templates'),
                static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static'))
    
    app.config.from_object(config_class)

    # Test MySQL connection validity, fallback to SQLite if connection fails
    uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if uri and uri.startswith('mysql'):
        from sqlalchemy import create_engine
        try:
            engine = create_engine(uri)
            conn = engine.connect()
            conn.close()
            print("Connected to MySQL database successfully.")
        except Exception as e:
            print(f"MySQL connection failed ({e}). Falling back to local SQLite database.")
            if os.environ.get('VERCEL'):
                db_path = '/tmp/loansphere.db'
                if not os.path.exists(db_path):
                    import shutil
                    src_db = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'database', 'loansphere.db')
                    if os.path.exists(src_db):
                        try:
                            shutil.copy(src_db, db_path)
                            print("Copied pre-seeded SQLite database to /tmp successfully.")
                        except Exception as copy_err:
                            print(f"Failed to copy pre-seeded database to /tmp: {copy_err}")
            else:
                db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'database', 'loansphere.db')
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    return app

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Retrieve user by primary key ID (Session loader)
    return User.query.get(int(user_id))
