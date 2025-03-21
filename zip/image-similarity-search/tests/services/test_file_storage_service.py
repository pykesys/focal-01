from io import BytesIO
from pathlib import Path

import pytest

from image_search.services.file_storage_service import SimpleFileStorageService, FileNotFoundException
from image_search.settings import Settings


class TestSimpleFileStorageService:
    def test_save_file(self, simple_file_storage_service: SimpleFileStorageService):
        # given
        given_file_id = 'test file id'
        given_file_content = b"file_content"

        # when
        actual_result = simple_file_storage_service.save_file(file_id=given_file_id, file=BytesIO(given_file_content))

        # then
        assert actual_result.path.exists()
        assert actual_result.path.read_bytes() == given_file_content

    def test_get_file(self, simple_file_storage_service: SimpleFileStorageService, settings: Settings):
        # given
        given_file_id = 'test file id'
        given_file_content = b"file_content"
        given_file_path = Path(settings.image_dir) / given_file_id
        given_file_path.write_bytes(given_file_content)

        # when
        actual_result = simple_file_storage_service.get_file(file_id=given_file_id)

        # then
        assert actual_result.path == given_file_path

    def test_should_raise_exception_when_file_not_found(self, simple_file_storage_service: SimpleFileStorageService):
        # given
        given_file_id = 'test file id'

        # when
        with pytest.raises(FileNotFoundException):
            simple_file_storage_service.get_file(file_id=given_file_id)


@pytest.fixture
def simple_file_storage_service(settings) -> SimpleFileStorageService:
    return SimpleFileStorageService(settings=settings)
