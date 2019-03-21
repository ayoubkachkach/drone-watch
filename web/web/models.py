from django.db import models



class EntityType(Enum):
    DATE = "DATE"
    LOCATION = "LOCATION"
    KILLED = "KILLED"
    INJURED = "INJURED"

class Source(models.Model):
    '''Model holding info on sources'''

    name = models.CharField(max_length=100)
    homepage = models.URLField(max_length=200, unique=True)
    favicon = models.URLField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    ''' Class representing model of a scraper article. '''

    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    date_published = models.DateTimeField()
    date_scraped = models.DateTimeField()
    url = models.URLField(max_length=600, unique=True)

    def __str__(self):
        return '{} ({})'.format(self.title, self.source_name)


class ArticleLabelling(models.Model):
    seed = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='seed')
    # Likelihood that article is reporting on a drone airstrike
    classification_score = models.FloatField(null=True)
    # Entities extracted from article
    entities = models.ManyToManyField(Entity, null=True)
    is_ground_truth = models.BooleanField(default=False)


class Entity(models.Model):
    seed = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='seed')
    type = models.CharField(
      choices=[(entity, entity.value) for entity in EntityType]
    )
    start_index = models.IntegerField() 
    end_index = models.IntegerField()

