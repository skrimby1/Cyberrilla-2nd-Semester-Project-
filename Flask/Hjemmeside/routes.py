from flask import Blueprint, render_template, session, redirect, url_for

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    
    if 'user_email' not in session:
        if request.accept_mimetypes['application/json']:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        return redirect(url_for('auth.login'))

    return render_template('home.html')
