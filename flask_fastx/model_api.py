'''
This files contains the implementation of the model generator function
it takes return type as input and returns a model as an output
'''
# pylint: disable=C0207

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
}


def create_model(types, descriptions):
    '''
    the model generator function which takes return type as input and returns a model as an output
    '''
    modeltemp = {}
    for type_ in types:
        ans = str(types[type_])

        if ans.find('typing') != -1:
            key = ans.split("[")[0]
            fields_param = ans.split("[")[1].replace("]", "")
            type_ = str(type_)
            if descriptions.get(type_) is None:
                descriptions[type_] = ""
            if python2restplus.get(fields_param) is None:
                fields_param = 'dict'
            modeltemp[type_] = python2restplus[key](
                python2restplus[fields_param], description=descriptions[type_])
        else:
            k = str(type_)
            ans = ans.split(" ")[1]
            ans = ans.replace("'", "")
            ans = ans.replace(">", "")
            if descriptions.get(k) is None:
                descriptions[k] = ""
            modeltemp[k] = python2restplus[ans](description=descriptions[k])
    return modeltemp
