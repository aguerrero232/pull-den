from google.cloud import firestore,pubsub_v1,bigquery
import yt_dlp
projectid="cs4843-youtube-dl"
datasetid="PullDenAnalytics"
topic="startDownload"
tableid="videos"
db=firestore.Client(projectid)
bq=bigquery.Client(projectid)
publish=pubsub_v1.PublisherClient()
def entryPoint(request):
  #https://brianli.com/how-to-enable-cors-for-a-google-cloud-function-using-http-invocation/
  if request.method == 'OPTIONS':
      ## Allows GET requests from any origin with the Content-Type
    headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '3600'
    }
    return ('', 204, headers)

  ## Set CORS headers for the main request
  headers = {
    'Access-Control-Allow-Origin': '*'
  }
  request_json = request.get_json()
  try:
    print(request)
    print(request_json)
    if request and 'id' in request_json:
      doc_ref = db.collection("OWNERSHIP").document(request_json['id']) #open ownership table
      doc = doc_ref.get() #get this document
      if not doc.exists: #if this document does not exist, create it before working on it
        doc_ref.set({
                "rootUserID":request_json['id'], #this is the user who owns this now, whether we have it or not
                "videos":list() #set the local variable to be pushed to the firestore database
            })
        doc=doc_ref.get()
      data = doc.to_dict()
      for key, value in data.items():
        if key == 'videos': #find the videos array
          videoList = value #set to local variable
          if request_json['vidID'] not in videoList: #this video is not owned by the user
            vid_ref = db.collection("VIDEO").document(request_json['vidID']) #open video table
            vidDoc = vid_ref.get() #get this document
            if not vidDoc.exists: #if this video doesn't actually exist (it is not downloaded)
              with yt_dlp.YoutubeDL() as ytdl: #grab basic information about the video itself
                yinfo=ytdl.extract_info(request_json['vidID'],download=False) #use yt-dlp to grab more info quickly
                vid_ref.set({
                  "vidID":request_json['vidID'],
                  "title":yinfo['title'],
                  "channelID":yinfo['channel_id']
                })
                job=bq.query(f"""
                INSERT INTO 
                `{projectid}.{datasetid}.{tableid}`
                (vidID,channelID,startedDownload,shareCount,userDownloaded)
                VALUES
                ("{request_json['vidID']}","{yinfo['channel_id']}",CURRENT_DATETIME(),0,"{request_json['id']}")
                """)
                job.result()
              #Publish to topic
              tpath=publish.topic_path(projectid,topic)
              data_str=str(request_json['vidID']).encode("utf-8")
              future=publish.publish(tpath,data_str)
              print(future.result())
            #done if the video exists or not regardless
            videoList.append(request_json['vidID']) #add this video to the local variable of the video list
            doc_ref.set({
                "rootUserID":request_json['id'], #this is the user who owns this now, whether we have it or not
                "videos":videoList #set the local variable to be pushed to the firestore database
            })
          else: 
            return "This user already owns this video"
      return ("Function completed",200,headers)
    else:
      return ("Failed if statement",500,headers)
  except BaseException as e:
    tb=sys.exc_info()[2]
    print("Exception hit:"+str(e.with_traceback()))
    return (str(e.with_traceback()),500,headers)