from flask import Flask, render_template
# from flask import request
import json


app = Flask(__name__)


# resp_data = b"""
# HTTP/1.1 200 OK
# Server: viola
# Accept-Ranges: bytes
# Content-Lenght: 11
# Content-Type: text/html

# <h1>ok</h1>
# """

resp_data = """
<h1>ok</h1>
"""


@app.route('/')
def hello_world():
    # print(request.path)
    # print(request.method)
    # return resp_data
    # return json.dumps({"name": "tiger", "age": 28, "sex": "male"})
    return render_template("hello.tpl", name="tiger")