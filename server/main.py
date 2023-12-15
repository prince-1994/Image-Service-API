from fastapi import FastAPI, Request, Response, status
from server.dependencies import get_settings
from server.endpoints.images import router as images_router
import time
from common.exceptions import UnknownClientException, AppException
from common.logger import AppLogger
import json

logger = AppLogger(__name__)
settings = get_settings()
EXCEPTION_TO_STATUS_CODE_MAPPING = {
    UnknownClientException: status.HTTP_401_UNAUTHORIZED
}


app = FastAPI(
    debug=settings.debug)


# Very Imp Note: Exception handlers don't get triggered from middlewares
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Exception handler for Exceptions"""
    status_code = EXCEPTION_TO_STATUS_CODE_MAPPING[type(exc)]
    return Response(content=json.dumps({"error": exc.detail}),
                    status_code=status_code)


@app.on_event('startup')
async def startup():
    pass


@app.on_event('shutdown')
async def shutdown():
    pass


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware('http')
async def check_rapid_api_secret(request: Request, call_next):
    if (request.headers.get('X-RapidAPI-Proxy-Secret')
            == settings.rapid_api_secret):
        response = await call_next(request)
        return response
    else:
        logger.info(
            f"UnknownClient: {request.client} | {request.url}")
        return Response(
            json.dumps({"msg": "Unauthorized to perform this request"}),
            status_code=status.HTTP_401_UNAUTHORIZED
        )

app.include_router(images_router, prefix='/images')


@app.get('/ping')
def ping():
    return Response(status_code=status.HTTP_200_OK)
