import json
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def open_json(filename: str) -> list[dict]:
    """
    Load and return JSON data from the specified file.

    Args:
        filename (str): Path to the JSON file.

    Returns:
        list[dict]: Parsed JSON data as a list of dictionaries.
    """
    with open(filename, "r") as f:
        return json.load(f)


def save_json(filename: str, data: list[dict]) -> None:
    """
    Save JSON data to a specified file.

    Args:
        filename (str): Path to the JSON file.
        data (list[dict]): Data to be saved in JSON format.

    Returns:
        None
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved JSON data to {filename}")


def delete_post_by_id(post_id: str) -> None:
    """
    Remove a blog post by its UUID from the JSON file.

    Args:
        post_id (str): UUID of the post to delete.

    Returns:
        None
    """
    blog_posts = open_json('blog_storage.json')
    filtered_blog_posts = [post for post in blog_posts if post["id"] != post_id]
    save_json('blog_storage.json', filtered_blog_posts)
    print(f"Deleted post with ID {post_id}")


def fetch_post_by_id(post_id: str) -> dict | None:
    """
    Retrieve a blog post by its UUID.

    Args:
        post_id (str): UUID of the post.

    Returns:
        dict | None: Post dictionary if found, otherwise None.
    """
    blog_posts = open_json('blog_storage.json')
    return next((post for post in blog_posts if post["id"] == post_id), None)


def update_post_by_id(post_id: str, title: str, author: str, content: str) -> bool:
    """
    Update a blog post's details in the JSON file.

    Args:
        post_id (str): UUID of the post to update.
        title (str): Updated title of the post.
        author (str): Updated author of the post.
        content (str): Updated content of the post.

    Returns:
        bool: True if the post was updated, otherwise False.
    """
    blog_posts = open_json('blog_storage.json')

    for post in blog_posts:
        if post["id"] == post_id:
            post["author"] = author
            post["title"] = title
            post["content"] = content
            save_json('blog_storage.json', blog_posts)
            print(f"Updated Post: {post}")
            return True
    return False


@app.route('/')
def index() -> str:
    """
    Render the homepage with all blog posts.

    Returns:
        str: Rendered HTML template with posts data.
    """
    blog_posts = open_json('blog_storage.json')
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add() -> str:
    """
    Handle adding a new blog post.

    Returns:
        str: Redirect to homepage after adding a post or render add.html form.
    """
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        blog_posts = open_json('blog_storage.json')

        new_post = {
            "id": str(uuid.uuid4()),  # Assigning a unique UUID
            "author": author,
            "title": title,
            "content": content,
            "likes": 0  # Initialize likes to 0
        }

        blog_posts.append(new_post)
        save_json('blog_storage.json', blog_posts)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<uuid:post_id>', methods=['POST'])
def delete(post_id: uuid.UUID) -> str:
    """
    Handle deletion of a blog post.

    Args:
        post_id (uuid.UUID): UUID of the post to delete.

    Returns:
        str: Redirect to homepage after deletion.
    """
    delete_post_by_id(str(post_id))
    return redirect(url_for('index'))


@app.route('/update/<uuid:post_id>', methods=['GET', 'POST'])
def update(post_id: uuid.UUID) -> str:
    """
    Handle updating an existing blog post.

    Args:
        post_id (uuid.UUID): UUID of the post to update.

    Returns:
        str: Redirect to homepage after updating or render update.html form.
    """
    post = fetch_post_by_id(str(post_id))

    if not post:
        print("Post not found!")
        return "Post not found", 404

    if request.method == 'POST':

        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]

        update_post_by_id(str(post_id), title, author, content)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<uuid:post_id>', methods=['POST'])
def like(post_id: uuid.UUID) -> str:
    """
    Handle liking a blog post by increasing its like count.

    Args:
        post_id (uuid.UUID): UUID of the post to like.

    Returns:
        str: Redirect to homepage after updating likes.
    """
    blog_posts = open_json('blog_storage.json')

    for post in blog_posts:
        if post["id"] == str(post_id):
            # Ensure 'likes' field exists, initialize if missing
            post["likes"] = post.get("likes", 0) + 1
            save_json('blog_storage.json', blog_posts)
            print(f"Post {post_id} now has {post['likes']} likes.")
            break

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
