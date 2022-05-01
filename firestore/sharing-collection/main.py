from google.cloud import firestore
import random
import string

db=firestore.Client("cs4843-youtube-dl")
def entryPoint(request): 

  request_json = request.get_json()
  try:
    showThumb = True
    showSubs = True
    showDesc = True 

    while True: 
      sharableLink = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=15))
      share_ref = db.collection("SHARING").document(sharableLink)
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
      return "Added to SHARING collection"
    else:
      return "Failed if statement"
    
  except BaseException as e:
    return str(e)
