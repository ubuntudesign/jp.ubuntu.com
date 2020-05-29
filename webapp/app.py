"""
A Flask application for jp.ubuntu.com
"""

# Packages
import yaml
from canonicalwebteam.blog import BlogViews
from canonicalwebteam.blog.flask import build_blueprint
from canonicalwebteam.flask_base.app import FlaskBase

from webapp.blueprint import jp_website
import webapp.template_utils as template_utils


app = FlaskBase(
    __name__,
    "jp.ubuntu.com",
    template_folder="../templates",
    static_folder="../static",
)

app.register_blueprint(jp_website)
blog_views = BlogViews(blog_title="Ubuntu blog", tag_ids=[3184])
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
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0")
