from fastapi import Request
import time
from server.dependencies import get_settings
from common.logger import AppLogger

settings = get_settings()
logger = AppLogger(__name__)


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def check_rapid_api_secret(request: Request, call_next):
    is_rapidapi = request.headers.get('X-RapidAPI-Proxy-Secret') \
            == settings.rapid_api_secret
    is_rapidapi = is_rapidapi or settings.env == 'dev'
    request.state.user = 'rapidapi' if is_rapidapi else ''
    response = await call_next(request)
    return response
