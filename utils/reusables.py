def success_response(msg=None):
    data = {"status": "success",
            "message": msg}
    return data


def failure_response(msg=None):
    data = {"status": "failed",
            "message": msg}
    return data
