import json
from django.http import HttpResponse
"""
???????????????????????????????
getRelated
getOption
getParam
??????????????????????????
"""
def getRelated(request):
    try:
        related = request["related"]
    except KeyError:
        related = []
    return related
"""
???????????????????????????????
try getRelated, ASK TECHNOPARK!!!
??????????????????????????
"""

def getResponse(object):
    response_info = {"code": 0, "response": object}
    return HttpResponse(json.dumps(response_info), content_type='application/json')

def generateError(message):
    response_data = {"code": 1, "response": message}
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def getParam(request):
    data = {}
    for el in request.GET:
        data[el] = request.GET.get(el)
    return data

def getOptional(request, values):
    optional = {}
    for value in values:
        try:
            optional[value] = request[value]
        except KeyError:
            continue
    return optional


def tryParam(input, required):
    for el in required:
        if el not in input:
            raise Exception(el + " not in parameters")
        if input[el] is not None:
            try:
                input[el] = input[el].encode('utf-8')
            except Exception:
                continue

    return