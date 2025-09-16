from flask import Flask, session, redirect, url_for, request

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Cyberrilla123'

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes)
    app.register_blueprint(auth)

    @app.before_request
    def require_login():
        exempt = (
            'auth.login',
            'auth.logout',
            'auth.register',
            'static',
            'auth.api_login',
            'auth.receive_data',
            'auth.send_data' #Ændret til at tillade API login uden login, ellers ville den redirect
        )
        # if you’re not logged in and not on login/logout/static, redirect
        if request.endpoint not in exempt and 'user_email' not in session:
            return redirect(url_for('auth.login'))

    return app