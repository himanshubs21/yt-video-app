from flask import Flask, render_template, request, send_file
import yt_dlp
import pandas as pd

app = Flask(__name__)

def get_video_details(video_urls):
    # (Same code you shared earlier)
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = request.form['urls'].split(',')
        urls = [url.strip() for url in urls]
        video_details = get_video_details(urls)
        file_name = "video_details.xlsx"
        save_to_excel(video_details, file_name)
        return send_file(file_name, as_attachment=True)
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
