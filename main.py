from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from io import BytesIO
from PIL import Image
import base64
from model import find_and_display_similar_images # Import your model function

app = FastAPI()

# Mount static directory to serve HTML file
app.mount("/static", StaticFiles(directory='/home/aj/Downloads/ComputerVision/static'), name="static")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(BytesIO(contents)).convert("RGB")

    # Save the uploaded image temporarily
    input_image_path = "temp_input_image.jpg"
    input_image.save(input_image_path)

    # Directory where your image dataset is stored
    image_directory = 'path_to_your_image_dataset'

    # Find similar images using your model
    similar_images = find_and_display_similar_images(input_image_path, image_directory)

    # Generate HTML for displaying images
    html_content = generate_html(similar_images)
    return HTMLResponse(content=html_content, status_code=200)

def generate_html(similar_images):
    """ Generate HTML content to display similar images """
    images_html = '<h2>Similar Images</h2>'
    for image_path in similar_images:
        encoded_img = image_to_base64(image_path)
        images_html += f'<img src="data:image/jpeg;base64,{encoded_img}" alt="Similar Image" style="width:200px">'
    return images_html

def image_to_base64(image_path):
    """ Converts an image to its base64 representation. """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.get("/")
async def main():
    # Serve your HTML page
    with open('path_to_index.html', 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
