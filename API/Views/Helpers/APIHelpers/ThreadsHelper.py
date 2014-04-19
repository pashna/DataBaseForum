from API.Views.Helpers.Connector.Execuror import Update, Select
from API.Views.Helpers.APIHelpers import ForumsHelper, UsersHelper
from API.Views.Helpers.Instruments import finder


def createThreadHelper(forum, title, isClosed, user, date, message, slug, optional):
    finder.find(table="Users", id="email", value=user)
    finder.find(table="Forums", id="short_name", value=forum)

    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    select = Select('select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE slug = %s', (slug, )
    )
    if len(select) == 0:
        Update('INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (forum, title, isClosed, user, date, message, slug, isDeleted, )
        )
        select = Select(
            'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
            'FROM Threads WHERE slug = %s', (slug, )
        )
    response = threadFormat(select)

    # Delete few extra elements
    del response["dislikes"]
    del response["likes"]
    del response["points"]
    del response["posts"]

    return response


def detailsThreadHelper(id, related):
    select = Select(
        'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE id = %s', (id, )
    )
    if len(select) == 0:
        raise Exception('No thread exists with id=' + str(id))
    select = threadFormat(select)

    if "user" in related:
        select["user"] = UsersHelper.detailsHelper(select["user"])
    if "forum" in related:
        select["forum"] = ForumsHelper.detailForumHelper(short_name=select["forum"], related=[])

    return select


def threadFormat(thread):
    thread = thread[0]
    format = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }
    return format


def voteThreadHelper(id, value):
    finder.find(table="Threads", id="id", value=id)

    if value == -1:
        Update("UPDATE Threads SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
    else:
        Update("UPDATE Threads SET likes=likes+1, points=points+1  where id = %s", (id, ))

    return detailsThreadHelper(id=id, related=[])


def toggleThreadHelper(id, isClosed):
    finder.find(table="Threads", id="id", value=id)
    Update("UPDATE Threads SET isClosed = %s WHERE id = %s", (isClosed, id, ))

    response = {
        "thread": id
    }

    return response


def updateThreadHelper(id, slug, message):
    finder.find(table="Threads", id="id", value=id)
    Update('UPDATE Threads SET slug = %s, message = %s WHERE id = %s',
                          (slug, message, id, ))

    return detailsThreadHelper(id=id, related=[])


def listThreadHelper(table, id, related, params):
    if table == "forum":
        finder.find(table="Forums", id="short_name", value=id)
    if table == "user":
        finder.find(table="Users", id="email", value=id)
    select = "SELECT id FROM Threads WHERE " + table + " = %s "
    parameters = [id]

    if "since" in params:
        select += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        select += " ORDER BY date " + params["order"]
    else:
        select += " ORDER BY date DESC "
    if "limit" in params:
        select += " LIMIT " + str(params["limit"])

    result = Select(query=select, params=parameters)
    threadArray= []

    for id in result:
        id = id[0]
        threadArray.append(detailsThreadHelper(id=id, related=related))

    return threadArray


def toggleDeleteThreadHelper(thread_id, status):
    finder.find(table="Threads", id="id", value=thread_id)
    Update("UPDATE Threads SET isDeleted = %s WHERE id = %s", (status, thread_id, ))

    res = {
        "thread": thread_id
    }
    return res


def createSubscriptionHelper(email, thread_id):
    finder.find(table="Threads", id="id", value=thread_id)
    finder.find(table="Users", id="email", value=email)
    select = Select('select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, ))
    if len(select) == 0:
        Update('INSERT INTO Subscriptions (thread, user) VALUES (%s, %s)', (thread_id, email, ))
        select = Select('select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, ))

    answer = {
        "thread": select[0][0],
        "user": select[0][1]
    }
    return answer


def removeSubscriprionHelper(email, thread_id):
    finder.find(table="Threads", id="id", value=thread_id)
    finder.find(table="Users", id="email", value=email)

    select = Select('select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, ))
    if len(select) == 0:
        raise Exception("user " + email + " does not subscribe thread #" + str(thread_id))
    Update('DELETE FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, ))

    answer = {
        "thread": select[0][0],
        "user": select[0][1]
    }
    return answer