import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import os

def get_image_features(image_path, model, processor):
    """ Extracts features from an image using the CLIP model. """
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    outputs = model.get_image_features(**inputs)
    return outputs.detach().numpy()

def list_image_files(directory):
    """ Lists all image files in the given directory. """
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) 
            and os.path.splitext(f)[1].lower() in supported_extensions]


def find_and_display_similar_images(input_image_path, image_directory, top_k=5):
    """ Finds and displays top_k similar images to the input image. """

    # Load the pre-trained CLIP model
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
    
    # Get the list of image file paths
    image_dataset_paths = list_image_files(image_directory)
    
    # Find similar images
    input_features = get_image_features(input_image_path, model, processor)
    similarities = []
    for path in image_dataset_paths:
        features = get_image_features(path, model, processor)
        sim = cosine_similarity(input_features, features)
        similarities.append((path, sim[0][0]))

    # Sort and select top similar images
    similarities.sort(key=lambda x: x[1], reverse=True)
    similar_images = similarities[:top_k]

    # Display the images
    plt.figure(figsize=(15, 10))
    plt.subplot(1, len(similar_images) + 1, 1)
    plt.imshow(Image.open(input_image_path))
    plt.title("Input Image")
    plt.axis('off')
    for i, (path, similarity) in enumerate(similar_images, start=2):
        plt.subplot(1, len(similar_images) + 1, i)
        plt.imshow(Image.open(path))
        plt.title(f"Similarity: {similarity:.2f}")
        plt.axis('off')
    plt.show()

# Example usage
#input_image_path = 'gdrive/My Drive/Colab Notebooks/NLP/Training data/boston_677231_2.jpg'
#image_directory = 'gdrive/My Drive/Colab Notebooks/NLP/Training data/'

# Call the function
#find_and_display_similar_images(input_image_path, image_directory)
