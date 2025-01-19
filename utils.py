from flask import request

def isEmpty(items: list[str]) -> bool:
    for item in items:
        if item == "":
            return True
    
    return False


def get_request_params(*args: str) -> dict:
    retValue = {}
    for arg in args:
        retValue[arg] = request.form.get(arg, "")
    
    return retValue
