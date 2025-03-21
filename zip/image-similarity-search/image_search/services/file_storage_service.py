import shutil
from abc import abstractmethod, ABC
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Annotated, BinaryIO

from fastapi import Depends

from image_search.settings import SettingsDep


@dataclass(frozen=True)
class SaveFileResult:
    path: Path


@dataclass(frozen=True)
class GetFileResult:
    path: Path


class FileNotFoundException(Exception):
    pass


class FileStorageService(ABC):
    @abstractmethod
    def save_file(self, file_id: str, file: IO[bytes]) -> SaveFileResult:
        pass

    @abstractmethod
    def get_file(self, file_id: str) -> GetFileResult:
        pass


class SimpleFileStorageService(FileStorageService):
    """
    This class is a simple implementation of the FileStorageService interface.
    Normally I would store the file in a cloud storage service like S3 or GCS.
    But it is what is it.

    We save files in the image_dir with filename equal to file_id.
    """

    def __init__(
            self,
            settings: SettingsDep,
    ):
        self.__image_dir = Path(settings.image_dir)

    def save_file(self, file_id: str, file: BinaryIO):
        file_path = self.__image_dir / file_id
        with open(file_path, "wb") as f:
            # noinspection PyTypeChecker
            shutil.copyfileobj(file, f)
        return SaveFileResult(path=file_path)

    def get_file(self, file_id: str) -> GetFileResult:
        filename = self.__image_dir / file_id
        if not filename.exists():
            raise FileNotFoundException()
        return GetFileResult(path=filename)


FileStorageServiceDep = Annotated[FileStorageService, Depends(SimpleFileStorageService)]
