from django.db import models
from enum import Enum


class LabelPost(models.Model):

    urls = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'labelpost'


class Source(models.Model):
    '''Model holding info on sources'''

    name = models.CharField(max_length=100, unique=True)
    homepage = models.URLField(max_length=200, unique=True)
    favicon = models.URLField(max_length=200, unique=True)

    class Meta:
        db_table = 'source'

    def __str__(self):
        return self.name


class Types(Enum):
    NOT_STRIKE = "NOT_STRIKE"
    STRIKE = "STRIKE"
    MANY_STRIKES = "MANY_STRIKES"
    EDITORIAL = "EDITORIAL"


class Article(models.Model):
    ''' Class representing model of a scraper article. '''

    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    date_published = models.DateTimeField(null=True)
    date_scraped = models.DateTimeField()
    url = models.URLField(max_length=600, unique=True)

    # Likelihood that article is reporting on a drone airstrike
    classification_score = models.FloatField(null=True)
    # True if article has been labelled manually, False otherwise
    is_ground_truth = models.BooleanField(null=True, default=False)

    article_type = models.CharField(
        max_length=20,
        choices=[(tag, tag.value) for tag in Types
                ],  # Choices is a list of Tuple
        null=True)

    class Meta:
        db_table = 'article'

    def __str__(self):
        return '{} ({})'.format(self.title, self.source.name)


class DateEntity(models.Model):
    seed = models.OneToOneField(
        Article, on_delete=models.CASCADE, related_name='date_entity')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    date_str = models.CharField(max_length=50)
    date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'date_entity'


class LocationEntity(models.Model):
    seed = models.OneToOneField(
        Article, on_delete=models.CASCADE, related_name='location_entity')
    country_start_index = models.IntegerField(null=True)
    region_start_index = models.IntegerField(null=True)
    country_end_index = models.IntegerField(null=True)
    region_end_index = models.IntegerField(null=True)
    country = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=200, null=True)

    #TODO: come up with fields to better describe location (e.g. latitude, longitude ..)

    class Meta:
        db_table = 'location_entity'


class KilledEntity(models.Model):
    seed = models.OneToOneField(
        Article, on_delete=models.CASCADE, related_name='killed_entity')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    num_killed = models.IntegerField()

    class Meta:
        db_table = 'killed_entity'


class InjuredEntity(models.Model):
    seed = models.OneToOneField(
        Article, on_delete=models.CASCADE, related_name='injured_entity')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    num_injured = models.IntegerField()

    class Meta:
        db_table = 'injured_entity'


class PerpetratorEntity(models.Model):
    seed = models.OneToOneField(
        Article, on_delete=models.CASCADE, related_name='perpetrator_entity')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    perpetrator = models.CharField(max_length=100)

    class Meta:
        db_table = 'perpetrator_entity'
