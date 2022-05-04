from google.cloud import firestore
projectid="cs4843-youtube-dl"
db=firestore.Client(projectid)

def entryPoint(request):
  request_json = request.get_json()
  try:
    if request and 'id' in request_json:
      doc_ref = db.collection("OWNERSHIP").document(request_json['id'])
      doc = doc_ref.get()
      if doc.exists:
        data = doc.to_dict()
        for key, value in data.items():
          if key == 'videos':
            videoList = value
            if request_json['vidID'] not in videoList:
              vid_ref = db.collection("VIDEOS").document(request_json['vidID'])
              vidDoc = vid_ref.get()
              if not vidDoc.exists:
                video_ref.set({
                  "vidID":request_json['vidID'],
                  "title":request_json['title'],
                  "channelID":request_json['channelID'],
                  "GCSVideo":request_json['GCSVideo']
                })
              videoList.append(request_json['vidID'])
              doc.set({
                  "rootUserID":request_json['id'],
                  "Videos":videoList
              })
      return "Added to Ownership collection"
    else:
      return "Failed if statement"

  except BaseException as e:
    return str(e)