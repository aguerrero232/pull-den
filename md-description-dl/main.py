import base64
from google.cloud import storage, bigquery,firestore
from timeit import default_timer as timer
import yt_dlp
import mimetypes
import os
projectid="cs4843-youtube-dl"
bucketid='md-description'
collectionid="VIDEO"
datasetid="PullDenAnalytics"
tableid="storage"
def md_description_dl(event, context):
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

          description_filename = f'/tmp/{vid_id}.txt'

          with open(description_filename, 'w') as description_file:
               description_file.write(vid_info['description'])

          storage_client = storage.Client(projectid)
          bucket = storage_client.get_bucket(bucketid)
          blob = bucket.blob(vid_id)
          blob.upload_from_filename(description_filename)
          end=timer()
          doc_ref=db.collection(collectionid).document(vid_id)
          doc_ref.set({
               "GCSDescription":blob.public_url
          },merge=True)
          job=bq.query(f"""
          INSERT INTO 
          `{projectid}.{datasetid}.{tableid}`
          (vidID,itemType,timeNeeded,completed,mimeType,byteSize)
          VALUES
          ("{vid_id}","description",{int(end-start)},CURRENT_DATETIME(),"{mimetypes.guess_type(description_filename)}",{os.path.getsize(description_filename)})
          """)
          job.result()
          os.remove(description_filename)
          
     except BaseException as e:
          print(e)
          return -1
