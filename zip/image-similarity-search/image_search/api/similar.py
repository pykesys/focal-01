from fastapi import APIRouter
from fastapi.responses import JSONResponse

from image_search.services.image_search_service import ImageSearchServiceDep, SimilarImage

router = APIRouter()


class SimilarImagesResponse(JSONResponse):
    def __init__(self, images: list[SimilarImage]):
        converted_images = [{'image_id': i.image_id, 'score': i.score} for i in images]
        super().__init__(content={"images": converted_images})


# This is not async because we do CPU-bound work here
@router.get("/similar/{image_id}/")
def similar_images(image_id: str, image_search_service: ImageSearchServiceDep):
    search_result = image_search_service.similar_images(image_id)
    return SimilarImagesResponse(images=search_result.images)
