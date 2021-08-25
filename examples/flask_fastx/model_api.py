'''
This files contains the implementation of the model generator function
it takes return type as input and returns a model as an output
'''
# pylint: disable=C0207

import re
from flask_restx import fields   # type: ignore

# dict to map each return type to its field data type
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
    'nested': fields.Nested,
}


def create_model(api, types, descriptions):
    '''
    the model generator function which takes return type as input and returns a model as an output
    '''
    x = dict()

    for key, value in types.items():
        if isinstance(value, dict):
            x = extract_dict_attr(api, value, key, descriptions)
            types[key] = fields.Nested(api.model(key, x))
        else:
            q = str(value)
            if q.find('typing') != -1:
                x, types[key] = extract_prim_typing(
                    value, key, descriptions)
            else:
                x, types[key] = extract_prim(value, key, descriptions)
    return types


def extract_dict_attr(api, ans, type_, descriptions):
    '''
    extracts any dictionary attributes to API models, works with primitive and complex types
    '''
    fieldTypes = dict()
    for key, value in ans.items():
        if isinstance(value, dict):
            x = extract_dict_attr(api, value, key, descriptions)
            fieldTypes[key] = fields.Nested(api.model(key, x))
        else:
            q = str(value)
            if q.find('typing') != -1:
                x, ans = extract_prim_typing(value, key, descriptions)
                fieldTypes[key] = ans
            else:
                x, ans = extract_prim(value, key, descriptions)
                fieldTypes[key] = ans
    return fieldTypes


def extract_prim_typing(ans, type_, descriptions):
    ans = str(ans)
    if ans.find('typing') != -1:
        key = ans.split("[")[0]
        fields_param = ans.split("[")[1].replace("]", "")
        type_ = str(type_)
        if descriptions.get(type_) is None:
            descriptions[type_] = ""
        if python2restplus.get(fields_param) is None:
            fields_param = 'dict'

        key = str(key)

        fieldsType = python2restplus[key](
            python2restplus[fields_param], description=descriptions[type_])

        return key, fieldsType


def extract_prim(ans, type_, descriptions):
    ans = str(ans)
    k = str(type_)
    ans = ans.split(" ")[1]
    ans = ans.replace("'", "")
    ans = ans.replace(">", "")
    if descriptions.get(k) is None:
        descriptions[k] = ""
    key = ans
    if key in python2restplus:
        fieldsType = python2restplus[key](description=descriptions[k])
    else:
        fieldsType = None

    return key, fieldsType
