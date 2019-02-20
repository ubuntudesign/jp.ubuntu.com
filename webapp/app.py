"""
A Flask application for jp.ubuntu.com
"""

import flask
import talisker.flask
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.debug import DebuggedApplication
from werkzeug.routing import BaseConverter
from canonicalwebteam.blog.app import BlogExtension

from webapp.blueprint import jp_website
from webapp.handlers import set_handlers


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = flask.Flask(
    __name__, template_folder="../templates", static_folder="../static"
)


app.url_map.strict_slashes = False
app.url_map.converters["regex"] = RegexConverter

app.wsgi_app = ProxyFix(app.wsgi_app)
if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

talisker.flask.register(app)

set_handlers(app)
app.register_blueprint(jp_website)

blog = BlogExtension()
blog.init_app(app, "Ubuntu blog", [3184], "lang:jp", "/blog")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
