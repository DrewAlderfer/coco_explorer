import asyncio
import flask
from flask import request, url_for
import os
from tools import COCO_Image_Search, Record

app = flask.Flask(__name__)

@app.route('/')
def index():
    content = "welcome to 100 days of making COCO Dataset Planner/Explorer/Organizer<br>"
    content += "This is the landing page. It will include README information about this project and maybe some examples of drawings and their associated images."
    context = {
            "endpoint_1": "/",
            "endpoint_2": "/explorer",
            "endpoint_3": "/record",
            "link_text_1": "Home",
            "link_text_2": "Explorer",
            "link_text_3": "Record",
            "content": content
            }
    return flask.render_template('index.html', **context)

@app.get('/explorer')
def explorer_get():
    """
    The GET function for the explorer endpoint. This is what is displayed before
    a client makes sends a POST request for a set of search terms.
    """
    content = flask.render_template("explorer.html")
    context = {
            "endpoint_1": "/",
            "endpoint_2": "#",
            "endpoint_3": "/record",
            "link_text_1": "Home",
            "link_text_2": "Explorer",
            "link_text_3": "Record",
            "content": content
            }
    return flask.render_template('index.html', **context)

@app.post('/explorer')
def explorer_post():
    """
    This is the POST function for the explorer page. It takes the POST request
    from the client and runs the function.
    """
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
            "endpoint_2": "#",
            "endpoint_3": "/record",
            "link_text_1": "Home",
            "link_text_2": "Explorer",
            "link_text_3": "Record",
            "content": content
            }
    return flask.render_template('index.html', **context)


@app.route('/record')
def record():
    """
    Organizer and Recording Tab on the website.
    """
    days = Record().days
    results = ""

    print(url_for('static', filename=f'{days[0]["image"]}.jpg'))
    for day in days:
        if day['image']:
            url = url_for('static', filename=f'data/train2017/{day["image"]}.jpg')
            print(url)
            results += f'<span class="result"><img src="{url}"></img></span><br>\n'
        else: 
            continue
    content = flask.render_template("record.html", results=results)

    context = {
            "endpoint_1": "/",
            "endpoint_2": "/explorer",
            "endpoint_3": "#",
            "link_text_1": "Home",
            "link_text_2": "Explorer",
            "link_text_3": "Record",
            "content": content
            }
    return flask.render_template('index.html', **context)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
