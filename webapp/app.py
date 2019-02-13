"""
A Flask application for jp.ubuntu.com
"""

import flask
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.debug import DebuggedApplication

from webapp.blueprint import jp_website_blueprint
from webapp.handlers import set_handlers


app = flask.Flask(
    __name__, template_folder="../templates", static_folder="../static"
)

app.url_map.strict_slashes = False

app.wsgi_app = ProxyFix(app.wsgi_app)
if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

set_handlers(app)
app.register_blueprint(jp_website_blueprint())

if __name__ == "__main__":
    app.run(host="0.0.0.0")
