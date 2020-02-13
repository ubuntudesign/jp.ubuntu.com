"""
A Flask application for jp.ubuntu.com
"""

# Packages
import flask
import talisker.flask
import talisker.logs
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.debug import DebuggedApplication
from werkzeug.routing import BaseConverter
from canonicalwebteam.blog import BlogViews
from canonicalwebteam.blog.flask import build_blueprint
from canonicalwebteam.yaml_responses.flask_helpers import prepare_redirects
import yaml

# Local
from webapp.blueprint import jp_website
from webapp.handlers import set_handlers


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = flask.Flask(
    __name__, template_folder="../templates", static_folder="../static"
)

app.before_request(prepare_redirects())

app.url_map.strict_slashes = False
app.url_map.converters["regex"] = RegexConverter

app.wsgi_app = ProxyFix(app.wsgi_app)
if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

talisker.flask.register(app)
talisker.logs.set_global_extra({"service": "jp.ubuntu.com"})

set_handlers(app)
app.register_blueprint(jp_website)

blog_views = BlogViews(blog_title="Ubuntu blog", tag_ids=[3184])
app.register_blueprint(build_blueprint(blog_views), url_prefix="/blog")

if __name__ == "__main__":
    app.run(host="0.0.0.0")

# read releases.yaml
with open("releases.yaml") as releases:
    releases = yaml.load(releases, Loader=yaml.FullLoader)

# Template context
@app.context_processor
def context():
    return {
        "releases": releases,
    }
