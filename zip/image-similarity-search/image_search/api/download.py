from fastapi import APIRouter
from fastapi.responses import FileResponse

from image_search.services.image_service import ImageServiceDep

router = APIRouter()


# This is not async because we use blocking DB operations
@router.get("/download/{image_id}/")
def download_image(image_id: str, image_service: ImageServiceDep):
    image = image_service.download_image(image_id)
    return FileResponse(
        path=image.path,
        filename=image.filename,
    )
