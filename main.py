from flask import Flask, request, render_template, jsonify
import requests
import os
import json
import mysql.connector

db_config = {
    "host": "139.144.36.136",
    "user": "thundkad_pv",
    "password": "Pranavkd44#",
    "database": "thundkad_pv"
}

app = Flask(__name__,template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    if request.method == 'POST':
        file = request.files['file']
        video_id = request.form['video_id']
        if file:
            headers = {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGMwQzI0MTY2NTM4ZDg3MjI0ZDQ1YjU5RjI4NzExNTk2RTQ5NjEzNzUiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2OTc3ODY4NzQ2NzIsIm5hbWUiOiJ3ZWIzIn0.0kkTUd5tRhI8Khi8TEkE4OXyGGVY1zfHQzDqNIJigaw",
                "Content-Type": file.content_type,
                "Content-Disposition": f'attachment; filename="{file.filename}"'
            }
            response = requests.post('https://api.web3.storage/upload', headers=headers, data=file)
            if response.status_code == 200:
                responcc = response.text
                responcc = json.loads(responcc)
                cid = responcc['cid']
                file_url = f'https://{cid}.ipfs.dweb.link'
                cursor.execute("UPDATE qa_posts SET content = %s WHERE qa_posts.postid = %s", (file_url, video_id))
                connection.commit()
                return render_template('upload.html', cid=file_url)
    return render_template('upload.html')

@app.route('/video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        video_file = request.files['file']
        text_file = request.files['file1']
        if video_file and text_file:
            headers = {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGMwQzI0MTY2NTM4ZDg3MjI0ZDQ1YjU5RjI4NzExNTk2RTQ5NjEzNzUiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2OTc3ODY4NzQ2NzIsIm5hbWUiOiJ3ZWIzIn0.0kkTUd5tRhI8Khi8TEkE4OXyGGVY1zfHQzDqNIJigaw",
                "Content-Type": "multipart/form-data"
            }
            files = {
                'video.mp4': (video_file.filename, video_file, video_file.content_type),
            }
            response = requests.post('https://api.web3.storage/upload', headers=headers, files=files)
            if response.status_code == 200:
                responcc = response.text
                responcc = json.loads(responcc)
                cid = responcc['cid']
                file_url = f'https://{cid}.ipfs.dweb.link'
                return render_template('uploadvd.html', cid=file_url)
    return render_template('uploadvd.html')


if __name__ == '__main__':
    app.run(debug=True)
