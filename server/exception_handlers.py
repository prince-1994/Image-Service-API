import json
from fastapi import Request, Response, status
from common.exceptions import AppException, UnknownClientException


EXCEPTION_TO_STATUS_CODE_MAPPING = {
    UnknownClientException: status.HTTP_401_UNAUTHORIZED
}


async def app_exception_handler(request: Request, exc: AppException):
    """Exception handler for Exceptions"""
    status_code = EXCEPTION_TO_STATUS_CODE_MAPPING[type(exc)]
    return Response(content=json.dumps({"error": exc.detail}),
                    status_code=status_code)
