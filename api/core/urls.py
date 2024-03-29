from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')


urlpatterns = [
    path("", include(router.urls)),
    path("tags/<slug:tag_slug>/", TagsView.as_view()),
    path("tags/", TagView.as_view()),
    path("last-posts/", LastPostsView.as_view()),    
    path("feedback/", ContactView.as_view()),
    path('register/', RegisterView.as_view()),    
    path('profile/', ProfileView.as_view()),    
    path("comments/", AddCommentView.as_view()),
    path("comments/<slug:post_slug>/", GetCommentsView.as_view()),
]