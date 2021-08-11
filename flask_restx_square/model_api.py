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
    'typing.List': fields.List,
    'dict': fields.Raw,
}


def create_model(types, descriptions={}):
    modeltemp = dict()

    for type in types:
        ans = str(types[type])

        if ans.find('typing') != -1:
            key = ans.split("[")[0]
            fieldsParam = ans.split("[")[1].replace("]", "")
            type = str(type)
            if descriptions.get(type) is None:
                descriptions[type] = ""
            modeltemp[type] = python2restplus[key](
                python2restplus[fieldsParam], description=descriptions[type])
        else:
            k = str(type)
            ans = ans.split(" ")[1]
            ans = ans.replace("'", "")
            ans = ans.replace(">", "")
            print("Primitive Type:  ", ans)
            if descriptions.get(k) is None:
                descriptions[k] = ""
            modeltemp[k] = python2restplus[ans](description=descriptions[k])
    return modeltemp
