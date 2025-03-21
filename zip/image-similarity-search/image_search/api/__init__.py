from fastapi import APIRouter

from image_search.api import upload, download, similar

router = APIRouter()

router.include_router(upload.router)
router.include_router(download.router)
router.include_router(similar.router)
