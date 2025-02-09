from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
from os import getenv, path, mkdir
from datetime import timedelta
import logging


# SET UP LOGGING
logging.basicConfig(
    filename='error_log.txt',  # Specify the log file name
    level=logging.ERROR,        # Set the logging level to ERROR
    format='%(asctime)s - %(levelname)s - %(message)s',  # Customize the log format
)

# Load .env-file
load_dotenv()



# Create Flask-Application
def create_app():
    app = Flask(__name__)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    
    if not path.exists("./sessions"):
        mkdir("./sessions")
    app.config['SESSION_FILE_DIR'] = './sessions'
    
    app.permanent_session_lifetime = timedelta(minutes=5000)
    
    Session(app)
    
    return app