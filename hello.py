from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return render_template('hello.html', message='Hello World!')

@app.route('/example')
def example_route():
    return '<h1>This is an example route</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

