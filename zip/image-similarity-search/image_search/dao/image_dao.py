from typing import Annotated

from fastapi import Depends

from image_search.db import DatabaseSessionDep, Image


class ImageDao:
    def __init__(self, db_session: DatabaseSessionDep):
        self.__db_session = db_session

    def save_image(self, image: Image) -> Image:
        self.__db_session.add(image)
        self.__db_session.commit()
        self.__db_session.refresh(image)
        return image

    def get_image(self, image_id: str) -> Image | None:
        return self.__db_session.get(Image, image_id)

    def get_all_images(self) -> list[Image]:
        # TODO add pagination
        return self.__db_session.query(Image).all()


ImageDaoDep = Annotated[ImageDao, Depends(ImageDao)]
