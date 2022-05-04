from google.cloud import firestore,pubsub_v1
projectid="cs4843-youtube-dl"
topic="startDownload"
db=firestore.Client(projectid)
publish=pubsub_v1.PublisherClient()
def entryPoint(request):
  request_json = request.get_json()
  try:
    if request and 'id' in request_json:
      doc_ref = db.collection("OWNERSHIP").document(request_json['id']) #open ownership table
      doc = doc_ref.get() #get this document
      if doc.exists: #if this document actually exists (the user has a ownership document)
        data = doc.to_dict()
        for key, value in data.items():
          if key == 'videos': #find the videos array
            videoList = value #set to local variable
            if request_json['vidID'] not in videoList: #this video is not owned by the user
              vid_ref = db.collection("VIDEOS").document(request_json['vidID']) #open video table
              vidDoc = vid_ref.get() #get this document
              if not vidDoc.exists: #if this video doesn't actually exist (it is not downloaded)
                vid_ref.set({
                  "vidID":request_json['vidID'],
                  "title":request_json['title'],
                  "channelID":request_json['channelID'],
                  "GCSVideo":request_json['GCSVideo']
                })
                #Publish to topic
                tpath=publish.topic_path(projectid,topic)
                data_str=str(request_json['vidID']).encode("utf-8")
                future=publish.publish(tpath,data_str)
                print(future.result())
              #done if the video exists or not regardless
              videoList.append(request_json['vidID']) #add this video to the local variable of the video list
              doc.set({
                  "rootUserID":request_json['id'], #this is the user who owns this now, whether we have it or not
                  "videos":videoList #set the local variable to be pushed to the firestore database
              })
            else: 
              return "This user already owns this document"
      return "Function completed"
    else:
      return "Failed if statement"

  except BaseException as e:
    return str(e)