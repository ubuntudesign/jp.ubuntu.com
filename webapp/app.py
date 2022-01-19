"""
A Flask application for jp.ubuntu.com
"""

# Packages
import yaml
import flask
import talisker
import webapp.template_utils as template_utils

from canonicalwebteam.blog import build_blueprint, BlogViews, BlogAPI
from canonicalwebteam.discourse import DiscourseAPI, EngagePages, EngageParser
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from canonicalwebteam import image_template
from webapp.views import build_engage_index, engage_thank_you


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


# Engage pages and takeovers from Discourse
# This section needs to provide takeover data for /
discourse_api = DiscourseAPI(
    base_url="https://discourse.ubuntu.com/",
    session=session,
)

engage_path = "/engage"
engage_pages = EngagePages(
    parser=EngageParser(
        api=discourse_api,
        index_topic_id=21103,
        url_prefix=engage_path,
    ),
    document_template="engage/base.html",
    url_prefix=engage_path,
    blueprint_name="engage-pages",
)

app.add_url_rule(engage_path, view_func=build_engage_index(engage_pages))


def get_takeovers():
    takeovers = {}

    engage_pages.parser.parse()
    takeovers["sorted"] = sorted(
        engage_pages.parser.takeovers,
        key=lambda takeover: takeover["publish_date"],
        reverse=True,
    )
    takeovers["active"] = [
        takeover
        for takeover in engage_pages.parser.takeovers
        if takeover["active"] == "true"
    ]

    return takeovers


def takeovers_json():
    takeovers = get_takeovers()
    response = flask.jsonify(takeovers["active"])
    response.cache_control.max_age = "300"
    response.cache_control._set_cache_value(
        "stale-while-revalidate", "360", int
    )
    response.cache_control._set_cache_value("stale-if-error", "600", int)

    return response


def takeovers_index():
    takeovers = get_takeovers()

    return flask.render_template(
        "takeovers/index.html",
        takeovers=takeovers,
    )


app.add_url_rule("/takeovers.json", view_func=takeovers_json)
app.add_url_rule("/takeovers", view_func=takeovers_index)
engage_pages.init_app(app)

app.add_url_rule(
    "/engage/<page>/thank-you",
    view_func=engage_thank_you(engage_pages),
)


# read releases.yaml
with open("releases.yaml") as releases:
    releases = yaml.load(releases, Loader=yaml.FullLoader)


# Image template
@app.context_processor
def utility_processor():
    return {"image": image_template}


# Template context
@app.context_processor
def context():
    return {
        "format_date": template_utils.format_date,
        "get_json_feed": template_utils.get_json_feed_content,
        "replace_admin": template_utils.replace_admin,
        "truncate_chars": template_utils.truncate_chars,
        "page": flask.request.args.get("page", ""),
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
