from django.db import models
from rest_framework import serializers
from pydantic import BaseModel
from typing import List
import django
from django.conf import settings
# settings.configure(DEBUG=True)
# django.setup()

django_type_map = {
    'int': models.IntegerField(),
    'str': models.TextField(),
    'datetime': models.DateTimeField(),
    'time': models.TimeField(),
    'bool': models.BooleanField(),
    'float': models.FloatField(),
    'typing.List': models.ManyToManyField,
}


def create_list_model(primitive_data_type=str):
    class Data(models.Model):
        data = django_type_map[str(primitive_data_type)]

    print(Data.__dict__)
    return Data


def get_model(types):
    modeltemp = {}
    for type_ in types:
        ans = str(types[type_])

        if ans.find('typing') != -1:
            key = ans.split("[")[0]
            fields_param = ans.split("[")[1].replace("]", "")
            type_ = str(type_)
            ListModel = create_list_model(fields_param)
            modeltemp[type_] = django_type_map[key](ListModel)
        else:
            k = str(type_)
            ans = ans.split(" ")[1]
            ans = ans.replace("'", "")
            ans = ans.replace(">", "")
            print("Primitive Type:  ", ans)
            modeltemp[k] = django_type_map[ans]
    return modeltemp


def create_serializer(api_model, serializer_fields):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = api_model
            fields = serializer_fields
    return Serializer


def create_django_api_model_serializer(model_class, serializer_fields=None, exclude_fields=None):
    # map the model_class types to djano types
    params_return = model_class.__annotations__
    model = get_model(params_return)
    model['__module__'] = __name__
    model = type(model_class.__name__, (models.Model,), model)
    # create the serializer
    serializer = create_serializer(model, serializer_fields)
    return model, serializer
