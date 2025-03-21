from io import BytesIO
from pathlib import Path
from unittest import mock

import pytest

from image_search.db import Image
from image_search.services.errors import ImageNotFoundException
from image_search.services.file_storage_service import SaveFileResult, GetFileResult, FileNotFoundException
from image_search.services.image_service import ImageService, DownloadImageResult


class TestImageService:
    def test_upload_image(self, image_service: ImageService, file_storage_service, image_dao, image_search_service,
                          uuid_generator):
        # given
        given_filename = 'test.jpg'
        given_file_content = b'file_content'
        given_file = BytesIO(given_file_content)
        given_path = f'foo/{given_filename}'
        file_storage_service.save_file.return_value = SaveFileResult(path=Path(given_path))
        given_features = 'test features'
        image_search_service.index_image.return_value = mock.Mock(features=given_features)
        given_image_id = 'test image id'
        uuid_generator.generate_uuid.return_value = given_image_id
        image_dao.save_image.return_value = mock.Mock(id=given_image_id)

        # when
        actual_result = image_service.upload_image(given_filename, given_file)

        # then
        assert actual_result.id == given_image_id
        file_storage_service.save_file.assert_called_once_with(given_image_id, given_file)
        image_search_service.index_image.assert_called_once_with(filename=Path(given_path))
        expected_image = Image(id=given_image_id, filename=given_filename, features=given_features)
        image_dao.save_image.assert_called_once_with(expected_image)

    def test_download_image(self, image_service: ImageService, file_storage_service, image_dao):
        # given
        given_image_id = 'test image id'
        given_image = Image(
            id=given_image_id,
            filename='test.jpg',
            features='test features',
        )
        given_file_path = Path('foo/test.jpg')
        image_dao.get_image.return_value = given_image
        file_storage_service.get_file.return_value = GetFileResult(path=given_file_path)

        # when
        actual_result = image_service.download_image(given_image_id)

        # then
        assert actual_result == DownloadImageResult(filename=given_image.filename, path=given_file_path)
        image_dao.get_image.assert_called_once_with(given_image_id)
        file_storage_service.get_file.assert_called_once_with(given_image_id)

    def test_download_image_should_raise_not_found_when_image_not_found(self, image_service: ImageService, image_dao):
        # given
        given_image_id = 'test image id'
        image_dao.get_image.return_value = None

        # when
        with pytest.raises(ImageNotFoundException):
            image_service.download_image(given_image_id)

        # then
        image_dao.get_image.assert_called_once_with(given_image_id)

    def test_download_image_should_raise_not_found_when_file_not_found(self, image_service: ImageService, image_dao,
                                                                       file_storage_service):
        # given
        given_image_id = 'test image id'
        given_image = Image(
            id=given_image_id,
            filename='test.jpg',
            features='test features',
        )
        image_dao.get_image.return_value = given_image
        file_storage_service.get_file.side_effect = FileNotFoundException

        # when
        with pytest.raises(ImageNotFoundException):
            image_service.download_image(given_image_id)

        # then
        image_dao.get_image.assert_called_once_with(given_image_id)
        file_storage_service.get_file.assert_called_once_with(given_image_id)


@pytest.fixture
def image_service(file_storage_service, image_dao, image_search_service, uuid_generator):
    return ImageService(file_storage_service, image_dao, image_search_service, uuid_generator)


@pytest.fixture
def file_storage_service():
    return mock.Mock()


@pytest.fixture
def image_dao():
    return mock.Mock()


@pytest.fixture
def image_search_service():
    return mock.Mock()


@pytest.fixture
def uuid_generator():
    return mock.Mock()
