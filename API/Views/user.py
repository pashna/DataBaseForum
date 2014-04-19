import json

from django.http import HttpResponse

from API.Views.Helpers.APIHelpers import PostHelpers, UsersHelper
from API.Views.Helpers.HttpHelpers.helpers import getResponse, tryParam, getOptional, getParam, generateError
from API.Views.Helpers.APIHelpers.UsersHelper import followHelper, listFollowersHelper, unfollowHelper


def createUser(request):
    if request.method == "POST":

        requestData = json.loads(request.body)
        requiredData = ["email", "username", "name", "about"]
        option = getOptional(request=requestData, values=["isAnonymous"])
        try:
            tryParam(input=requestData, required=requiredData)
            users = UsersHelper.createUserHelper(email=requestData["email"], username=requestData["username"],
                               about=requestData["about"], name=requestData["name"], optional=option)
        except Exception as e:
            return generateError(e.message)
        return getResponse(users)
    else:
        return HttpResponse(status=400)


def detailsUser(request):
    if request.method == "GET":
        requestData = getParam(request)
        requiredData = ["user"]
        try:
            tryParam(input=requestData, required=requiredData)
            userdetails = UsersHelper.detailsHelper(email=requestData["user"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(userdetails)
    else:
        return HttpResponse(status=400)


def followUser(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["follower", "followee"]
        try:
            tryParam(input=requestData, required=requiredData)
            folowing = followHelper(email1=requestData["follower"], email2=requestData["followee"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(folowing)
    else:
        return HttpResponse(status=400)


def unfollowUser(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["follower", "followee"]
        try:
            tryParam(input=requestData, required=requiredData)
            following = unfollowHelper(email1=requestData["follower"], email2=requestData["followee"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(following)
    else:
        return HttpResponse(status=400)

def updatePost(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        requiredData = ["user", "name", "about"]
        try:
            tryParam(input=requestData, required=requiredData)
            users = UsersHelper.updateProfileHelper(email=requestData["user"], name=requestData["name"], about=requestData["about"])
        except Exception as e:
            return generateError(e.message)
        return getResponse(users)
    else:
        return HttpResponse(status=400)


def listFollowersUser(request):
    if request.method == "GET":
        requestData = getParam(request)
        requiredData = ["user"]
        param = getOptional(request=requestData, values=["limit", "order", "since_id"])
        try:
            tryParam(input=requestData, required=requiredData)
            arrayFollower = listFollowersHelper(email=requestData["user"], fol1="follower", optional=param)
        except Exception as e:
            return generateError(e.message)
        return getResponse(arrayFollower)
    else:
        return HttpResponse(status=400)


def listFollowing(request):
    if request.method == "GET":
        requestData = getParam(request)
        requiredData = ["user"]
        param = getOptional(request=requestData, values=["limit", "order", "since_id"])
        try:
            tryParam(input=requestData, required=requiredData)
            followings = listFollowersHelper(email=requestData["user"], fol1="followee", optional=param)
        except Exception as e:
            return generateError(e.message)
        return getResponse(followings)
    else:
        return HttpResponse(status=400)


def listPost(request):
    if request.method == "GET":
        requestData = getParam(request)
        requiredData = ["user"]
        option = getOptional(request=requestData, values=["limit", "order", "since"])
        try:
            tryParam(input=requestData, required=requiredData)
            arrayPosts = PostHelpers.postListHelper(table="user", id=requestData["user"], related=[], option=option)
        except Exception as e:
            return generateError(e.message)
        return getResponse(arrayPosts)
    else:
        return HttpResponse(status=400)
