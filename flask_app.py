import os
import json
from flask import Flask, request, jsonify
import vertexai
from google.oauth2 import service_account
from vertexai.preview.generative_models import GenerativeModel
import functions_framework
from vertexai.preview.vision_models import ImageGenerationModel
import pathlib
import io
import base64

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1> Home Page! </h1>"

# Initialize Vertex AI
PROJECT_ID = "lucky-processor-443818-m3"
LOCATION = "us-central1"
CREDENTIALS_FILE = "/home/yemoe/sites/my_project/vertexai_key.json"

# Load service account credentials
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)

@app.route("/id")
def get_id():
    if request.method == "OPTIONS":
                headers = {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Max-Age": "3600",
                }

                return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "*"}

    return ("24266607_Moe", 200, headers)

@app.route("/recipe-instructions")
def get_recipe():

    if request.method == "OPTIONS":
                headers = {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Max-Age": "3600",
                }

                return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "*"}

    # Load the Generative Model
    gemini_model = GenerativeModel(model_name="gemini-1.5-flash")

    # Get query parameters
    dish_name = request.args.get("name")
    minutes_under = request.args.get("minutes_under", 80)

    if not dish_name:
        return ({}, 200, headers)

    # Construct prompt
    text_prompt = f"""
    What is the recipe for {dish_name} under {minutes_under} minutes? Respond in the JSON format below.
    If you do not have the recipe for the dish, respond with an empty JSON.

    {{
        "name": "<the name of the dish>",
        "prep_time": "<the time needed to prepare the dish>",
        "cook_time": "<the time needed to cook the dish>",
        "ingredients": [
            {{"<name of the cooking part>": ["list of ingredients"]}},
            ...
        ],
        "instructions": [
            {{"<name of the cooking part>": ["list of instructions"]}},
            ...
        ]
    }}
    """

    # Start a chat session
    response = gemini_model.generate_content(contents=text_prompt)

    # Remove first and last lines from AI-generated response
    text_response = response.text
    cleaned_response = text_response.strip('```json').strip('```').strip()
    json_response = json.loads(cleaned_response)

    # Return the AI-generated response
    return (json_response, 200, headers)

@app.route("/recipe-image")
def get_image():
    if request.method == "OPTIONS":
                headers = {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Max-Age": "3600",
                }

                return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "*",
    "Content-Type": "image/png",
    }

    image_name = request.args.get("name")

    imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

    image_prompt = image_name

    response = imagen_model.generate_images(
        prompt=image_prompt,
        aspect_ratio='16:9'
    )
    image = response.images[0]
    image.show()

    pathlib.Path('tmp.png').write_bytes(image._image_bytes)

    image._size
    # PNG : 512x288
    len(image._image_bytes)
    pilimage = image._pil_image.resize((512, 288))

    pilimage.save('tmp_small.png')

    image_bytes = pathlib.Path('tmp_small.png').read_bytes()

    return (image_bytes, 200, headers)

@app.route("/recipe")
def get_recipe_final():

    if request.method == "OPTIONS":
                headers = {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Max-Age": "3600",
                }

                return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "*"}

    # Load the Generative Model
    gemini_model = GenerativeModel(model_name="gemini-1.5-flash")

    # Get query parameters
    dish_name = request.args.get("name")
    minutes_under = request.args.get("minutes_under", 80)

    if not dish_name:
        return ({}, 200, headers)

    # Construct prompt
    text_prompt = f"""
    What is the recipe for {dish_name} under {minutes_under} minutes? Respond in the JSON format below.
    If you do not have the recipe for the dish, respond with an empty JSON.

    {{
        "name": "<the name of the dish>",
        "prep_time": "<the time needed to prepare the dish>",
        "cook_time": "<the time needed to cook the dish>",
        "ingredients": [
            {{"<name of the cooking part>": ["list of ingredients"]}},
            ...
        ],
        "instructions": [
            {{"<name of the cooking part>": ["list of instructions"]}},
            ...
        ]
    }}
    """

    # Start a chat session
    response = gemini_model.generate_content(contents=text_prompt)

    # Remove first and last lines from AI-generated response
    text_response = response.text
    cleaned_response = text_response.strip('```json').strip('```').strip()


    image_name = request.args.get("name")

    imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

    image_prompt = image_name

    response = imagen_model.generate_images(
        prompt=image_prompt,
        aspect_ratio='16:9'
    )
    image = response.images[0]
    image.show()

    pathlib.Path('tmp.png').write_bytes(image._image_bytes)

    image._size
    # PNG : 512x288
    len(image._image_bytes)
    pilimage = image._pil_image.resize((512, 288))

    pilimage.save('tmp_small.png')

    image_bytes = pathlib.Path('tmp_small.png').read_bytes()

    buffer = io.BytesIO()
    pilimage.save(buffer, format="PNG")
    buffer.getvalue()
    pathlib.Path('tmp_small.png').write_bytes(buffer.getvalue())

    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    base64_image = "data:image/png;base64," + base64_image


    # new_response.image = base64_image
    recipe = json.loads(cleaned_response)
    recipe["image"] = base64_image
    # Return the AI-generated response
    # return (recipe, 200, headers)
    return (recipe, 200, headers)

if __name__ == "__main__":
    app.run(debug=True)