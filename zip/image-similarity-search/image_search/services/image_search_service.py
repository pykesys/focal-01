from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import numpy as np
from fastapi import Depends
from sklearn.metrics.pairwise import cosine_similarity

from image_search.dao.image_dao import ImageDaoDep
from image_search.services.errors import ImageNotFoundException


@dataclass(frozen=True)
class IndexImageResult:
    features: bytes


@dataclass(frozen=True)
class SimilarImage:
    image_id: str
    score: float


@dataclass(frozen=True)
class SimilarImagesResult:
    images: list[SimilarImage]


class ImageSearchService(ABC):
    """
    Abstract class because maybe we want to implement different image search services in the future.
    """

    @abstractmethod
    def index_image(self, filename: Path) -> IndexImageResult:
        pass

    @abstractmethod
    def similar_images(self, image_id: str) -> SimilarImagesResult:
        pass


class Vgg16ImageSearchService:
    def __init__(self, image_dao: ImageDaoDep):
        self.__image_dao = image_dao

    def index_image(self, filename: Path) -> IndexImageResult:
        features = self.__extract_features(filename)
        return IndexImageResult(features=features.tobytes())

    def similar_images(self, image_id: str) -> SimilarImagesResult:
        """
        TODO This should be implemented using a vector database instead of a linear search.
        We could use Faiss or Annoy or vector extensions in a database like Postgres or SQLite.
        """
        needle = self.__image_dao.get_image(image_id)
        if needle is None:
            raise ImageNotFoundException(image_id)
        needle_features = np.frombuffer(needle.features, dtype=np.float32)
        haystack = self.__image_dao.get_all_images()

        results: list[SimilarImage] = []
        for haystack_image in haystack:
            haystack_features = np.frombuffer(haystack_image.features, dtype=np.float32)
            score = self.__calculate_score(needle_features, haystack_features)
            results.append(SimilarImage(image_id=haystack_image.id, score=score))
        results.sort(key=lambda r: r.score, reverse=True)

        # TODO parameterize the number of similar images
        return SimilarImagesResult(images=results[:5])

    @classmethod
    def __get_model(cls):
        # TODO move model to separate dependency and use lru_cache
        # Local imports because Keras is slow to import
        from keras.src.applications.vgg16 import VGG16

        if not hasattr(cls, '_model'):
            cls._model = VGG16(weights='imagenet', include_top=False, pooling='avg')
        return cls._model

    def __extract_features(self, img_path: Path) -> np.ndarray[np.float32]:
        # Local imports because Keras is slow to import
        from keras.api.preprocessing import image
        from keras.src.applications.vgg16 import preprocess_input

        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = self.__get_model().predict(x)
        return features.flatten()

    # TODO make this a strategy
    def __calculate_score(self, features1: np.ndarray, features2: np.ndarray) -> float:
        return self.__calculate_cosine_similarity(features1, features2)

    @staticmethod
    def __calculate_l2_distance(features1: np.ndarray, features2: np.ndarray) -> float:
        # This thinks supercar is more similar to dog than to cat
        return np.linalg.norm(features1 - features2).item()

    @staticmethod
    def __calculate_cosine_similarity(features1: np.ndarray, features2: np.ndarray) -> float:
        return cosine_similarity([features1], [features2]).item()


ImageSearchServiceDep = Annotated[ImageSearchService, Depends(Vgg16ImageSearchService)]
