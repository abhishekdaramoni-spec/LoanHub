import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Ensure static upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize DB tables in app context if not exists
    with app.app_context():
        try:
            db.create_all()
            print("Database tables initialized successfully.")
        except Exception as e:
            print(f"Warning: Database creation skipped or failed: {e}")
            
    app.run(host='0.0.0.0', port=5000, debug=True)
