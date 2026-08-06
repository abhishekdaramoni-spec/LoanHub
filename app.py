import os
from flask import Flask, render_template
from config import Config
from utils.extensions import db, login_manager, mail, csrf
from models import User
from routes import auth_bp, main_bp, admin_bp

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
                static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static'))
    
    app.config.from_object(config_class)

    # Normalize DATABASE_URL for PostgreSQL if set as postgres:// (Render/Heroku convention)
    uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri

    # Verify connection to remote MySQL/PostgreSQL, fallback to SQLite if connection fails
    if uri and not uri.startswith('sqlite'):
        from sqlalchemy import create_engine
        try:
            engine = create_engine(uri)
            conn = engine.connect()
            conn.close()
            print("Connected to database successfully.")
        except Exception as e:
            print(f"Remote connection check failed ({e}). Falling back to local SQLite database.")
            db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', 'loansphere.db')
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

# WSGI Application entry point for production servers
app = create_app()

# Serve static files efficiently in production using WhiteNoise
from whitenoise import WhiteNoise
app.wsgi_app = WhiteNoise(app.wsgi_app, root=app.static_folder, prefix=app.static_url_path + '/')

# Setup User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize directories, database tables, and default seed data on module load (Gunicorn safe)
with app.app_context():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    try:
        db.create_all()
        print("Database tables initialized successfully.")
        # Auto-seed basic data if tables are empty
        from utils.seeder import seed_default_data
        seed_default_data()
    except Exception as e:
        print(f"Warning: Database creation or seeding failed: {e}")

if __name__ == '__main__':
    # Run server on port read from environment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
