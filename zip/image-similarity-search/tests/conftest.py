from tempfile import TemporaryDirectory, NamedTemporaryFile

import pytest

from image_search.settings import Settings


@pytest.fixture
def settings():
    with (TemporaryDirectory(prefix='image-search-image-dir-') as image_dir,
          NamedTemporaryFile(prefix='image-search-', suffix='.sqlite') as sqlite_file):
        yield Settings(image_dir=image_dir, sqlite_url=f"sqlite:///{sqlite_file.name}")
