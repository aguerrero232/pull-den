import yt_dlp
import os
from google.cloud import storage,bigquery,firestore
from hurry.filesize import size, si, iec
from timeit import default_timer as timer
import base64
import mimetypes

projectid="cs4843-youtube-dl"
collectionid="VIDEO"
bucketid='downloaded-videos'
datasetid="PullDenAnalytics"
tableid="storage"

def download_video(event, context):

    try:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        vid_url = pubsub_message
        bq=bigquery.Client(projectid)
        db=firestore.Client(projectid)
        storclient=storage.Client(projectid)
        bucket=storclient.get_bucket(bucketid)
        ydl_opts={
        'outtmpl':'/tmp/%(id)s.%(ext)s',
        }
        start=timer()
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
            yinfo=ytdl.extract_info(vid_url,download=False)
            blob=bucket.blob(yinfo['id'])
            vid_id = yinfo['id']
            if blob.exists():
                print("Blob already exists: "+vid_url)
            else:
                if yinfo['filesize_approx'] < (1024**3)*4:
                    print("File doesn't exist, downloading: "+vid_url)
                    yinfo=ytdl.extract_info(vid_url)
                    print("Download finished from YouTube, "+yinfo['id']+"."+yinfo['ext']+" file size is "+str(os.path.getsize("/tmp/"+yinfo['id']+"."+yinfo['ext']))+" bytes or "+size(os.path.getsize("/tmp/"+yinfo['id']+"."+yinfo['ext']),system=iec))
                    
                    blob.upload_from_filename("/tmp/"+yinfo['id']+"."+yinfo['ext'])
                    end=timer()
                    print("Downloaded and Uploaded "+yinfo['id']+"."+yinfo['ext']+", ("+str(os.path.getsize("/tmp/"+yinfo['id']+"."+yinfo['ext']))+" bytes or "+size(os.path.getsize("/tmp/"+yinfo['id']+"."+yinfo['ext']),system=iec)+") to GCS in "+str(end-start)+" seconds")
                else:
                    print("Expected file size is too large, 4GiB or smaller, the expected file size is: "+str(yinfo['filesize_approx'])+" bytes ("+size(yinfo['filesize_approx'],system=iec)+")")
                    return
            print(blob.public_url)
            doc_ref=db.collection(collectionid).document(vid_id)
            doc_ref.set({
                "GCSVideo":blob.public_url
            },merge=True)
            job=bq.query(f"""
            INSERT INTO 
            `{projectid}.{datasetid}.{tableid}`
            (vidID,itemType,timeNeeded,completed,mimeType,byteSize)
            VALUES
            ("{vid_id}","video",{int(end-start)},CURRENT_DATETIME(),"{mimetypes.guess_type("/tmp/"+yinfo['id']+"."+yinfo['ext'])}",{os.path.getsize("/tmp/"+yinfo['id']+"."+yinfo['ext'])})
            """)
            job.result()
            os.remove("/tmp/"+yinfo['id']+"."+yinfo['ext'])
            return

    except BaseException as e:
      print(e)
      return -1
