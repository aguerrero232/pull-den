import yt_dlp
import os
from google.cloud import storage
from hurry.filesize import size, si, iec
from timeit import default_timer as timer
def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    try:
      if request.args and 'link' in request.args:
        print("Recieved: "+request.args.get('link'))
        storclient=storage.Client('cs4843-youtube-dl')
        bucket=storclient.get_bucket('test-youtube-videos')
        ydl_opts={
          'outtmpl':'/tmp/%(id)s.%(ext)s',
          #'format':'mp4'
          #'outtmpl':'/tmp/%(id)s.mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
          yinfo=ytdl.extract_info(request.args.get('link'),download=False)
          blob=bucket.blob(yinfo['id'])
          if blob.exists():
            print("Blob already exists: "+request.args.get('link'))
          else:
            if yinfo['filesize_approx'] < (1024**3)*4:
              print("File doesn't exist, downloading: "+request.args.get('link'))
              yinfo=ytdl.extract_info(request.args.get('link'))
              print("Download finished from YouTube, "+yinfo['id']+"."+yinfo['ext']+" file size is "+str(os.path.getsize("/tmp/"+yinfo['id']+"."+yinfo['ext']))+" bytes or "+size(os.path.getsize("/tmp/"+yinfo['id']+"."+yinfo['ext']),system=iec))
              start=timer()
              blob.upload_from_filename("/tmp/"+yinfo['id']+"."+yinfo['ext'])
              end=timer()
              print("Uploaded "+yinfo['id']+"."+yinfo['ext']+", ("+str(os.path.getsize("/tmp/"+yinfo['id']+"."+yinfo['ext']))+" bytes or "+size(os.path.getsize("/tmp/"+yinfo['id']+"."+yinfo['ext']),system=iec)+") to GCS in "+str(end-start)+" seconds")
            else:
              return "Expected file size is too large, 4GiB or smaller, the expected file size is: "+str(yinfo['filesize_approx'])+" bytes ("+size(yinfo['filesize_approx'],system=iec)+")"
          print(blob.public_url)
          return blob.public_url
      else:
        #print("Failed to parse: "+request.args.get('link'))
        return "please provide 'link' argument"
    except BaseException as e:
      return str(e)
          