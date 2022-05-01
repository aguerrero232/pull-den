import os
import yt_dlp
from google.cloud import storage

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cs4843-youtube-dl-aa8095ad1501.json'

if os.environ['URL']:
	url = os.environ['URL']
else:
	print('No video URL provided to download. Exiting...')
	exit(-1)

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
