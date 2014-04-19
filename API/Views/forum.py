import json

from django.http import HttpResponse

from API.Views.Helpers.APIHelpers import ForumsHelper, PostHelpers, ThreadsHelper
from API.Views.Helpers.HttpHelpers.helpers import getRelated, getResponse, tryParam, getOptional, getParam, generateError


def createForum(request):
    if request.method == "POST":
        requiredData = ["name", "short_name", "user"]
        requestData = json.loads(request.body)
        try:
            tryParam(input=requestData, required=requiredData)
            forum = ForumsHelper.createForumHelper(name=requestData["name"], short_name=requestData["short_name"],
                                      user=requestData["user"])
        except Exception as e:
            print(e.message)
            return generateError(e.message)
        return getResponse(forum)
    else:
        return HttpResponse(status=400)



def listThreadsForum(request):
    if request.method == "GET":
        required = ["forum"]
        request = getParam(request)
        related = getRelated(request)
        optional = getOptional(request=request, values=["limit", "order", "since"])
        try:
            tryParam(input=request, required=required)
            arrayThreads = ThreadsHelper.listThreadHelper(table="forum", id=request["forum"],
                                             related=related, params=optional)
        except Exception as e:
            return generateError(e.message)
        return getResponse(arrayThreads)
    else:
        return HttpResponse(status=400)


def detailForum(request):
    if request.method == "GET":
        requestData = getParam(request)
        requiredData = ["forum"]
        related = getRelated(requestData)
        try:
            tryParam(input=requestData, required=requiredData)
            forums = ForumsHelper.detailForumHelper(short_name=requestData["forum"], related=related)
        except Exception as e:
            return generateError(e.message)
        return getResponse(forums)
    else:
        return HttpResponse(status=400)

def listUsersForum(request):
    if request.method == "GET":
        request_data = getParam(request)
        required_data = ["forum"]
        optional = getOptional(request=request_data, values=["limit", "order", "since_id"])
        try:
            tryParam(input=request_data, required=required_data)
            arrayUsers = ForumsHelper.listForumUsersHelper(request_data["forum"], optional)
        except Exception as e:
            return generateError(e.message)
        return getResponse(arrayUsers)
    else:
        return HttpResponse(status=400)


def listPostsForum(request):
    if request.method == "GET":
        requestData = getParam(request)
        requiredData = ["forum"]
        related = getRelated(requestData)
        optional = getOptional(request=requestData, values=["limit", "order", "since"])
        try:
            tryParam(input=requestData, required=requiredData)
            arrayPosts = PostHelpers.postListHelper(table="forum", id=requestData["forum"],
                                       related=related, option=optional)
        except Exception as e:
            return generateError(e.message)
        return getResponse(arrayPosts)
    else:
        return HttpResponse(status=400)