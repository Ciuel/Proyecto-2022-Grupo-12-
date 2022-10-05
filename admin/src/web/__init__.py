from flask import Flask, render_template
from src.web.config import get_config
import src.core.db as database
from src.web.controllers.discipline import discipline_blueprint
from src.web.controllers.associate import associate_blueprint
from src.web.controllers.configuration import configuration_blueprint
from src.web.controllers.api.configuration import configuration_api_blueprint
from src.web.controllers.user import user_blueprint
from src.web.helpers import handlers


def create_app(
    env="development", static_folder="/static", template_folder="templates"
):
    config = get_config()
    app = Flask(
        __name__, static_folder=static_folder, template_folder=template_folder
    )

    app.config.from_object(config[env])

    # Controllers
    app.register_blueprint(discipline_blueprint)
    app.register_blueprint(associate_blueprint)
    app.register_blueprint(configuration_blueprint)
    app.register_blueprint(user_blueprint)
    # Api
    app.register_blueprint(configuration_api_blueprint)

    with app.app_context():
        database.init_app(app)

    # Routes
    @app.get("/")
    def bar():
        return render_template("home.html")

    @app.get("/home")
    def home():
        return render_template("home.html")

    @app.get("/login")
    def login():
        return render_template("login.html")

    @app.get("/listado_socios")
    def associates_list():
        return render_template("associate_list.html")

    @app.get("/public_index")
    def public_home():
        return render_template("public_index.html")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        database.db.session.remove()

    @app.cli.command("resetdb")
    def resetdb():
        database.reset_db()

    app.register_error_handler(400, handlers.bad_request_error)
    app.register_error_handler(401, handlers.unauthorized_error)
    app.register_error_handler(403, handlers.forbidden_error)
    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)

    return app
