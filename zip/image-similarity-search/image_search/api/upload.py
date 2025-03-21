from fastapi import APIRouter, UploadFile, HTTPException, Response

from image_search.services.image_service import ImageServiceDep

router = APIRouter()

ALLOWED_CONTENT_TYPES = frozenset([
    "image/jpeg",
])


# This is not async because we do CPU-bound work here
@router.post("/upload/")
def upload_image(
        file: UploadFile,
        image_service: ImageServiceDep,
        response: Response
):
    try:
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise InvalidFileTypeException(file.content_type)
        result = image_service.upload_image(file.filename, file.file)
        response.status_code = 201
        return {"image_id": result.id}
    finally:
        file.close()


class InvalidFileTypeException(HTTPException):
    def __init__(self, content_type: str):
        super().__init__(status_code=400, detail=f"Invalid file type: {content_type}")
