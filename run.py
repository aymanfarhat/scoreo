from scoreo import app


@app.cli.command('initdb')
def initdb_command():
    print('wtf')
    print('this is a test')

#if __name__ == '__main__':
#    import uuid
#    app.secret_key = str(uuid.uuid4())
#    app.debug = False
#    app.run(debug=True)
