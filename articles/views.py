from rest_framework import generics, status
from rest_framework.response import Response

from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer


class APIArticle(generics.ListCreateAPIView):
    """Получение всех и добавление новых статей"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class APIArticleComments(generics.ListCreateAPIView):
    """Добавление комментария к статье, получение всех комментариев к статье до 3 уровня"""
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        """Создание первого комментария к статье"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                comment = serializer.save(path=[-1], article_id=kwargs['pk'])
                comment.path = [comment.id]
                comment.save()
            except:
                return Response({'error': 'Perhaps such an article with pk={0} does not exist'.format(kwargs['pk'])},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """Получение комментариев к статье до 3 уровня включительно"""
        return Comment.objects.filter(article_id=self.kwargs['pk'], path__len__lte=3)


class APINestedComments(generics.ListCreateAPIView):
    """
    Добавление дочернего комментария к переданному в запросе, а также просмотр всех его дочерних комментариев,
    которые лежат дальше 3 уровня
    """
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        """Добавление вложенных комментариев"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                parent_comment = Comment.objects.get(id=kwargs['pk'])
                comment = serializer.save(path=parent_comment.path, article_id=parent_comment.article_id)
                comment.path.append(comment.id)
                comment.save()
            except:
                return Response({'error': 'Perhaps such an comment with pk={0} does not exist'.format(kwargs['pk'])},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        Получение дочерних комментариев от текущего с pk, переданным в качестве параметра pk, которые имеют уровень
        вложенности более 3
        """
        return Comment.objects.filter(path__len__gte=4, path__contains=[self.kwargs['pk']])
