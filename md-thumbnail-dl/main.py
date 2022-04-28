import base64
from google.cloud import storage
import yt_dlp
import urllib.request
from PIL import Image

def md_thumbnail_dl(event, context):
     """Triggered from a message on a Cloud Pub/Sub topic.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """
     pubsub_message = base64.b64decode(event['data']).decode('utf-8')
     print(pubsub_message)
     # right now the function expects a url, can change to video id in the future
     vid_url = pubsub_message

     ydl_opts={
               'outtmpl':'/tmp/%(id)s.%(ext)s',
               #'format':'mp4'
               #'outtmpl':'/tmp/%(id)s.mp4'
          }
     with yt_dlp.YoutubeDL(ydl_opts) as ytdlp:
          vid_info = ytdlp.extract_info(vid_url, download=False)
          vid_id = vid_info['id']
          vid_ext = vid_info['ext']
          
          thumbnail_filename = f'/tmp/{vid_id}.{vid_ext}'
          urllib.request.urlretrieve(vid_info['thumbnail'], thumbnail_filename)

     image = Image.open(thumbnail_filename).convert('RGB')
     thumbnail_jpg_version = f'/tmp/{vid_id}.jpg'
     image.save(thumbnail_jpg_version, 'jpeg')

     storage_client = storage.Client('cs4843-youtube-dl')
     bucket = storage_client.get_bucket('md-thumbnail')
     blob = bucket.blob(vid_id)
     blob.upload_from_filename(thumbnail_jpg_version)


