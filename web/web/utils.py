from django.shortcuts import _get_queryset
from text2digits import text2digits
from web.models import Article
from web.models import CasualtyEntity
from web.models import DateEntity
from web.models import LocationEntity
from web.models import PerpetratorEntity
from web.models import Types
from web.models import VictimEntity
from web.models import CasualtyType


def get_object_or_None(klass, *args, **kwargs):
    """
    function def taken from: http://skorokithakis.github.io/django-annoying/
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def store_label(results, article):
    date_entity = results.get('date', None)
    country_entity = results.get('country', None)
    region_entity = results.get('region', None)
    killed_entity = results.get('killed', None)
    injured_entity = results.get('injured', None)
    perpetrator_entity = results.get('perpetrator', None)
    article_type = results.get('article_type', None)

    DateEntity.objects.filter(seed=article).delete()
    LocationEntity.objects.filter(seed=article).delete()
    CasualtyEntity.objects.filter(seed=article).delete()
    PerpetratorEntity.objects.filter(seed=article).delete()

    if (not article_type):
        article_type = Types.NOT_DRONE.value
    else:
        article_type = getattr(Types, article_type).value

    article.is_ground_truth = True
    article.article_type = article_type

    # t2d = text2digits.Text2Digits()

    if (article_type == Types.STRIKE.value):
        article.classification_score = 1
    else:
        article.classification_score = 0

    if (date_entity):
        date_str = date_entity['content']
        date = DateEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'start_index': int(date_entity['start_index']),
                'end_index': int(date_entity['end_index']),
                'date_str': date_str,
                'date': dateparser.parse(date_str)
            })

        #date.save()
    if (country_entity):
        location, _ = LocationEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'country_start_index': int(country_entity['start_index']),
                'country_end_index': int(country_entity['end_index']),
                'country': country_entity['content'],
            })

    if (region_entity):
        location, _ = LocationEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'region_start_index': int(region_entity['start_index']),
                'region_end_index': int(region_entity['end_index']),
                'region': region_entity['content']
            })

        #location.save()
    if (killed_entity):
        if (killed_entity['content'].lower() == 'a'):
            killed_entity['content'] = '1'
        killed, _ = CasualtyEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'start_index': int(killed_entity['start_index']),
                'end_index': int(killed_entity['end_index']),
                'num': killed_entity['content']
            })
        VictimEntity().objects.update_or_create(
            seed=killed,
            defaults={
                'seed': article,
                'start_index': int(killed_entity['start_index']),
                'end_index': int(killed_entity['end_index']),
                'num': killed_entity['content']
            })
        #killed.save()
    if (injured_entity):
        num_injured = t2d.convert(injured_entity['content'])
        injured, _ = InjuredEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'start_index': int(injured_entity['start_index']),
                'end_index': int(injured_entity['end_index']),
                'num_injured': int(num_injured)
            })
        #injured.save()
    if (perpetrator_entity):
        perpetrator, _ = PerpetratorEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'start_index': int(perpetrator_entity['start_index']),
                'end_index': int(perpetrator_entity['end_index']),
                'perpetrator': perpetrator_entity['content']
            })
    article.save()


def get_related_object(article, field_name):
    result = None
    try:
        result = getattr(article, field_name)
    except getattr(Article, field_name).RelatedObjectDoesNotExist:
        pass

    return result


# def make_label_dict()


def get_labels(article):
    labels = {}

    date = get_object_or_None(DateEntity, seed=article)
    location = get_object_or_None(LocationEntity, seed=article)
    perpetrator = get_object_or_None(PerpetratorEntity, seed=article)

    labels['date'] = date and date.get_dict()
    labels['country'] = location and location.get_country_dict()
    labels['region'] = location and location.get_region_dict()
    labels['perpetrator'] = perpetrator and perpetrator.get_dict()

    casualties = CasualtyEntity.objects.filter(seed=article)
    labels['deaths'] = [
        casualty.get_dict()
        for casualty in casualties
        if casualty.casualty_type == CasualtyType.DEATH.value
    ]
    labels['injuries'] = [
        casualty.get_dict()
        for casualty in casualties
        if casualty.casualty_type == CasualtyType.INJURY.value
    ]

    return labels
