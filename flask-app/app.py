from flask import Flask, request, render_template, send_file
import yt_dlp
import pandas as pd
import os

app = Flask(__name__)

def get_video_details(video_urls):
    video_details = []
    for url in video_urls:
        try:
            ydl_opts = {'quiet': True, 'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_info = {
                    'Title': info_dict.get('title', '').upper(),
                    'URL': url,
                    'Uploader': info_dict.get('uploader', '').upper(),
                    'Duration (HH:MM:SS)': format_duration(info_dict.get('duration', 0)),
                    'Publish Year': extract_publish_year(info_dict.get('upload_date')).upper(),
                    'View Count': str(info_dict.get('view_count', '')).upper(),
                    'Uploader ID': info_dict.get('uploader_id', '').upper(),
                    'Description': info_dict.get('description', '').upper(),
                    'Like Count': str(info_dict.get('like_count', '')).upper(),
                    'Dislike Count': str(info_dict.get('dislike_count', '')).upper(),
                    'Published Date': info_dict.get('upload_date', '').upper()
                }
                video_details.append(video_info)
        except Exception as e:
            print(f"Error extracting {url}: {e}")
    return video_details

def format_duration(duration_seconds):
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def extract_publish_year(upload_date):
    if upload_date:
        return upload_date[:4]
    return None

def save_to_excel(video_details, file_name="video_details.xlsx"):
    df = pd.DataFrame(video_details)
    df.to_excel(file_name, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = request.form.get('urls')
        video_urls = [url.strip() for url in urls.split(',')]
        video_details = get_video_details(video_urls)
        file_name = "video_details.xlsx"
        save_to_excel(video_details, file_name)
        return send_file(file_name, as_attachment=True)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
