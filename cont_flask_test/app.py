from flask import Flask, request
import yt_dlp
from google.cloud import storage
import base64
# import os

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cs4843-youtube-dl-aa8095ad1501.json'
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        json = request.get_json()
        # print(base64.b64decode(json["message"]["data"]).decode('utf-8'))
        url = base64.b64decode(json["message"]["data"]).decode('utf-8')

        ytdlp_opts = { 'outtmpl':'/tmp/%(id)s.%(ext)s' }
        try:
            with yt_dlp.YoutubeDL(ytdlp_opts) as ytdl:
                yinfo = ytdl.extract_info(url)
            vid_id = yinfo['id']
            vid_ext = yinfo['ext']
            storage_client = storage.Client('cs4843-youtube-dl')
            bucket = storage_client.get_bucket('test-youtube-videos')
            blob = bucket.blob(vid_id)
            blob.upload_from_filename(f'/tmp/{vid_id}.{vid_ext}')
        except BaseException as e:
            print(e)
            exit(-1)

        # need to update database entry here to signify that the video download is completed

        return
    else:
        return ("Not a POST request, this app only accepts POST requests.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
