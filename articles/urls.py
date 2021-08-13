from django.urls import path
from .views import APIArticle, APIArticleComments, APINestedComments


urlpatterns = [
    path('articles/', APIArticle.as_view(), name='articles'),
    path('article_comments/<int:pk>', APIArticleComments.as_view(), name='article_comments'),
    path('nested_comments/<int:pk>', APINestedComments.as_view(), name='nested_comments')
]
