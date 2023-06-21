from flask import Flask, render_template, request, url_for, redirect
import json

app = Flask(__name__)

pathfile = 'posts_data.json'


class JsonStorage:
    """Creates a class with a json storage of blog posts. Init requires a pathfile.
    After class will use a list of dictionaries from json to do updates and updating the file after each change
    Structure: [{id: , author: , title: , content: }, {..}]"""

    def __init__(self, pathfile):
        self.update_id = None
        self.update_index = None
        self.pathfile = pathfile
        with open(self.pathfile, "r") as handle:
            self.blog_posts = json.load(handle)

    def get_blog_posts(self):
        """returns the self.blog_posts for future uses"""
        return self.blog_posts

    def add(self, new_post):
        """gets new_post from flask /add function with a new post and update the file"""
        self.blog_posts.append(new_post)
        self.update_json_file()

    def update_json_file(self):
        """method to update json file after each change"""
        with open(self.pathfile, "w") as handle:
            json.dump(self.blog_posts, handle)

    def get_last_id(self):
        """getting last id (last item in the list)"""
        return self.blog_posts[-1]['id']

    def delete_post(self, post_id):
        """gets post_id to delete. Deletes it from the self.blogposts and update the file"""
        self.blog_posts = list(filter(lambda x: (x['id'] != post_id), self.blog_posts))
        self.update_json_file()

    def post_exist(self, post_id):
        """In case of post_id no found returns False for (delete/update - will show page 404
        If exists returns index of item in the list"""
        post_to_check = list(filter(lambda x: x['id'] == post_id, self.blog_posts))
        post_index_in_list = self.blog_posts.index(post_to_check[0])
        if len(post_to_check) == 0:
            # Post not found
            return False
        else:
            return post_index_in_list

    def update_blogpost_post(self, post_id, upd_post):
        """gets post_id to update (for POST method), checks if it exists, and upd_post(list of 3 elements) with new data.
        Updates it in the self.blogposts and update the file"""
        self.update_id = self.post_exist(post_id)
        if not self.update_id:
            print(self.update_id)
        self.blog_posts[self.update_id]['title'] = upd_post[0]
        self.blog_posts[self.update_id]['author'] = upd_post[1]
        self.blog_posts[self.update_id]['content'] = upd_post[2]
        self.update_json_file()

    def update_blogpost_get(self, post_id):
        """gets post_id  (for GET method) shows data for post_id before the update (to show it on the webpage). """
        self.update_id = self.post_exist(post_id)
        if not self.update_id:
            return False
        else:
            title_before = self.blog_posts[self.update_id]['title']
            author_before = self.blog_posts[self.update_id]['author']
            content_before = self.blog_posts[self.update_id]['content']
            return title_before, author_before, content_before


# creating the storage object
app_storage = JsonStorage(pathfile)


@app.route('/', methods=['POST', 'GET'])
def index():
    """Creates index page, based on updates json-storage class"""
    return render_template('index.html', posts=app_storage.get_blog_posts())


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Creates add page (GET), after the form send data with POST updates object with method .add() with new_blog_post
    - data fetched from post method (new_title, new_author, new_content). Id created
    Redirects to updated index page (after new post added)"""
    if request.method == 'POST':
        new_title = request.form['title']
        new_author = request.form['author']
        new_content = request.form['content']
        new_id = app_storage.get_last_id() + 1
        new_blog_post = {"id": new_id, "author": new_author, "title": new_title, "content": new_content}
        app_storage.add(new_blog_post)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes post by post_id in the object and redirects for updated index page"""
    app_storage.delete_post(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Get method -  uses update_blogpost_get to get post info before the update and to sgow it on the update-page.
    Post - if update"""
    if not app_storage.post_exist(post_id):
        return "Post not found", 404
    if request.method == 'POST':
        upd_title = request.form['title']
        upd_author = request.form['author']
        upd_content = request.form['content']
        upd_post = [upd_title, upd_author, upd_content]
        app_storage.update_blogpost_post(post_id, upd_post)
        return redirect(url_for('index'))
    title, author, content = app_storage.update_blogpost_get(post_id)
    return render_template('update.html', post_id=post_id, title=title, author=author, content=content)


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(debug=True)
