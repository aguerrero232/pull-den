import base64
from google.cloud import storage,bigquery,firestore
import yt_dlp
import urllib.request
from PIL import Image
from timeit import default_timer as timer
import mimetypes
import os
projectid="cs4843-youtube-dl"
collectionid="VIDEO"
bucketid='md-thumbnail'
datasetid="PullDenAnalytics"
tableid="storage"
def md_thumbnail_dl(event, context):
     """Triggered from a message on a Cloud Pub/Sub topic.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """
     try:
          pubsub_message = base64.b64decode(event['data']).decode('utf-8')

          # right now the function expects a url, can change to video id in the future
          vid_url = pubsub_message
          bq=bigquery.Client(projectid)
          db=firestore.Client(projectid)
          ydl_opts={
                    'outtmpl':'/tmp/%(id)s.%(ext)s'
               }
          start=timer()
          with yt_dlp.YoutubeDL(ydl_opts) as ytdlp:
                    vid_info = ytdlp.extract_info(vid_url, download=False)
          
          vid_id = vid_info['id']
          vid_ext = vid_info['ext']
               
          thumbnail_filename = f'/tmp/{vid_id}.{vid_ext}'
          thumbnail_png_version = f'/tmp/{vid_id}.png'

          urllib.request.urlretrieve(vid_info['thumbnail'], thumbnail_filename)

          image = Image.open(thumbnail_filename).convert('RGB')
          image.save(thumbnail_png_version, 'png')

          storage_client = storage.Client(projectid)
          bucket = storage_client.get_bucket(bucketid)
          blob = bucket.blob(vid_id)
          blob.upload_from_filename(thumbnail_png_version)
          end=timer()
          doc_ref=db.collection(collectionid).document(vid_id)
          doc_ref.set({
               "GCSThumbnail":blob.public_url
          },merge=True)
          job=bq.query(f"""
          INSERT INTO 
          `{projectid}.{datasetid}.{tableid}`
          (vidID,itemType,timeNeeded,completed,mimeType,byteSize)
          VALUES
          ("{vid_id}","thumbnail",{int(end-start)},CURRENT_DATETIME(),"{mimetypes.guess_type(thumbnail_filename)}",{os.path.getsize(thumbnail_filename)})
          """)
          job.result()
          os.remove(thumbnail_filename)

     except BaseException as e:
          print(e)
          return -1
