import json

from django.http import HttpResponse

from API.Views.Helpers.APIHelpers import PostHelpers, ThreadsHelper
from API.Views.Helpers.HttpHelpers.helpers import getResponse, getRelated, tryParam, getOptional, getParam, generateError
from API.Views.Helpers.APIHelpers.ThreadsHelper import createSubscriptionHelper, removeSubscriprionHelper


def detailsThread(request):
    if request.method == "GET":
        requestData = getParam(request)
        requiredData = ["thread"]
        related = getRelated(requestData)
        try:
            tryParam(input=requestData, required=requiredData)
            threads = ThreadsHelper.detailsThreadHelper(id=requestData["thread"], related=related)
        except Exception as e:
            return generateError(e.message)
        return getResponse(threads)
    else:
        return HttpResponse(status=400)


def voteThread(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["thread", "vote"]
        try:
            tryParam(input=requestData, required=requiredData)
            threads = ThreadsHelper.voteThreadHelper(id=requestData["thread"], value=requestData["vote"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(threads)
    else:
        return HttpResponse(status=400)


def subscribeThread(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["thread", "user"]
        try:
            tryParam(input=requestData, required=requiredData)
            subscriptions = createSubscriptionHelper(email=requestData["user"], thread_id=requestData["thread"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(subscriptions)
    else:
        return HttpResponse(status=400)


def createThread(request):
    if request.method == "POST":

        requestData = json.loads(request.body)
        requiredData = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
        option = getOptional(request=requestData, values=["isDeleted"])
        try:
            tryParam(input=requestData, required=requiredData)
            threads = ThreadsHelper.createThreadHelper(forum=requestData["forum"], title=requestData["title"], isClosed=requestData["isClosed"],
                                     user=requestData["user"], date=requestData["date"], message=requestData["message"],
                                     slug=requestData["slug"], optional=option)
        except Exception as e:
            return generateError(e.message)
        return getResponse(threads)
    else:
        return HttpResponse(status=400)


def openThread(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["thread"]
        try:
            tryParam(input=requestData, required=requiredData)
            threads = ThreadsHelper.toggleThreadHelper(id=requestData["thread"], isClosed=0)
        except Exception as e:
            return generateError(e.message)
        return getResponse(threads)
    else:
        return HttpResponse(status=400)


def closeThread(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["thread"]
        try:
            tryParam(input=requestData, required=requiredData)
            threads = ThreadsHelper.toggleThreadHelper(id=requestData["thread"], isClosed=1)
        except Exception as e:
            return generateError(e.message)
        return getResponse(threads)
    else:
        return HttpResponse(status=400)


def unsubscribeThread(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["thread", "user"]
        try:
            tryParam(input=requestData, required=requiredData)
            subscriptions = removeSubscriprionHelper(email=requestData["user"], thread_id=requestData["thread"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(subscriptions)
    else:
        return HttpResponse(status=400)

def updateThread(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["thread", "slug", "message"]
        try:
            tryParam(input=requestData, required=requiredData)
            threads = ThreadsHelper.updateThreadHelper(id=requestData["thread"], slug=requestData["slug"], message=requestData["message"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(threads)
    else:
        return HttpResponse(status=400)


def removeThread(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["thread"]
        try:
            tryParam(input=requestData, required=requiredData)
            threads = ThreadsHelper.toggleDeleteThreadHelper(thread_id=requestData["thread"], status=1)
        except Exception as e:
            return generateError(e.message)
        return getResponse(threads)
    else:
        return HttpResponse(status=400)


def restoreThread(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["thread"]
        try:
            tryParam(input=requestData, required=requiredData)
            threads = ThreadsHelper.toggleDeleteThreadHelper(thread_id=requestData["thread"], status=0)
        except Exception as e:
            return generateError(e.message)
        return getResponse(threads)
    else:
        return HttpResponse(status=400)


def thread_list(request):
    if request.method == "GET":
        requestData = getParam(request)
        id = None
        try:
            id = requestData["forum"]
            table = "forum"
        except KeyError:
            try:
                id = requestData["user"]
                table = "user"
            except KeyError:
                return generateError("No user or forum parameters setted")
        optional = getOptional(request=requestData, values=["limit", "order", "since"])
        try:
            t_list = ThreadsHelper.listThreadHelper(table=table, id=id, related=[], params=optional)
        except Exception as e:
            return generateError(e.message)
        return getResponse(t_list)
    else:
        return HttpResponse(status=400)


def listPost(request):
    if request.method == "GET":
        requestData = getParam(request)
        requiredData = ["thread"]
        table = "thread"
        optional = getOptional(request=requestData, values=["limit", "order", "since"])
        try:
            tryParam(input=requestData, required=requiredData)
            arrayPost = PostHelpers.postListHelper(table=table, id=requestData["thread"], related=[], option=optional)
        except Exception as e:
            return generateError(e.message)
        return getResponse(arrayPost)
    else:
        return HttpResponse(status=400)