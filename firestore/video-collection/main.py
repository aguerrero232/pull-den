from google.cloud import firestore,pubsub_v1,bigquery
subscriber = pubsub_v1.SubscriberClient();
projectid="cs4843-youtube-dl"
collectionid="SHARING"
datasetid="PullDenAnalytics"
tableid="videos"
db=firestore.Client(projectid)
bq=bigquery.Client(projectid)
def entryPoint(request): 
  request_json = request.get_json()
  try:
    if request and 'vidID' in request_json:
      video_ref = db.collection("VIDEO").document(request_json['vidID'])
      video_ref.set({
        "vidID":request_json['vidID'],
        "title":request_json['title'],
        "channelID":request_json['channelID'],
        "GCSVideo":request_json['GCSVideo']
      }, merge=True)
      #return "Added Video Details to Firstore"
      job=bq.query(f"""
      INSERT INTO 
      `{projectid}.{datasetid}.{tableid}`
      (vidID,channelID,startedDownload,shareCount,userDownloaded)
      VALUES
      ("{request_json['vidID']}","{request_json['channelID']}",0,"{request_json['userID']}")
      """)
      job.result()
      return "Added Video Details to Firstore"
    else:
      return "Failed if statement"
    
    
  except BaseException as e:
    return str(e)

