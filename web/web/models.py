from django.db import models


class EntityType(Enum):
    DATE = "DATE"
    LOCATION = "LOCATION"
    KILLED = "KILLED"
    INJURED = "INJURED"


class Source(models.Model):
    '''Model holding info on sources'''

    name = models.CharField(max_length=100, unique=True)
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


class ArticleLabel(models.Model):  #StrikeParameters
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='seed')
    # Likelihood that article is reporting on a drone airstrike
    classification_score = models.FloatField(null=True)
    #True if article has been labelled manually, False otherwise
    is_ground_truth = models.BooleanField(default=False)
    # Entities extracted from article
    date_entities = models.ManyToManyField(DateEntity, null=True)
    location_entities = models.ManyToManyField(LocationEntity, null=True)
    killed_entities = models.ManyToManyField(KilledEntity, null=True)
    injured_entities = models.ManyToManyField(InjuredEntity, null=True)


class DateEntity(models.Model):
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='seed')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    date = models.DateTimeField()


class LocationEntity(models.Model):
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='seed')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    location = models.CharField(max_length=200)
    #TODO: come up with fields to better describe location (e.g. latitude, longitude ..)


class KilledEntity(models.Model):
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='seed')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    num_killed = models.IntegerField()
    #TODO: come up with fields to better describe location (e.g. latitude, longitude ..)


class InjuredEntity(models.Model):
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='seed')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    num_injured = models.IntegerField()
