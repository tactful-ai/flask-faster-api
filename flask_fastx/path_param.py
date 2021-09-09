'''
This module is for extracting path params from a given route
'''

from typing import List, Optional, get_args
import re


def extract_path_params(path):
    '''
    Extracting path params from string by regex and append them to list
    '''
    params_types_list: List[str] = []  # Store path params with their type
    params_list: List[str] = []  # Store path params without type
    # Searching for params between angle brackets
    params = re.findall(r'\<(.*?)\>', path)  # returns a list with all matches
    if len(params) > 0:
        params_types_list.extend(params)
    # removing param type
    for param in params_types_list:
        param = param[param.find(':')+1:]
        params_list.append(param)
    return params_list


class name:
    names: List[str]


annot = name.__annotations__['names']

print(annot.__args__[0])
