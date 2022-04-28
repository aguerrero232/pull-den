import base64
from google.cloud import storage
import yt_dlp

def md_description_dl(event, context):
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
               'outtmpl':'/tmp/%(id)s.%(ext)s'
          }

     with yt_dlp.YoutubeDL(ydl_opts) as ytdlp:
          vid_info = ytdlp.extract_info(vid_url, download=False)
          vid_id = vid_info['id']

     description_filename = f'/tmp/{vid_id}.txt'

     with open(description_filename, 'w') as description_file:
          description_file.write(vid_info['description'])

     storage_client = storage.Client('cs4843-youtube-dl')
     bucket = storage_client.get_bucket('md-description')
     blob = bucket.blob(vid_id)
     blob.upload_from_filename(description_filename)

