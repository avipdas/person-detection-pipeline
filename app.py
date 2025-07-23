from flask import Flask, render_template, send_from_directory
from dashboard import init_dashboard

app = Flask(__name__)
init_dashboard(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory('static/video', filename)

if __name__ == '__main__':
    app.run(debug=True)
