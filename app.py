import json
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Function to load JSON data
def open_json(filename):
    with open(filename) as f:
        return json.load(f)

# Function to save JSON data
def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved JSON data to {filename}")

# Function to delete a post by UUID
def delete_post_by_id(post_id):
    blog_posts = open_json('blog_storage.json')
    filtered_blog_posts = [post for post in blog_posts if post["id"] != str(post_id)]  # Convert UUID to string
    save_json('blog_storage.json', filtered_blog_posts)

    print(f"Deleted post with ID {post_id}")

# Function to fetch a post by UUID
def fetch_post_by_id(post_id):
    blog_posts = open_json('blog_storage.json')
    return next((post for post in blog_posts if post["id"] == str(post_id)), None)  # Convert UUID to string

# Function to update a post by UUID
def update_post_by_id(post_id, title, author, content):
    """Finds and updates a post in the JSON file."""
    blog_posts = open_json('blog_storage.json')

    for post in blog_posts:
        if post["id"] == str(post_id):  # Convert UUID to string
            post["author"] = author
            post["title"] = title
            post["content"] = content
            save_json('blog_storage.json', blog_posts)
            print(f"Updated Post: {post}")  # Debugging
            return True  # Successfully updated

    return False  # Post not found

# Route: Homepage (Displays all blog posts)
@app.route('/')
def index():
    blog_posts = open_json('blog_storage.json')
    return render_template('index.html', posts=blog_posts)

# Route: Add New Post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Load existing blog posts
        blog_posts = open_json('blog_storage.json')

        # Create a new post entry with a UUID ID
        new_post = {
            "id": str(uuid.uuid4()),  # Assign a unique UUID
            "author": author,
            "title": title,
            "content": content
        }

        # Append new post and save back to JSON
        blog_posts.append(new_post)
        save_json('blog_storage.json', blog_posts)

        return redirect(url_for('index'))
    return render_template('add.html')

# Route: Delete a Post (Uses UUID)
@app.route('/delete/<uuid:post_id>', methods=['POST'])
def delete(post_id):
    """Deletes a blog post by its UUID."""
    delete_post_by_id(post_id)
    return redirect(url_for('index'))

# Route: Update an Existing Post (Uses UUID)
@app.route('/update/<uuid:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Handles updating an existing blog post using UUID validation."""
    post = fetch_post_by_id(post_id)

    if not post:
        print("Post not found!")  # Debugging
        return "Post not found", 404

    if request.method == 'POST':
        # Retrieve updated values from form
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]

        update_post_by_id(post_id, author, title, content)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run()
