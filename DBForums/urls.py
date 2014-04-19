from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DBForums.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^db/api/forum/create/$', 'API.Views.forum.createForum', name='createForum'),
    url(r'^db/api/forum/details/$', 'API.Views.forum.detailForum', name='detailForum'),
    url(r'^db/api/forum/listThreads/$', 'API.Views.forum.listThreadsForum', name='listThreadForum'),
    url(r'^db/api/forum/listPosts/$', 'API.Views.forum.listPostsForum', name='listPostsForum'),
    url(r'^db/api/forum/listUsers/$', 'API.Views.forum.listUsersForum', name='listUsersForum'),

    url(r'^db/api/thread/create/$', 'API.Views.thread.createThread', name='createThread'),
    url(r'^db/api/thread/details/$', 'API.Views.thread.detailsThread', name='detailThread'),
    url(r'^db/api/thread/close/$', 'API.Views.thread.closeThread', name='closeThread'),
    url(r'^db/api/thread/open/$', 'API.Views.thread.openThread', name='openThread'),
    url(r'^db/api/thread/close/$', 'API.Views.thread.closeThread', name='closeThread'),
    url(r'^db/api/thread/vote/$', 'API.Views.thread.voteThread', name='voteThread'),
    url(r'^db/api/thread/list/$', 'API.Views.thread.thread_list', name='listThread'),
    url(r'^db/api/thread/update/$', 'API.Views.thread.updateThread', name='updateThread'),
    url(r'^db/api/thread/remove/$', 'API.Views.thread.removeThread', name='removeThread'),
    url(r'^db/api/thread/vote/$', 'API.Views.thread.voteThread', name='voteThread'),
    url(r'^db/api/thread/list/$', 'API.Views.thread.thread_list', name='listThread'),
    url(r'^db/api/thread/update/$', 'API.Views.thread.updateThread', name='updateThread'),
    url(r'^db/api/thread/remove/$', 'API.Views.thread.removeThread', name='removeThread'),
    url(r'^db/api/thread/restore/$', 'API.Views.thread.restoreThread', name='restoreThread'),
    url(r'^db/api/thread/subscribe/$', 'API.Views.thread.subscribeThread', name='subscribeThread'),
    url(r'^db/api/thread/unsubscribe/$', 'API.Views.thread.unsubscribeThread', name='unsubscribeThread'),
    url(r'^db/api/thread/restore/$', 'API.Views.thread.restoreThread', name='restoreThread'),
    url(r'^db/api/thread/listPosts/$', 'API.Views.thread.listPost', name='listPostsThread'),

    url(r'^db/api/post/remove/$', 'API.Views.post.removePost', name='removePost'),
    url(r'^db/api/post/restore/$', 'API.Views.post.restorePost', name='restorePost'),
    url(r'^db/api/post/update/$', 'API.Views.post.updatePost', name='updatePost'),
    url(r'^db/api/post/create/$', 'API.Views.post.createPost', name='createPost'),
    url(r'^db/api/post/details/$', 'API.Views.post.detailsPost', name='detailsPost'),
    url(r'^db/api/post/list/$', 'API.Views.post.listPost', name='listPost'),
    url(r'^db/api/post/vote/$', 'API.Views.post.votePost', name='votePost'),


    url(r'^db/api/user/follow/$', 'API.Views.user.followUser', name='followUser'),
    url(r'^db/api/user/unfollow/$', 'API.Views.user.unfollowUser', name='unfollowUser'),
    url(r'^db/api/user/listFollowers/$', 'API.Views.user.listFollowersUser', name='listFollowers'),
    url(r'^db/api/user/listFollowing/$', 'API.Views.user.listFollowing', name='listFollowing'),
    url(r'^db/api/user/create/$', 'API.Views.user.createUser', name='createUser'),
    url(r'^db/api/user/details/$', 'API.Views.user.detailsUser', name='detailsUser'),
    url(r'^db/api/user/updateProfile/$', 'API.Views.user.updatePost', name='updateUser'),
    url(r'^db/api/user/listPosts/$', 'API.Views.user.listPost', name='postsUser'),

    url(r'^db/api/clear/$', 'API.Views.dropper.dropDB', name='dropDB'),
)
