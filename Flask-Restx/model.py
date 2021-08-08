from enum import Enum
from typing import Any
from flask_restx import fields


class DictItem(fields.Raw):
    def output(self, key, obj, *args, **kwargs):
        try:
            dct = getattr(obj, self.attribute)
        except AttributeError:
            return {}
        return dct or {}


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


def create_model(types, modelName=None):
    # check if types is a dictionary or not if not then return the primitive type
    # if it is then return the model dictionary
    print("type: ", types)
    isPrimitive = True
    ans = str(types)

    if ans.find('typing') == -1:
        ans = ans.split(" ")[1]
        ans = ans.replace("'", "")
        ans = ans.replace(">", "")
        k = str(types)
        if k != 'return':
            # the return should be either the primitive type or a dictionary of primitive types
            # ex either fields.String or {'name': fields.String,duration:fields.Integer} without 'data' and all of this
            return isPrimitive, {'data': python2restplus[ans]}

    else:
        k = str(types)
        return isPrimitive, {'data': python2restplus[ans]}
    # need 2 returns : 1:boolean is primitive or not 2:the model or fileds.<primitiveType>:
