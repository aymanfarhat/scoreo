from scoreo import app


@app.route('/')
def index():
    return 'Hellow world'
