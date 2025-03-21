from requests import request, Response

BASE_URL = 'http://localhost:8000'
API_URL = f'{BASE_URL}/api'
UPLOAD_URL = f'{API_URL}/upload/'
DOWNLOAD_URL = f'{API_URL}/download'
SIMILAR_URL = f'{API_URL}/similar'


# FIXME this test might stop working if we run it more than 5 times, too many identical cat images, our image might not get returned :)

def test_upload_download_similarity():
    # Upload test images
    response = upload('orange-cat.jpg')
    assert_response(response, 201)
    orange_cat_id = response.json()['image_id']

    response = upload('golden-dog.jpg')
    assert_response(response, 201)

    response = upload('sports-car.jpg')
    assert_response(response, 201)

    # Download one image
    response = download(orange_cat_id)
    assert_response(response, 200)
    assert response.headers['Content-Type'] == 'image/jpeg'
    assert response.headers['Content-Disposition'] == 'attachment; filename="orange-cat.jpg"'

    # Find similar images
    response = similar(orange_cat_id)
    assert_response(response, 200)
    similar_images = response.json()['images']
    assert len(similar_images) >= 3  # At least the 3 uploaded images
    # One of the top results is our image
    # The score is not perfect because of floating point precision
    top_score = similar_images[0]['score']
    assert any(i['image_id'] == orange_cat_id and i['score'] == top_score for i in similar_images)


def upload(file_path: str) -> Response:
    response = request("POST", UPLOAD_URL, files={
        'file': (file_path, open(file_path, 'rb'), 'image/jpeg')
    })
    return response


def download(image_id: str) -> Response:
    response = request("GET", f'{DOWNLOAD_URL}/{image_id}/')
    return response


def similar(image_id: str) -> Response:
    response = request("GET", f'{SIMILAR_URL}/{image_id}/')
    return response


def assert_response(response, status_code):
    assert response.status_code == status_code, response.text
