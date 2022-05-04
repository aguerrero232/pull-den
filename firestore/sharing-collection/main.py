from google.cloud import firestore,bigquery
import random
import string
projectid="cs4843-youtube-dl"
collectionid="SHARING"
datasetid="PullDenAnalytics"
tableid="videos"
db=firestore.Client(projectid)
bq=bigquery.Client(projectid)
def entryPoint(request): 

  request_json = request.get_json()
  try:
    showThumb = True
    showSubs = True
    showDesc = True 

    while True: 
      sharableLink = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=15))
      share_ref = db.collection(collectionid).document(sharableLink)
      doc = share_ref.get()
      if not doc.exists:
        break

    if request and 'id' in request_json and 'vidID' in request_json: 
      share_ref.set({
        "rootUserID":request_json['id'],
        "vidID":request_json['vidID'],
        "sharableLink":sharableLink,
        "permission":{
          "showThumb":showThumb,
          "showSubs":showSubs,
          "showDesc":showDesc
        }    
      }, merge=True)
      print( "Added to SHARING collection")
      job=bq.query(f"""UPDATE 
      `{projectid}.{datasetid}.{tableid}`
      SET shareCount = shareCount + 1
      WHERE vidID = "{request_json['vidID']}"
      """)
      job.result()
      return sharableLink
    else:
      return "Failed if statement"
    
  except BaseException as e:
    return str(e)
