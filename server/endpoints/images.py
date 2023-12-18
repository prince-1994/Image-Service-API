from fastapi import APIRouter, Request, BackgroundTasks, status
from fastapi.responses import FileResponse, Response
from PIL import Image
from app.images.usecases import edit
import os
import uuid
from common.logger import AppLogger
import json

router = APIRouter()
logger = AppLogger(__name__)


valid_image_formats = {"png", "jpeg", "jpg", "tiff", "bmp", "ppm"}


@router.post("/edit")
async def edit_file(
    request: Request,
    background_tasks: BackgroundTasks,
    format: str = "png"
):
    if request.state.user != 'rapidapi':
        logger.info(
                f"UnknownClient: {request.client} | {request.url}")
        return Response(
            json.dumps({"msg": "Unauthorized to perform this request"}),
            status_code=status.HTTP_401_UNAUTHORIZED)
    if format not in valid_image_formats:
        return Response(
            json.dumps({"msg": "Invalid format for output image"}),
            status_code=status.HTTP_400_BAD_REQUEST
            )
    response = None
    try:
        cur_id = str(uuid.uuid4())
        input_filepath = f"tmp/images/input-{cur_id}"
        output_filepath = f"tmp/images/output-{cur_id}.{format}"
        with open(input_filepath, 'wb') as f:
            f.write(await request.body())
        logger.info(cur_id)
        img = Image.open(input_filepath)
        edited_img = edit(img, request.query_params)
        edited_img.save(output_filepath)
        response = FileResponse(output_filepath)
    except OSError:
        response = Response(
            json.dumps({"msg": "Invalid request - Maybe image is not valid"}),
            status_code=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        logger.error(e)
        response = Response(
            json.dumps({"msg": "Something went wrong"}),
            status_code=status.HTTP_400_BAD_REQUEST
            )
    finally:
        if os.path.exists(input_filepath):
            background_tasks.add_task(os.unlink, input_filepath)
        if os.path.exists(output_filepath):
            background_tasks.add_task(os.unlink, output_filepath)
    return response
