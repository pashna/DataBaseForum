from API.Views.Helpers.Connector.Execuror import Update, Select
from API.Views.Helpers.APIHelpers import UsersHelper
from API.Views.Helpers.Instruments import finder


def createForumHelper(name, short_name, user):
    finder.find(table="Users", id="email", value=user)
    result = Select('select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, ))
    if len(result) == 0:
        Update('INSERT INTO Forums (name, short_name, user) VALUES (%s, %s, %s)',
                              (name, short_name, user, ))
        result = Select('select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, ))
    return ForumFormat(result)


def ForumFormat(forum):
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return response


def detailForumHelper(short_name, related):
    result = Select('select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name,))
    if len(result) == 0:
        raise ("Cant find  forum " + short_name)
    result = ForumFormat(result)

    if "user" in related:
        result["user"] = UsersHelper.detailsHelper(result["user"])
    return result


def listForumUsersHelper(short_name, optional):
    finder.find(table="Forums", id="short_name", value=short_name)

    select = "SELECT distinct email FROM Users JOIN Posts ON Posts.user = Users.email " \
            " JOIN Forums on Forums.short_name = Posts.forum WHERE Posts.forum = %s "
    if "since_id" in optional:
        select += " AND Users.id >= " + str(optional["since_id"])
    if "order" in optional:
        select += " ORDER BY Users.id " + optional["order"]
    if "limit" in optional:
        select += " LIMIT " + str(optional["limit"])

    resultArray = []
    result = Select(select, (short_name, ))
    for user in result:
        user = user[0]
        resultArray.append(UsersHelper.detailsHelper(user))
    return resultArray
