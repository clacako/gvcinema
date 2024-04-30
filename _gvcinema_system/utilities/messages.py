from django.utils.html import strip_tags, mark_safe
from datetime import datetime

def message(code, messages, data=None, **kwargs):
    message_dict    = {}
    for key, value in messages.items():
        if "_" in list(key): key = key.replace("_", " ")
        message_dict[key.title()]   = value
    
    message = {
        "is_success"    : code,
        "message"       : message_dict,
        "data"          : data,
        **kwargs
    }
    
    return message

def server_error_message():
    return "whoops, something happened on your server"

def response(status, message, data=None, detail=None, **kwargs):
    response    = {
        "status"    : status,
        "response"  : {
                "message"   : message,
                "detail"    : detail,
                "data"      : data
            }
    }
    return response

def method_not_allowed():
    response    = {
        "status"    : 405,
        "response"  : [
            {
                "message"   : "Method not allowed",
                "detail"    : 
                    {
                        "message" : ["Method not allowed"]
                    },
                "data"      : []
            }
        ]
    }

    return response

def user_unauthorized(code):
    response    = {
        "status"    : 401,
        "response"  : [
            {
                "message"   : f"User unauthorized {code}",
                "detail"    : 
                    {
                        "message" : ["User cannot access this site"]
                    },
                "data"      : []
            }
        ]
    }

    return response

def errors_to_html(errors):
    error_list = []
    for key, value in errors.items():
        # error_list.append('<b>{}</b> :'.format(key.title()))
        error_list.append(f"<strong>{key.title().replace('_', ' ')}</strong>, {strip_tags(value)}")

    error_str = '<br />'.join(error_list)

    return error_str
    
def serializer_errors_to_str(message):
    errors          = {"message": val[0] for key, val in message.items()} 

    return errors.get("message")
