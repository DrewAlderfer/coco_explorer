import asyncio
import flask
from flask import request, url_for
import os
from tools import COCO_Image_Search

app = flask.Flask(__name__)

@app.route('/')
def index():
    content = "welcome to 100 days of making COCO Dataset Planner/Explorer/Organizer<br>"
    content += "This is the landing page. It will include README information about this project and maybe some examples of drawings and their associated images."
    context = {
            "endpoint_1": "/explorer",
            "endpoint_2": "/record",
            "link_text_1": "Explorer",
            "link_text_2": "Record",
            "content": content
            }
    return flask.render_template('index.html', **context)

@app.get('/explorer')
def explorer_get():
    content = flask.render_template("explorer.html")
    context = {
            "endpoint_1": "/",
            "endpoint_2": "/record",
            "link_text_1": "Home",
            "link_text_2": "Record",
            "content": content
            }
    return flask.render_template('index.html', **context)

@app.post('/explorer')
def explorer_post():
    if 'search' in request.form:
        img_search = COCO_Image_Search()
        cats = request.form['categories'].split()
        pattern = request.form['caption_search'].split()
        images = img_search.cat_search(cats).caption_contains(pattern).get_results()
        print(images)
        results = ""
        for x in images.output[0]:
            url = url_for('static', filename=x)
            results += f'<span class="result"><img src="{url}"></img></span><br>\n'
        print(results)
    else:
        results = None
    content = flask.render_template("explorer.html", results=results)
    context = {
            "endpoint_1": "/",
            "endpoint_2": "/record",
            "link_text_1": "Home",
            "link_text_2": "Record",
            "content": content
            }
    return flask.render_template('index.html', **context)


@app.route('/record')
def record():
    content = "welcome to 100 days of making COCO Dataset Planner/Explorer/Organizer:<br>"
    content += "This is the planner/record page. It records the completed days with their COCO data objects and my drawing. It also stores days that have yet to be completed but for which I have already selected a photo from the dataset."
    context = {
            "endpoint_1": "/",
            "endpoint_2": "/explorer",
            "link_text_1": "Home",
            "link_text_2": "Explorer",
            "content": content
            }
    return flask.render_template('index.html', **context)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
