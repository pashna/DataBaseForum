from API.Views.Helpers.Connector.Execuror import Update, Select
from API.Views.Helpers.Instruments import finder


def createUserHelper(email, username, about, name, optional):

    try:
        isAnonymous = 0
        if "isAnonymous" in optional:
            isAnonymous = optional["isAnonymous"]
        user = Select('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
        if len(user) == 0:
            Update(
                'INSERT INTO Users (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, isAnonymous, ))
        user = Select('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s',
                           (email, ))
    except Exception as e:
        raise Exception(e.message)

    return userFormat(user)


def updateProfileHelper(email, about, name):
    finder.find(table="Users", id="email", value=email)
    Update('UPDATE Users SET email = %s, about = %s, name = %s WHERE email = %s',
                          (email, about, name, email, ))
    return detailsHelper(email)


def followerListHelper(email, type):
    where = "followee"
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"
    arrayFol = Select("SELECT " + type + " FROM Followers JOIN Users ON Users.email = Followers." + type +
                    " WHERE " + where + " = %s ", (email, )
    )
    result = []
    for el in arrayFol:
        result.append(el[0])
    return result


def detailsHelper(email):
    user = userFormat(Select('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, )))
    user["followers"] = followerListHelper(email, "follower")
    user["following"] = followerListHelper(email, "followee")
    user["subscriptions"] = userInThreadHelper(email)
    return user


def userInThreadHelper(email):
    s_list = []
    subscriptions = Select('select thread FROM Subscriptions WHERE user = %s', (email, ))
    for el in subscriptions:
        s_list.append(el[0])
    return s_list


def userFormat(user):
    user = user[0]
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }
    return user_response

def followHelper(email1, email2):
    finder.find(table="Users", id="email", value=email1)
    finder.find(table="Users", id="email", value=email2)

    if email1 == email2:
        raise Exception("User with email=" + email1 + " can't follow himself")

    result = Select('SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, ))

    if len(result) == 0:
        Update('INSERT INTO Followers (follower, followee) VALUES (%s, %s)',
                              (email1, email2, ))

    return detailsHelper(email1)


def listFollowersHelper(email, fol1, optional):
    finder.find(table="Users", id="email", value=email)

    if fol1 == "followee":
        fol2 = "follower"
    else:
        fol2 = "followee"

    query = "SELECT "+fol1+" FROM Followers JOIN Users ON Users.email = Followers."+fol1+\
            " WHERE "+fol2+" = %s "
    resultArray = []
    if "since_id" in optional:
        query += " AND Users.id >= "+str(optional["since_id"])
    if "order" in optional:
        query += " ORDER BY Users.name "+optional["order"]
    else:
        query += " ORDER BY Users.name DESC "
    if "limit" in optional:
        query += " LIMIT "+str(optional["limit"])

    resultSelect = Select(query=query, params=(email, ))

    for id in resultSelect:
        id = id[0]
        resultArray.append(detailsHelper(email=id))

    return resultArray


def unfollowHelper(email1, email2):
    followers = Select('SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, ))

    if len(followers) != 0:
        Update('DELETE FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, ))
    else:
        raise Exception("No such following")
    return detailsHelper(email1)