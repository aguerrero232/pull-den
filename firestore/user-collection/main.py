from google.cloud import firestore
db=firestore.Client("cs4843-youtube-dl")
def entryPoint(request): 
  request_json = request.get_json()
  try:
    if request and 'id' in request_json:
      user_ref = db.collection("USERS").document(request_json['id'])
      user_ref.set({
        "OAUTH":request_json['id']
      })
      return request_json['id']
    else:
      return "Failed if statement"
    return request_json['id']
    
  except BaseException as e:
    return str(e)