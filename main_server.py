import imp
from flask import Flask, request
from avoid_circular_import import cyber_database
import database_tables
from update_database import fetch_endpoints, update_endpoints

cyber_intruder = Flask(__name__)
cyber_intruder.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
cyber_intruder.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
cyber_database.init_app(cyber_intruder)
cyber_intruder.app_context().push()
cyber_database.create_all()

@cyber_intruder.route("/endpoints", methods=["GET", "PUT"])
def end_points():
    if request.method == "GET":
        return fetch_endpoints()

    elif request.method == "PUT":
        hostname = request.args.get("Endpoint_Name")
        if not hostname:
            return "must provide hostname on PUT", 400

        host = request.get_json()
        update_endpoints(host)
        return {}, 204
