import json
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def open_json(filename):
    with open(filename) as f:
        return json.load(f)

def save_json(filename, data):
    """Save JSON data to a file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)



@app.route('/')
def index():
    blog_posts = open_json('blog_storage.json')
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        # Load existing blog posts
        blog_posts = open_json('blog_storage.json')

        # Create a new post entry with an uuid ID
        new_post = {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content
        }

        # Append new post and save back to JSON
        blog_posts.append(new_post)
        save_json('blog_storage.json', blog_posts)

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    print(f"Received DELETE request for post ID: {post_id}")  # Debugging

    blog_posts = open_json('blog_storage.json')
    initial_count = len(blog_posts)

    # Filter out the post with the given UUID
    updated_posts = [post for post in blog_posts if post["id"] != post_id]

    if len(updated_posts) < initial_count:
        print(f"Post {post_id} deleted successfully.")  # Debugging
    else:
        print(f"Post {post_id} not found or deletion failed.")  # Debugging

    print("Updated JSON Data:", updated_posts)  # Debugging

    save_json('blog_storage.json', updated_posts)  # Save updated JSON

    # Re-load JSON to confirm deletion
    reloaded_posts = open_json('blog_storage.json')
    print("Reloaded JSON Data:", reloaded_posts)

    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run()
