from fastapi import FastAPI, Response, status
from server.dependencies import get_settings
from server.endpoints.images import router as images_router
from common.exceptions import AppException
from server.exception_handlers import app_exception_handler
from common.logger import AppLogger
from server.middlewares import add_process_time_header, check_rapid_api_secret

logger = AppLogger(__name__)
settings = get_settings()

# Very Imp Note: Exception handlers don't get triggered from middlewares

app = FastAPI(
    debug=settings.debug,
    exception_handlers={AppException: app_exception_handler})
app.middleware('http')(add_process_time_header)
app.middleware('http')(check_rapid_api_secret)
app.include_router(images_router, prefix='/images')


@app.get('/ping')
def ping():
    return Response(status_code=status.HTTP_200_OK)
