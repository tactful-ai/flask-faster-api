from flask import Flask
from flask.scaffold import F
import jwt
import json
from flask import request, jsonify
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrectKey'

#Authorization: Bearer <access_token>

def login_required(f):
    @wraps(f)
    def authenticate_user(*args, **kwargs):
        
        auth = request.headers.get('Authorization')
        if(not auth):
            return jsonify({'message' : 'Token is missing!'}), 403
        authMethod = auth.split(' ')
        if(authMethod[0] != 'Bearer' or len(authMethod)!=2):
            return jsonify({'message' : 'Authorization must be in this format Bearer <access_token>'}), 403
        try:
            data = jwt.decode(authMethod[1].replace("'"," "), app.config['SECRET_KEY'])
        except Exception as e:
            print(e)
            return jsonify({'message' : 'Token is invalid or expired!'}), 403
        return f(data,*args, **kwargs)
    return authenticate_user





@app.route('/login' , methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if(username!='test' or password!='test'):
        return jsonify({'message':'Invalid username or password'})
    try:
        token = jwt.encode(
                {
                'user':username ,
                'iat':datetime.datetime.utcnow(),
                'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
                },
                app.config['SECRET_KEY'],
                )
        return jsonify({'token':token.decode('utf-8')})
    except Exception as e:
        print(e)
        return jsonify({'message':'error occured'})




@app.route('/course' , methods=['GET'])
def getCourses():
    f = open('courses.json')
    courses = json.load(f)
    return jsonify({'Courses':courses})  ## converts a Python object into a json string


@app.route('/course', methods=['POST'])
@login_required
def addCourse(data):
    course = request.get_json()
    keyslist = course.keys()
    if(len(keyslist)<4):
        return jsonify({'error':'Missing info make sure that you entered id , name , duration , teacherslist'})
    keys = course.keys()
    listofKeys = ['id','name','duration','teacherslist','studentsNum']
    for key in keys:
        if (key == 'studentsNum'):
            course[key] = int(course[key])
        if(key not in listofKeys):
            return jsonify({'error':key +' not a valid key  make sure that you entered id , name , duration , teacherslist'})
    f = open('courses.json','r+')
    courses = json.load(f)
    exist = False
    for item in courses['Courses']:
        if (item["id"] == course["id"]):
            exist =True;
            break;
    if(not exist):
        courses['Courses'].append(course)  
        f.seek(0)     #moving pointer to the beginning of the file
        f.truncate()   #remove the content of the file
        f.write(json.dumps(courses))
        return jsonify({'Courses':courses['Courses']})
    else:
        return jsonify({'error':'There is a course with same ID'})


@app.route('/course/<id>', methods=['PUT'])
@login_required
def editCourse(data,id):
    data = request.json
    f = open('courses.json','r+')
    done = False
    courses = json.load(f)
    keys = data.keys()
    listofKeys = ['name','duration','teacherslist','studentsNum']
    for key in keys:
        if(key not in listofKeys):
            return jsonify({'error':key +' not a valid key  make sure that you entered id , name , duration , teacherslist'})
    for course in courses['Courses']:
        if (course["id"] == id):
            for singlekey in keys:
                if (singlekey == 'studentsNum'):
                    data[singlekey] = int(data[singlekey])
                course[singlekey] = data[singlekey]
            done = True
            break
    if(done):
        f.seek(0)     #moving pointer to the beginning of the file
        f.truncate()   #remove the content of the file
        f.write(json.dumps(courses))
        return jsonify({'Courses':courses['Courses']})
    else:
         return jsonify({'error':'Course not found'})

    
@app.route('/course/<id>' , methods=['DELETE'])
@login_required
def deleteCourse(data,id):
    f = open('courses.json','r+')
    courses = json.load(f)
    done = False
    i=0
    for course in courses['Courses']:
        if (course["id"] == id):
            courses['Courses'].pop(i)
            done = True
            break
        i+=1
    if(done):
        f.seek(0)     #moving pointer to the beginning of the file
        f.truncate()   #remove the content of the file
        f.write(json.dumps(courses))
        return jsonify({'Courses':courses['Courses']})
    else:
         return jsonify({'error':'Course not found'})



@app.route('/filterby',methods=['GET'])
@login_required
def filterby(data):
    query = request.args
    querydict = query.to_dict(flat=False)
    keys = querydict.keys()
    listofKeys = ['name','duration','teacherslist']
    foundcourses = []
    for key in keys:
        if(key == 'teacherslist'):
            querydict['teacherslist'][0] = querydict['teacherslist'][0].split(',')
        if(key not in listofKeys):
            return jsonify({'error':key +' not a valid key'})
    f = open('courses.json','r+')
    courses = json.load(f)
    for course in courses['Courses']:
        found = True
        for singlekey in keys:
            if (course[singlekey]!=querydict[singlekey][0]):
                found = False
                break
        if(found):
            foundcourses.append(course)
           
    if(len(foundcourses)==0):
        return jsonify({'message':'No matching courses'})
    else:
        return jsonify({'courses':foundcourses})


@app.route('/enroll/<id>',methods=['POST'])
@login_required
def enroll(data,id):
    f = open('courses.json','r+')
    username = data['user']
    courses = json.load(f)
    for course in courses['Courses']:
        if (course["id"] == id):
            course["studentsNum"] +=1
            f.seek(0)     #moving pointer to the beginning of the file
            f.truncate()   #remove the content of the file
            f.write(json.dumps(courses))
            return jsonify({'message':username+" enrolled in "+course["name"]})
    return jsonify({'message':'Course not found'})
    

if __name__ == "__main__":
    app.run()