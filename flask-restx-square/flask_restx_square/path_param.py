from typing import List
import re


def ExtractPathParams(path):
    ParamsTypesList: List[str] = []  # Store path params with their type
    ParamsList: List[str] = []  # Store path params without type
    '''
    #this code for dealing with List of tuples (the output from ns.resources)
    urls : List[str]= []
    #extarct paths related to this API namespace
    for pathTuple in paths:
        for path in pathTuple[1]:
            urls.append(path)
    '''
    # Searching for params between angle brackets
    params = re.findall('\<(.*?)\>', path)  # returns a list with all matches
    if(len(params) > 0):
        ParamsTypesList.extend(params)
    # removing param type
    for param in ParamsTypesList:
        param = param[param.find(':')+1:]
        ParamsList.append(param)
    return ParamsList
