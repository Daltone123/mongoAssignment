import os
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

app = Flask(__name__)

# Load your pre-trained model
MODEL_PATH = "cats_dogs.keras"
model = load_model(MODEL_PATH)

# Ensure an upload folder exists to temporarily hold images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def preprocess_image(image_path):
    """Resizes the image to 128x128 and normalizes pixel values."""
    img = load_img(image_path, target_size=(128, 128))
    img_array = img_to_array(img)
    # Expand dimensions to add the batch size: (128, 128, 3) -> (1, 128, 128, 3)
    img_array = np.expand_dims(img_array, axis=0)
    # Rescale pixel values if your training step scaled them (e.g., dividing by 255)
    img_array = img_array / 255.0 
    return img_array

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if an actual file was uploaded
        if "file" not in request.files:
            return render_template("index.html", error="No file part uploaded.")
        
        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", error="No image selected.")

        if file:
            # Save the file temporarily
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Process image and run prediction
            processed_img = preprocess_image(file_path)
            prediction = model.predict(processed_img)[0][0]

            # Convert sigmoid float output into discrete labels and confidence scores
            if prediction >= 0.5:
                label = "Dog 🐶"
                confidence = round(float(prediction) * 100, 2)
            else:
                label = "Cat 🐱"
                confidence = round((1.0 - float(prediction)) * 100, 2)

            return render_template("index.html", label=label, confidence=confidence, filename=file.filename)


    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
