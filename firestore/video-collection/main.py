from google.cloud import firestore
from google.cloud import pubsub_v1
subscriber = pubsub_v1.SubscriberClient();
db=firestore.Client("cs4843-youtube-dl")
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
      return "Added Video Details to Firstore"
    else:
      return "Failed if statement"
    
    
  except BaseException as e:
    return str(e)