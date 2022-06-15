from App import app, db
from flask import jsonify, request,json

#Return response
def jsonResponse(jsonRes,responseCode):
    return app.response_class(
        response=json.dumps(jsonRes),
        status = responseCode,
        mimetype='application/json'
    )


@app.route('/api/login',methods=['POST'])
def loginEmployee():
    body = request.get_json()
    try:
        email = body["email"]
        password = body["password"]
    except:
        return jsonResponse({"error":"missing body"},400)

    return 'h'

