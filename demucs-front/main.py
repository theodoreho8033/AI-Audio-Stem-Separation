from flask import Flask, render_template, request
import requests
import io
app = Flask(__name__)


@app.route("/")
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
   

    return render_template("index.html")

@app.route("/upload", methods = ["POST"])
def upload():
    file = request.files['file']
    files = {'file': (file.filename, file.stream, file.content_type)}
    r = requests.post('https://demucsproxy4gb1cpu-wfccdzqdja-uw.a.run.app/upload', files =files)
    print(r.status_code)
    return r.content
if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)