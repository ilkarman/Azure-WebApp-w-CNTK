import os

os.environ['PATH'] = r'D:\home\site\wwwroot\cntk\cntk;' + os.environ['PATH']

import base64
import urllib
import numpy as np
from cntk import load_model, combine
from flask import render_template, request, json
from io import BytesIO
from PIL import Image, ImageOps
from WebApp import app

# Pre-load model
MODEL = load_model("Model/ResNet_18.model")
# Pre-load labels
with open('Model/synset-1k.txt', 'r') as f:
    LABELS = [l.rstrip() for l in f]


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/uploader", methods=['POST'])
def upload_file():
    # Check valid image and compress
    # Resnet requires size 224
    try:
        img = Image.open(BytesIO(request.files['imagefile'].read())).convert('RGB')
        img = ImageOps.fit(img, (224, 224), Image.ANTIALIAS)
        ret_imgio = BytesIO()
        img.save(ret_imgio, 'PNG')
    except:
        error_msg = "Please choose an image file"
        return render_template('index.html', **locals())

    classification = run_some_deep_learning_cntk(img)

    # Display re-sized picture
    png_output = base64.b64encode(ret_imgio.getvalue())
    processed_file = urllib.parse.quote(png_output)

    return render_template('index.html', **locals())


def run_some_deep_learning_cntk(rgb_pil_image):
    # Convert to BGR
    rgb_image = np.array(rgb_pil_image, dtype=np.float32)
    bgr_image = rgb_image[..., [2, 1, 0]]
    img = np.ascontiguousarray(np.rollaxis(bgr_image, 2))

    # Use last layer to make prediction
    z_out = combine([MODEL.outputs[3].owner])
    result = np.squeeze(z_out.eval({z_out.arguments[0]: [img]}))

    # Sort probabilities 
    a = np.argsort(result)[-1]
    predicted_category = " ".join(LABELS[a].split(" ")[1:])
    
    return predicted_category
