from . import models

def requestObjectMiddleware(get_response):

    def Middleware(request):
        models.request_object = request
        response = get_response(request)
        return response
    return Middleware