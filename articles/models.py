from django.contrib.postgres.fields import ArrayField
from django.db import models


class Article(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    publication_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    content = models.TextField(verbose_name='Текст статьи')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    path = ArrayField(models.IntegerField())
    article = models.ForeignKey(Article, verbose_name='Статья', on_delete=models.CASCADE)
    publication_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    content = models.TextField(verbose_name='Текст комментария')

    def __str__(self):
        return self.content[:200]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
