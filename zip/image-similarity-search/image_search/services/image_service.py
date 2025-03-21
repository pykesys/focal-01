from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, BinaryIO

from fastapi import Depends

from image_search.dao.image_dao import ImageDaoDep
from image_search.db import Image
from image_search.services.errors import ImageNotFoundException
from image_search.services.file_storage_service import FileStorageServiceDep, FileNotFoundException
from image_search.services.image_search_service import ImageSearchServiceDep
from image_search.services.uuid_generator import UUIDGeneratorDep


@dataclass(frozen=True)
class UploadImageResult:
    id: str


@dataclass(frozen=True)
class DownloadImageResult:
    filename: str
    path: Path


class ImageService:
    def __init__(
            self,
            file_storage_service: FileStorageServiceDep,
            image_dao: ImageDaoDep,
            image_search_service: ImageSearchServiceDep,
            uuid_generator: UUIDGeneratorDep,
    ):
        self.__file_storage_service = file_storage_service
        self.__image_dao = image_dao
        self.__image_search_service = image_search_service
        self.__uuid_generator = uuid_generator

    def upload_image(self, filename: str, file: BinaryIO) -> UploadImageResult:
        image_id = self.__uuid_generator.generate_uuid()
        save_file_result = self.__file_storage_service.save_file(image_id, file)
        features = self.__image_search_service.index_image(filename=save_file_result.path).features
        image = Image(
            id=image_id,
            filename=filename,
            features=features,
        )
        image = self.__image_dao.save_image(image)
        return UploadImageResult(id=image.id)

    def download_image(self, image_id: str) -> DownloadImageResult:
        image = self.__image_dao.get_image(image_id)
        if image is None:
            raise ImageNotFoundException(image_id=image_id)
        try:
            get_file_result = self.__file_storage_service.get_file(image_id)
        except FileNotFoundException:
            raise ImageNotFoundException(image_id=image_id)
        return DownloadImageResult(
            filename=image.filename,
            path=get_file_result.path
        )


ImageServiceDep = Annotated[ImageService, Depends(ImageService)]
