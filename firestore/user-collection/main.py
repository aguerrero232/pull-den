from google.cloud import firestore,bigquery
projectid="cs4843-youtube-dl"
collectionid="USERS"
datasetid="PullDenAnalytics"
tableid="user"
db=firestore.Client(projectid)
bq=bigquery.Client(projectid)
def entryPoint(request): 
  request_json = request.get_json()
  try:
    if request and 'id' in request_json:
      user_ref = db.collection(collectionid).document(request_json['id'])
      doc=user_ref.get()
      if not doc.exists:
        user_ref.set({
          "OAUTH":request_json['id'],
          "EMAIL":request_json['email']
        })
        job=bq.query(f"""
          INSERT INTO 
          `{projectid}.{datasetid}.{tableid}`
          (userID, dateJoined, videosOwned,email) 
          VALUES 
          ("{request_json['id']}",CURRENT_DATETIME(),0,"{request_json['email']}")
        """)
        job.result()
      return request_json['id']
    else:
      return "Failed if statement"
    
  except BaseException as e:
    return str(e)
