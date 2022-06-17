from App import app, db
from flask import jsonify, request,json
from App.models import directeur, employee,projet, task
from App import bcrypt
import jwt


jwt_secret_key = "ahmed"
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
    
    try:
        findByEmail =  employee.query.filter_by(email_adress = email).first()
        if findByEmail == None:
            return jsonResponse({"error":"email Not Found!","password":False,"email":True},401) #UNAUTHORIZED RESPONSE
        #verify password
        verifyPassword = bcrypt.check_password_hash(findByEmail.password_hash,password)
        if verifyPassword == False:
         return jsonResponse({"error":"password incorrect!","password":True,"email":False},401)  

        #return jwt in json response and GG WP
        projetOfEmployee = projet.query.filter_by(id = findByEmail.projet_id).first()
        bossOfEmployee = directeur.query.filter_by(id = projetOfEmployee.direct_id).first()
        payload = {
            "firstName":findByEmail.firstName,
            "lastName":findByEmail.lastName,
            "phone":findByEmail.phone,
            "email":findByEmail.email_adress,
            # "projet_id":findByEmail.projet_id,
            # "projet_title":projetOfEmployee.projet_title,
            # "projet_description":projetOfEmployee.projet_description
            "poste":findByEmail.poste,        
            }
        #Generate jwt
        token = jwt.encode(payload=payload,key=jwt_secret_key,algorithm="HS256")
        ResponseJson = {
            "projet_id":findByEmail.projet_id,
            "projet_title":projetOfEmployee.projet_title,
            "projet_description":projetOfEmployee.projet_description,
            "projet_boss_firstName":bossOfEmployee.firstName,
            "projet_boss_lastName":bossOfEmployee.lastName,
            "projet_boss_id":bossOfEmployee.id,
            "Tasks":[ obj.toJson() for obj in findByEmail.Tasks],
            "token":token
        }

        return jsonResponse(ResponseJson,200)

    except Exception as e:
        return jsonResponse({"error":str(e)},500) #in case of exception 



@app.route('/api/edit',methods=['POST'])
def changeStatus():
    body = request.get_json()
    auth_header = request.headers.get('Authorization')
    try:
        if auth_header:
            auth_token = auth_header.split(" ")[1] 
            tokenSignature = jwt.decode(jwt=auth_token,key=jwt_secret_key,algorithms=["HS256"])
            if tokenSignature == False:
                return jsonResponse({"error":"not authorized"},401)
            idTask = body["id"]
            taskFound = task.query.filter_by(id = int(idTask)).first()
            taskFound.status = 1 if taskFound.status == 0 else 0
            db.session.commit()
            return jsonResponse({"success":True},200)
        else:
            return jsonResponse({"error","there is no token"},401)

    except Exception as e:
        return jsonResponse({"error":str(e)},400) 

