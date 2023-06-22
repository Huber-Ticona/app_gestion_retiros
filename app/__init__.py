from flask import Flask
from dotenv import load_dotenv


def create_app():

    # SE CARGAN LAS VARIABLES DE ENTORNO
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # CARGA INSTANCIA CONFIGURACION
    if app.config['ENV'] == 'development':
        app.config.from_object('instance.config.ConfigDevelop')
    else:
        app.config.from_object('instance.config.ConfigProduction')

    from .main import main_bp
    from .auth.auth import auth_bp
    # Registrar Blueprint
    app.register_blueprint(main_bp, url_prefix='')
    app.register_blueprint(auth_bp, url_prefix='')

    return app
