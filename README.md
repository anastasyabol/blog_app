# Blog Application
This is a simple Flask-based blog application that enables users to view, add, update, and delete blog posts. The application utilizes a JSON file (posts_data.json) to store blog post data.

# Features
View Blog Posts: Check the home page for a list of existing blog posts.
Add a New Post: Click on the "Add" link in the navigation menu, fill in the required fields (title, author, content), and submit the form.
Update a Post: Click on the "Update" link next to a post, modify its content, and submit the form to update the post.
Delete a Post: Click on the "Delete" link next to a post to remove it permanently.

## Project Structure
app.py: Main Flask application file with routes and logic for handling blog posts.

posts_data.json: JSON file used to store blog post data.

templates/: Directory containing HTML templates for different pages.

static/: Directory for static files such as CSS stylesheets.
