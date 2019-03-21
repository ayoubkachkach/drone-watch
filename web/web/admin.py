from django.contrib import admin
from .models import Article, ArticleLabelling, Entity

admin.site.register(Article)
admin.site.register(Entity)
admin.site.register(ArticleLabelling)