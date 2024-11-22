# Image Classification

Image classification is a type of supervised learning where the model is trained to recognize and classify images into different categories or classes. It is a popular application of computer vision and deep learning, and is used in various fields such as healthcare, security, and autonomous vehicles. I wanted to make it easier to use image classiication models with Python therefore; I created some adapters for use with Ollama.

## Basic Usage

If your Ollama server is running locally and you have a model downloaded that classifies images, you can use the following code to classify an image:

```python
from inspyollama_client.client import LlamaClient

client = LlamaClient()  # Connect to the server

```
