from google.cloud import firestore

projectid = "cs4843-youtube-dl"
db = firestore.Client(projectid)

def entryPoint(request):
  if request.method == 'OPTIONS':
    headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '3600'
    }
    return ('', 204, headers)
  headers = {
    'Access-Control-Allow-Origin': '*'
  }
  request_json = request.get_json()
  try:
    if 'id' in request_json:
      doc_ref = db.collection("VIDEO").document(request_json['id']) #open video table
      data = doc_ref.get().to_dict() #get this document 
      return ({"video_data": data}, 200, headers)

    else:
      return("Error: No Video ID provided", 400, headers)

  except BaseException as e:
    return ("Exception:" + str(e.with_traceback()), 500, headers)