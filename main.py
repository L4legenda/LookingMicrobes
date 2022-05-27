from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import json
import io
import base64
import cv2
from imageio import imread
from colorutils import Color

app = Flask(__name__, static_url_path="/static")


def searchAllColors(imgHsv):
    colors = []
    for line in range(0, len(imgHsv), 5):
        for c in range(0, len(imgHsv[line]), 12):
            col = imgHsv[line][c]
            col = tuple((int(col[0]), int(col[1]), int(col[2])))
            isColor = True
            for cs in colors:
                if col == cs:
                    isColor = False
                    break
            if isColor:
                colors.append(col)
    return colors


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    data = json.loads(request.data)
    data["file"] = data['file'].split(",")[1]
    img = imread(io.BytesIO(base64.b64decode(data["file"])))
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    color = tuple(data["color"])

    mask = cv2.inRange(imgHsv, color, color)

    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    count = 0
    if contours:
        contours = contours[0]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 3)
        count = len(contours)


    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer).decode("utf-8")
    data["file"] = jpg_as_text
    data["count"] = count

    return jsonify(data)


@app.route("/getcolors", methods=["POST"])
def getcolors():
    data = json.loads(request.data.decode("utf-8"))
    data["file"] = data['file'].split(",")[1]
    img = imread(io.BytesIO(base64.b64decode(data["file"])))
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    colors = searchAllColors(imgHsv)
    return jsonify(colors)


app.run()
