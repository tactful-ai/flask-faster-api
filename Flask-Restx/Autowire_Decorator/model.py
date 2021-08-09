from enum import Enum
from typing import Any
from flask_restx import fields


python2restplus = {
    'str': fields.String,
    'datetime': fields.DateTime,
    'time': fields.String,
    'bool': fields.Boolean,
    'int': fields.Integer,
    'float': fields.Float,
    'relation': fields.Nested,
    'list': fields.List,
    'dict': fields.Raw,
    'enum': Enum,
}


def create_model(types):
    # this works with primitive types now
    modeltemp = dict()

    for type in types:
        ans = str(types[type])
        print(ans)
        if ans.find('typing') == -1:
            ans = ans.split(" ")[1]
            ans = ans.replace("'", "")
            ans = ans.replace(">", "")
            k = str(type)
            if k != 'return':
                modeltemp[k] = python2restplus[ans]

        else:
            k = str(type)
            if k != 'return':
                # for typing module stuff (optional, union, ....) which is not in the types dict
                modeltemp[k] = ans
    return modeltemp
