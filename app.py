import json

from flask import Flask, render_template, request

app = Flask(__name__)


def open_json(filename):
    with open(filename) as f:
        return json.load(f)
@app.route('/')
def index():
    blog_posts = open_json('blog_storage.json')
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    app.run()
