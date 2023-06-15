from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        return render_template('index.html', title='Home', name=request.args['name'])
    except:
        return render_template('index.html', title='Home', name='Username')


@app.route('/form')
def form():
    return render_template('form.html')


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5000)
