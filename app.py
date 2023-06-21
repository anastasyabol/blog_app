from flask import Flask, render_template, request, url_for, redirect
import json

app = Flask(__name__)

pathfile = 'posts_data.json'

class JsonStorage:
    def __init__(self, pathfile):
        self.pathfile = pathfile
        with open(self.pathfile, "r") as handle:
            self.blog_posts = json.load(handle)

    def add(self, new_post):
        self.blog_posts.append(new_post)
        self.update_json_file()

    def update_json_file(self):
        with open(self.pathfile, "w") as handle:
            json.dump(self.blog_posts, handle)

    def get_last_id(self):
        return self.blog_posts[-1]['id']


    def delete_post(self, post_id):
        self.blog_posts = list(filter(lambda x: (x['id'] != post_id), self.blog_posts))
        self.update_json_file()


    def update_blogpost_post(self, post_id, upd_post):
        update = list(filter(lambda x: x['id'] == post_id, self.blog_posts))
        update_index = self.blog_posts.index(update[0])
        if len(update) == 0:
            # Post not found
            return False
        id, author, title, content = update[0]['id'], update[0]['author'], update[0]['title'], update[0]['content']
        update[0]['title'] = upd_post[0]
        update[0]['author'] = upd_post[1]
        update[0]['content'] = upd_post[2]
        self.blog_posts[update_index] = update[0]
        self.update_json_file()

    def update_blogpost_get(self, post_id):
        update = list(filter(lambda x: x['id'] == post_id, self.blog_posts))
        title_before = update[0]['title']
        author_before = update[0]['author']
        content_before = update[0]['content']
        return title_before, author_before, content_before


app_storage = JsonStorage(pathfile)
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', posts=app_storage.blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
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
    app_storage.delete_post(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    if request.method == 'POST':
        upd_title = request.form['title']
        upd_author = request.form['author']
        upd_content = request.form['content']
        upd_post = [upd_title, upd_author, upd_content]
        if app_storage.update_blogpost_post(post_id, upd_post) == False:
            return "Post not found", 404
        else:
            app_storage.update_blogpost_post(post_id, upd_post)
            return redirect(url_for('index'))
    title, author, content = app_storage.update_blogpost_get(post_id)
    return render_template('update.html', post_id=post_id, title=title, author=author, content=content)


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(debug=True)
