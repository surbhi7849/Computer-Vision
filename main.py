from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn
from io import BytesIO
#from your_model_module import find_similar_images, display_images # Import your ML model and functions here

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(BytesIO(contents)).convert("RGB")

    # Save the uploaded image temporarily if needed
    input_image_path = "temp_input_image.jpg"
    input_image.save(input_image_path)

    # Assuming you have a function to find similar images
    similar_images = find_similar_images(input_image_path, image_dataset_paths, model, processor)

    # Generate and return an HTML page with the input and similar images displayed
    # You would need to modify display_images function to return an HTML string or handle it here
    html_content = generate_html_content(input_image_path, similar_images)
    return HTMLResponse(content=html_content, status_code=200)

def generate_html_content(input_image_path, similar_images):
    # Implement a function that generates an HTML string to display images
    # This could use <img> tags to show the input and similar images
    pass

@app.get("/")
def read_root():
    return {"message": "Welcome to the Visual Echoes: Airbnb Edition API"}

# Additional routes and logic as needed

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn
from PIL import Image
from io import BytesIO
from your_model_module import find_similar_images, display_images  # Import your ML model and functions

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(BytesIO(contents)).convert("RGB")

    # Save the uploaded image temporarily
    input_image_path = "temp_input_image.jpg"
    input_image.save(input_image_path)

    # Assuming you have a function to find similar images
    similar_images = find_similar_images(input_image_path, image_dataset_paths, model, processor)

    # Generate an HTML response
    html_content = generate_html_content(input_image_path, similar_images)
    return HTMLResponse(content=html_content, status_code=200)

def generate_html_content(input_image_path, similar_images):
    """ Generates HTML content with the input and similar images. """
    images_html = f'<img src="data:image/jpeg;base64,{image_to_base64(input_image_path)}" alt="Input Image" style="width:200px">'
    
    for image_path, _ in similar_images:
        images_html += f'<img src="data:image/jpeg;base64,{image_to_base64(image_path)}" alt="Similar Image" style="width:200px">'
    
    return images_html

def image_to_base64(image_path):
    """ Converts an image to its base64 representation. """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.get("/")
async def main():
    content = """
    <body>
    <form action="/uploadfile/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)

#uvicorn main:app --reload
