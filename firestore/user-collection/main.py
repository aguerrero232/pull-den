from google.cloud import firestore,bigquery
projectid="cs4843-youtube-dl"
collectionid="USERS"
datasetid="PullDenAnalytics"
tableid="user"
import sys
db=firestore.Client(projectid)
bq=bigquery.Client(projectid)
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
    if request and 'id' in request_json:
      print(request)
      print(request_json)
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
      return (request_json['id'],200,headers)
    else:
      return ("Failed if statement",500,headers)
    
  except BaseException as e:
    tb=sys.exc_info()[2]
    print("Exception hit: "+str(e.with_traceback(tb)))
    return (str(e.with_traceback(tb)),500,headers)
