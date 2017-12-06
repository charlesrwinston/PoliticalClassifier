import logging

from flask import Flask, render_template, request

from classify import classify_text


app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return render_template('index.html', result=classify_text(request.form['fooput']))
    if request.method == 'GET':
        return render_template('index.html')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
