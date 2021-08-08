from typing import Callable
from flask_restful import reqparse
import inspect
from fastapi import Query, Body, Cookie, Header, Path


def get_parser(signature, parameters) -> reqparse:
    parser = reqparse.RequestParser()
    location: str = 'args'  # default location -> 'args'

    for param in parameters.values():
        if param.name == "self":
            continue

        if str(param).find('Query') != -1:
            location = 'args'

        elif str(param).find('Body') != -1:
            location = 'form'

        elif str(param).find('Header') != -1:
            location = 'headers'

        elif str(param).find('Cookie') != -1:
            location = 'cookies'

        elif str(param).find('Path') != -1:
            continue

        # print("name : {}".format(param.name))
        # print("param : {}".format(param))
        # print("location : {}".format(location))
        # print("default : {}".format(param.default))
        # print("annotation : {}\n".format(parameters[str(param.name)].annotation))

        parser.add_argument(str(param.name), type=parameters[str(param.name)].annotation,
                            location=location)

    return parser

# full example to how get_parser() work.


'''
@ns.route('/enroll/<int:id_>')
class CourseEnroll(Resource):

    #below declare for every param -> name , type , location based on 
    # Query(None)-> location = 'args'
    # Body(None) -> location = 'form'
    # Header(None) -> location = 'header'
    # Cookie(None) -> location = 'cookies'
    # Path(None) this means path param
    # default -> location = 'args'
    
    def post(self, id_=Path(None), name: str = Query(None), course_name: str = Body(None),
             duration: float = Header(None)):
             
        signature = inspect.signature(CourseEnroll.post)
        parameters = dict(signature.parameters)
        student_args = get_parser(signature, parameters).parse_args() #  <--- get_parser()
        print(id_)
        print(student_args["name"])          #get name from Query  
        print(student_args["course_name"])   #get course_name from Body  
        print(student_args["duration"])      #get duration from Header  

        student = {
            "course_id": id_,
            "name": student_args["name"],
            "course_name": student_args["course_name"],
            "duration": student_args["duration"]
        }
        students.append(student)
        return {"Message:": "Successfully Enrolled", "Student": student}, 200
'''