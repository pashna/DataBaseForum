from API.Views.Helpers.Connector.Connector import connect
from API.Views.Helpers.Connector.Execuror import Update, Select
from API.Views.Helpers.APIHelpers import ForumsHelper, ThreadsHelper, UsersHelper
from API.Views.Helpers.Instruments import finder


def createPostHelper(date, thread, message, user, forum, optional):
    finder.find(table="Threads", id="id", value=thread)
    finder.find(table="Forums", id="short_name", value=forum)
    finder.find(table="Users", id="email", value=user)
    if len(Select("SELECT Threads.id FROM Threads JOIN Forums ON Threads.forum = Forums.short_name "
                                "WHERE Threads.forum = %s AND Threads.id = %s", (forum, thread, ))) == 0:
        raise Exception("no thread with id = " + thread + " in forum " + forum)
    if "parent" in optional:
        if len(Select("SELECT Posts.id FROM Posts JOIN Threads ON Threads.id = Posts.thread "
                             "WHERE Posts.id = %s AND Threads.id = %s", (optional["parent"], thread, ))) == 0:
            raise Exception("Cant find post with id = " + optional["parent"])
    query = "INSERT INTO Posts (message, user, forum, thread, date"
    values = "(%s, %s, %s, %s, %s"
    parameters = [message, user, forum, thread, date]

    for param in optional:
        query += ", "+param
        values += ", %s"
        parameters.append(optional[param])

    query += ") VALUES " + values + ")"

    update = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"

    connection = connect()
    with connection:
        cursor = connection.cursor()
        try:
            connection.begin()
            cursor.execute(update, (thread, ))
            cursor.execute(query, parameters)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception("Database error: " + e.message)
        post_id = cursor.lastrowid
        cursor.close()

    connection.close()
    post = postQueryHelper(post_id)
    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post


def detailsPostHelper(id, option):
    post = postQueryHelper(id)
    if post is None:
        raise Exception("no post with id = "+id)

    if "user" in option:
        post["user"] = UsersHelper.detailsHelper(post["user"])
    if "forum" in option:
        post["forum"] = ForumsHelper.detailForumHelper(short_name=post["forum"], related=[])
    if "thread" in option:
        post["thread"] = ThreadsHelper.detailsThreadHelper(id=post["thread"], related=[])

    return post


def postListHelper(table, id, related, option):
    if table == "user":
        finder.find(table="Users", id="email", value=id)
    if table == "forum":
        finder.find(table="Forums", id="short_name", value=id)
    if table == "thread":
        finder.find(table="Threads", id="id", value=id)
    select = "SELECT id FROM Posts WHERE " + table + " = %s "
    par = [id]
    if "since" in option:
        select += " AND date >= %s"
        par.append(option["since"])
    if "order" in option:
        select += " ORDER BY date " + option["order"]
    else:
        select += " ORDER BY date DESC "
    if "limit" in option:
        select += " LIMIT " + str(option["limit"])
    query = Select(query=select, params=par)
    post_list = []
    for id in query:
        id = id[0]
        post_list.append(detailsPostHelper(id=id, option=related))
    return post_list


def togglePostHelper(post_id, mark):
    finder.find(table="Posts", id="id", value=post_id)
    Update("UPDATE Posts SET isDeleted = %s WHERE Posts.id = %s", (mark, post_id, ))
    return {
        "post": post_id
    }

"""
def togglePostHelper(post_id, mark):
    finder.find(table="Posts", id="id", value=post_id)
    print "CANT FIND?????"
    return {
        "post": post_id
    }

def updatePostHelper(id, message):
    finder.find(table="Posts", id="id", value=id)
    print "CANT FIND?????"
    return detailsPostHelper(id=id, option=[])
"""

def updatePostHelper(id, message):
    finder.find(table="Posts", id="id", value=id)
    Update('UPDATE Posts SET message = %s WHERE id = %s', (message, id, ))
    return detailsPostHelper(id=id, option=[])


def votePostHelper(id, vote):
    finder.find(table="Posts", id="id", value=id)
    if vote == -1:
        Update("UPDATE Posts SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
    else:
        Update("UPDATE Posts SET likes=likes+1, points=points+1  where id = %s", (id, ))
    return detailsPostHelper(id=id, option=[])

def postQueryHelper(id):
    select = Select('select date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
                       'isHighlighted, isSpam, likes, message, parent, points, thread, user '
                       'FROM Posts WHERE id = %s', (id, ))
    if len(select) == 0:
        return None
    return postFormat(select)


def postFormat(post):
    post = post[0]
    response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],

    }
    return response