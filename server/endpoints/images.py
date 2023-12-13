from fastapi import APIRouter, UploadFile, Request, BackgroundTasks, status
from fastapi.responses import FileResponse, Response
from PIL import Image
from app.images.usecases import edit
import os
import uuid

router = APIRouter()


def remove_file(path: str) -> None:
    os.unlink(path)


valid_image_formats = {"png", "jpeg", "jpg", "tiff", "bmp", "ppm"}


@router.post("/edit")
async def edit_file(
    file: UploadFile,
    request: Request,
    background_tasks: BackgroundTasks,
    format: str = "jpg"
):
    if format not in valid_image_formats:
        return Response(
            {"msg": "Invalid format for output image"},
            status_code=status.HTTP_400_BAD_REQUEST
            )
    try:
        img = Image.open(file.file)
        edited_img = edit(img, request.query_params)
        file_path = f"tmp/images/{str(uuid.uuid4())}.{format}"
        edited_img.save(file_path)
        background_tasks.add_task(remove_file, file_path)
        return FileResponse(file_path)
    except OSError:
        return Response(
            {"msg": "Invalid request - Maybe image is not valid"},
            status_code=status.HTTP_400_BAD_REQUEST
            )
