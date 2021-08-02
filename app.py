from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

courses = [
    {'id': 0,
     'title': 'CS106',
    },
    {'id': 1,
     'title': 'CS110',
    },
    {'id': 2,
     'title': 'CS321',
    }
]


@app.route('/courses', methods=['GET'])
def list():
    return jsonify({'courses': courses})


#this functions is also list but with id cuz we need when we do GET after editing the data in PUT
@app.route('/courses/<int:course_id>', methods=['GET'])
def list_id(course_id): #NOTE: course_id need to be passed to the func here
    course = [course for course in courses if course['id'] == course_id]
    return jsonify({'courses': course[0]})
    


@app.route('/courses', methods=['POST'])
def add():
    course = {'id': courses[-1]['id']+1,
              'title': request.json['title']   
             }
    courses.append(course)
    return jsonify({'courses': courses}), 201       #201=request succeeded  


@app.route('/courses/<int:course_id>', methods=['PUT'])
def edit(course_id):     #NOTE: course_id need to be passed to the func here
    course = [course for course in courses if course['id'] == course_id]      #searching for the course with the course_id passed and store it in var to be able to edit it
    course[0]['title'] = request.json.get('title', course[0]['title'])    
    return jsonify({'courses': course[0]})
    #return jsonify({'courses': courses}) #do this if you want to return it all

@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete(course_id):     #NOTE: course_id need to be passed to the func here
    course = [course for course in courses if course['id'] == course_id]      
    courses.remove(course[0])    
    #return jsonify({'courses': course[0]})
    return jsonify({'courses': 'Deleted Successfully!'}) #do this if you want to return it all