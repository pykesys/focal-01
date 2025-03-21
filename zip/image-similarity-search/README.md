# Image search

A simple application that allows to:

* upload images
* download images
* search for similar images

API only. You can access API docs at `http://localhost:8000/docs`.

Built with:

* FastAPI
* SQLite for database
* Poetry
* Python 3.12

There are loads of TODOs throughout the code, but 80:20.

## Local development

### Install dependencies

```bash
poetry install
```

### Run the application in development mode

```bash
scripts/run-dev-mode.sh
```

> **Note**: The application will be available at `http://localhost:8000`.

### Run the application in docker

```bash
scripts/run-in-docker.sh
```

This will build the image and run the application in prd mode in a container.

> **Note**: The application will be available at `http://localhost:8000`.

> **Note**: The image is quite large, almost 4GB.

### Run unit tests

```bash
scripts/run-unit-tests.sh
```

### Run e2e tests

> **Note**: e2e tests require the application to be running.

```bash
scripts/run-e2e-tests.sh
```

## Algorithm description

There are multiple ways of doing image similarity search.
I've decided to use a deep learning model to extract features from images and use those
features to find similar images using cosine similarity.

In production system, I would probably compare multiple methods and multiple models to find the best one.

I've used the Vgg16 model to extract features from images.
I've used the model without the last layer, so it's not a classification model anymore, but a feature extractor.

This is like a RAG, but without AG and just R :)
