from rest_framework.response import Response


def success_response(data=None, message="ok", status=200):
    return Response(
        {
            "code": 0,
            "message": message,
            "data": data,
        },
        status=status,
    )
