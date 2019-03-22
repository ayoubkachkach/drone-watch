from django.db import models


class Source(models.Model):
    '''Model holding info on sources'''

    name = models.CharField(max_length=100, unique=True)
    homepage = models.URLField(max_length=200, unique=True)
    favicon = models.URLField(max_length=200, unique=True)

    class Meta:
        db_table = 'source'

    def __str__(self):
        return self.name


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

    class Meta:
        db_table = 'article'

    def __str__(self):
        return '{} ({})'.format(self.title, self.source_name)


class DateEntity(models.Model):
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='date_entities')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        db_table = 'date_entity'


class LocationEntity(models.Model):
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='location_entities')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    location = models.CharField(max_length=200)
    #TODO: come up with fields to better describe location (e.g. latitude, longitude ..)

    class Meta:
        db_table = 'location_entity'


class KilledEntity(models.Model):
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='killed_entities')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    num_killed = models.IntegerField()

    class Meta:
        db_table = 'killed_entity'


class InjuredEntity(models.Model):
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='injured_entities')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    num_injured = models.IntegerField()

    class Meta:
        db_table = 'injured_entity'


class PerpetratorEntity(models.Model):
    seed = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='perpetrator_entities')
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    perpetrator = models.CharField(max_length=100)

    class Meta:
        db_table = 'perpetrator_entity'