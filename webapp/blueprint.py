import flask


def jp_website_blueprint():
    """
    Return a blueprint for all routes of the main jp.ubuntu.com website
    """
    jp_website = flask.Blueprint(
        "jp_website",
        __name__,
        template_folder="/templates",
        static_folder="/static",
    )

    @jp_website.route("/")
    def homepage():
        status_code = 200

        return flask.render_template("index.html"), status_code

    @jp_website.route("/openstack")
    def openstack():
        status_code = 200

        return flask.render_template("openstack.html"), status_code

    @jp_website.route("/iot")
    def iot():
        status_code = 200

        return flask.render_template("iot.html"), status_code

    @jp_website.route("/ai-ml")
    def ai_ml():
        status_code = 200

        return flask.render_template("ai-ml.html"), status_code

    @jp_website.route("/kubernetes")
    def k8s():
        status_code = 200

        return flask.render_template("kubernetes.html"), status_code

    @jp_website.route("/enterprise-support")
    def enterprise_support():
        status_code = 200

        return (
            flask.render_template("enterprise-support/index.html"),
            status_code,
        )

    @jp_website.route("/enterprise-support/plans-and-pricing")
    def enterprise_support_plans():
        status_code = 200

        return (
            flask.render_template("enterprise-support/plans-and-pricing.html"),
            status_code,
        )

    @jp_website.route("/download")
    def download():
        status_code = 200

        return (flask.render_template("download.html"), status_code)

    @jp_website.route("/contact-us")
    def contact_us():
        status_code = 200

        return (flask.render_template("contact-us.html"), status_code)

    @jp_website.route("/thank-you")
    def thank_you():
        status_code = 200

        return (flask.render_template("thank-you.html"), status_code)

    @jp_website.route("/favicon.ico")
    def favicon():
        return flask.redirect(
            "https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto/https://assets.ubuntu.com/v1/088fd1bf-favicon.ico"  # noqa: E501
        )

    @jp_website.route("/robots.txt")
    def robots():
        return flask.Response("", mimetype="text/plain")

    @jp_website.route("/_status/check")
    def check():
        return "OK"

    return jp_website
