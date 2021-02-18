import os

import nitrogen.boundary.web_server as web
from nitrogen.blueprints.assimilation import bp as assimilation_blueprint


def conf_api(app):
    """Configure open_api for a Sanic app
    Docs:
    https://sanic-openapi.readthedocs.io/en/stable/sanic_openapi/configurations.html
    """
    app.blueprint(web.swagger_blueprint)
    app.config["API_TITLE"] = "Nitrogen API"
    app.config["API_VERSION"] = "0.2.5"
    app.config[
        "API_DESCRIPTION"
    ] = "A Nitrogen API with an 'Assimilation' example application."
    app.config["API_LICENSE_NAME"] = "Mozilla Public License Version 2.0"
    app.config["API_LICENSE_URL"] = "https://www.mozilla.org/en-US/MPL/2.0/"
    app.config["API_CONTACT_EMAIL"] = "kamil@magnet.coop"


def create_app():
    app = web.App(__name__)
    conf_api(app)

    @app.route("/", methods=["GET"])
    @web.doc.summary("Simple health check")
    @web.doc.response(200, {"status": str}, description="It's alive!")
    async def healthcheck(request):
        return web.response.json({"status": "ok"})

    return app


def run():
    app = create_app()
    app.blueprint(assimilation_blueprint)
    app.run(host="0.0.0.0", port=os.environ["SERVER_PORT"], debug=True)
