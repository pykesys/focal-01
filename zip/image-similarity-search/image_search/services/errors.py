from fastapi import HTTPException


class ImageNotFoundException(HTTPException):
    def __init__(self, image_id: str):
        super().__init__(status_code=404, detail=f"Image not found: {image_id}")
