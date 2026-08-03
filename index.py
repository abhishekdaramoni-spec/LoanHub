import os
import traceback

app = None
error_trace = None

try:
    from app import create_app
    app = create_app()
except Exception as e:
    error_trace = traceback.format_exc()
    print("CRITICAL ERROR during app factory creation:")
    print(error_trace)
    
    # Fallback Flask app to render the traceback directly in the browser for diagnostics
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def fallback_error(path):
        return f"""
        <html>
            <head><title>App Initialization Failed</title></head>
            <body style="font-family: monospace; padding: 30px; background-color: #F7FAFC; color: #2D3748;">
                <h1 style="color: #E53E3E;">App Factory Initialization Failed</h1>
                <p>The Flask application failed to start. Review the stack trace below:</p>
                <hr/>
                <pre style="background-color: #EDF2F7; padding: 20px; border-radius: 8px; border: 1px solid #CBD5E0; overflow-x: auto;">{error_trace}</pre>
            </body>
        </html>
        """, 500

if __name__ == '__main__':
    # Ensure static upload directory exists
    if app and not error_trace:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        from app import db
        with app.app_context():
            try:
                db.create_all()
                print("Database tables initialized successfully.")
            except Exception as e:
                print(f"Warning: Database creation skipped or failed: {e}")
                
        app.run(host='0.0.0.0', port=5000, debug=True)
    elif error_trace:
        app.run(host='0.0.0.0', port=5000, debug=True)
