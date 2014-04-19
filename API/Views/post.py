import json

from django.http import HttpResponse

from API.Views.Helpers.APIHelpers import PostHelpers
from API.Views.Helpers.HttpHelpers.helpers import tryParam, getResponse, getOptional, getRelated, getParam, generateError


def detailsPost(request):
    if request.method == "GET":

        requestData = getParam(request)
        requiredData = ["post"]
        relating = getRelated(requestData)
        try:
            tryParam(input=requestData, required=requiredData)
            posts = PostHelpers.detailsPostHelper(requestData["post"], option=relating)
        except Exception as e:
            return generateError(e.message)
        return getResponse(posts)
    else:
        return HttpResponse(status=400)


def createPost(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["user", "forum", "thread", "message", "date"]
        optionalData = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
        option = getOptional(request=requestData, values=optionalData)
        try:
            tryParam(input=requestData, required=requiredData)
            post = PostHelpers.createPostHelper(date=requestData["date"], thread=requestData["thread"],
                                message=requestData["message"], user=requestData["user"],
                                forum=requestData["forum"], optional=option)
        except Exception as e:
            return generateError(e.message)
        return getResponse(post)
    else:
        return HttpResponse(status=400)


def listPost(request):
    if request.method == "GET":
        requestData = getParam(request)
        id = None
        try:
            id = requestData["forum"]
            table = "forum"
        except KeyError:
            try:
                id = requestData["thread"]
                table = "thread"
            except KeyError:
                return generateError("ListPost Error")

        optional = getOptional(request=requestData, values=["limit", "order", "since"])
        try:
            postArray = PostHelpers.postListHelper(table=table, id=id, related=[], option=optional)
        except Exception as e:
            return generateError(e.message)
        return getResponse(postArray)
    else:
        return HttpResponse(status=400)

"""
Ne rabotaet??? Try param?
ask votePost
"""
def removePost(request):
    if request.method == "POST":
        requiredData = ["post"]
        requestData = json.loads(request.body)
        try:
            tryParam(input=requestData, required=requiredData)
            posts = PostHelpers.togglePostHelper(post_id=requestData["post"], mark=1)
        except Exception as e:
            return generateError(e.message)
        return getResponse(posts)
    else:
        return HttpResponse(status=400)


def restorePost(request):
    if request.method == "POST":
        requiredData = ["post"]
        requestData = json.loads(request.body)
        try:
            tryParam(input=requestData, required=requiredData)
            post = PostHelpers.togglePostHelper(post_id=requestData["post"], mark=0)
        except Exception as e:
            return generateError(e.message)
        return getResponse(post)
    else:
        return HttpResponse(status=400)


def updatePost(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["post", "message"]
        try:
            tryParam(input=requestData, required=requiredData)
            posts = PostHelpers.updatePostHelper(id=requestData["post"], message=requestData["message"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(posts)
    else:
        return HttpResponse(status=400)

def votePost(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["post", "vote"]
        try:
            tryParam(input=requestData, required=requiredData)
            posts = PostHelpers.votePostHelper(id=requestData["post"], vote=requestData["vote"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(posts)
    else:
        return HttpResponse(status=400)