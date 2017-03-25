import flask

app = flask.Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return 'Hellow world'

if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run(debug=True)
