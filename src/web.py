from flask import Flask, render_template, request
import cv2
import numpy as np
from main import analyze_road

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None

    if request.method == "POST":
        file = request.files.get("image")

        if file and file.filename != "":
            file_bytes = np.frombuffer(file.read(), np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if image is None:
                return "ERROR: File bukan gambar valid"

            data = analyze_road(image)

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
