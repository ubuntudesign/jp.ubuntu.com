"""
A Flask application for jp.ubuntu.com
"""

# Packages
import yaml
import flask
import talisker
import webapp.template_utils as template_utils

from canonicalwebteam.blog import build_blueprint, BlogViews, BlogAPI
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder

session = talisker.requests.get_session()
app = FlaskBase(
    __name__,
    "jp.ubuntu.com",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)

blog_views = BlogViews(
    api=BlogAPI(
        session=session,
        api_url="https://ubuntu.com/blog/wp-json/wp/v2",
        thumbnail_width=354,
        thumbnail_height=180,
    ),
    blog_title="Ubuntu blog",
    tag_ids=[3184],
    per_page=11,
)
app.register_blueprint(build_blueprint(blog_views), url_prefix="/blog")

# read releases.yaml
with open("releases.yaml") as releases:
    releases = yaml.load(releases, Loader=yaml.FullLoader)


# Template context
@app.context_processor
def context():
    return {
        "format_date": template_utils.format_date,
        "get_json_feed": template_utils.get_json_feed_content,
        "replace_admin": template_utils.replace_admin,
        "truncate_chars": template_utils.truncate_chars,
        "releases": releases,
        "platform": flask.request.args.get("platform", ""),
        "version": flask.request.args.get("version", ""),
        "architecture": flask.request.args.get("architecture", ""),
    }


@app.route("/favicon.ico")
def favicon():
    return flask.redirect(
        "https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto/"
        "https://assets.ubuntu.com/v1/088fd1bf-favicon.ico"
    )


@app.route("/robots.txt")
def robots():
    return flask.Response("", mimetype="text/plain")


# All other routes
template_finder_view = TemplateFinder.as_view("template_finder")
template_finder_view._exclude_xframe_options_header = True
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
