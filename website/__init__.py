from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#Defines database where everything is sent to 
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    #creates this app
    app = Flask(__name__)
    #configures app with a secret key
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    #creates the database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #initializes the app with the database
    db.init_app(app)

    from .views import views
    from .auth import auth
    #registers blueprint so we can be like 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #This is where the user is sent if they are not logged in. Just redirects
    login_manager.init_app(app) #Tells login_manager which app we are using

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')