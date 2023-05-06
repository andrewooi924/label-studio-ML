import os
import tempfile

import pytest
from google.cloud import storage
from utils.gcs import download_public_file, get_metadata_from_url

BUCKET = "ucf-crime-dataset"
TEST_VIDEO = "Assault/Assault038_x264.mp4"


@pytest.fixture
def destination_file_name():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        return f.name


def test_download_public_file(destination_file_name):
    download_public_file(BUCKET, TEST_VIDEO, destination_file_name)
    assert os.path.exists(destination_file_name)
    assert os.path.getsize(destination_file_name) > 0


def test_get_metadata_from_url():
    url = f"gs://{BUCKET}/{TEST_VIDEO}"
    assert get_metadata_from_url(url) == (BUCKET, TEST_VIDEO, "Assault038_x264.mp4")
