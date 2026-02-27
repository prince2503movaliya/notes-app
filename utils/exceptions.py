from rest_framework.views import exception_handler
from utils.response import error_response
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response(error_response(response.data, "Something went wrong"))

    return Response(error_response(message="Server error"), status=500)