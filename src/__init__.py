import os
from . import auth, db, dashboard
from flask import Flask


def create_app(test_config=None):
    """
    Application Factory to create and configure app instance
    :param test_config:
    :return:
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'src.sqlite'),
    )

    if test_config is None:
        # Load the instance configuration, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register application context
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')
    db.init_app(app)

    # A simple index page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
