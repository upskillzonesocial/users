from app.email_constants import SENDER_EMAIL
from flask import jsonify


def success_response(msg=None, receivers=None,
                     status_code=200):
    data = {"status": "success",
            "message": msg,

            "email": f"Users {receivers}  has been created by {SENDER_EMAIL}"}
    return jsonify(data), status_code


def failure_response(msg=None, status_code=500):
    data = {"status": "failed",
            "message": msg}
    return jsonify(data), status_code
