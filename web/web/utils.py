import dateparser

from django.shortcuts import _get_queryset
from text2digits import text2digits
from web.models import Article
from web.models import CasualtyEntity
from web.models import CasualtyType
from web.models import DateEntity
from web.models import LocationEntity
from web.models import PerpetratorEntity
from web.models import Types
from web.models import VictimEntity


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


def store_label(entities, article):
    date_entity = entities.get('date', None)
    country_entity = entities.get('country', None)
    region_entity = entities.get('region', None)
    perpetrator_entity = entities.get('perpetrator', None)
    article_type = entities.get('article_type', None)

    deaths = entities.get('deaths', [])
    injuries = entities.get('injuries', [])

    DateEntity.objects.filter(seed=article).delete()
    LocationEntity.objects.filter(seed=article).delete()

    print("HEEERE")
    print(CasualtyEntity._meta.get_fields())

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
        # If date_published is None, set relative_base for date parsing to date_scraped
        relative_base = article.date_published or article.date_scraped

        date, _ = DateEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed':
                article,
                'start_index':
                int(date_entity['start_index']),
                'end_index':
                int(date_entity['end_index']),
                'date_str':
                date_str,
                'date':
                dateparser.parse(
                    date_str, settings={'RELATIVE_BASE': relative_base})
            })
        date.save()

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
        location.save()

    if (region_entity):
        location, _ = LocationEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'region_start_index': int(region_entity['start_index']),
                'region_end_index': int(region_entity['end_index']),
                'region': region_entity['content']
            })
        location.save()

    for death in deaths:

        if (not death):
            continue

        print("HERE")
        if (death['content'].lower() == 'a'):
            death['content'] = '1'
        killed = CasualtyEntity(
            seed=article,
            start_index=int(death['start_index']),
            end_index=int(death['end_index']),
            num=death['content'],
            casualty_type=CasualtyType.DEATH.value)
        killed.save()

        victim = death['victim']
        if (not victim):
            continue

        victim_entity, _ = VictimEntity.objects.update_or_create(
            seed=killed,
            defaults={
                'seed': killed,
                'start_index': int(victim['start_index']),
                'end_index': int(victim['end_index']),
                'victim': victim['content'],
            })
        victim_entity.save()

    for injury in injuries:
        if (injury['content'].lower() == 'a'):
            injury['content'] = '1'
        injured = CasualtyEntity(
            seed=article,
            start_index=int(injury['start_index']),
            end_index=int(injury['end_index']),
            num=injury['content'],
            casualty_type=CasualtyType.INJURY.value)
        injured.save()

        victim = injury['victim']
        if (not victim):
            continue

        victim_entity, _ = VictimEntity.objects.update_or_create(
            seed=injured,
            defaults={
                'seed': injured,
                'start_index': int(victim['start_index']),
                'end_index': int(victim['end_index']),
                'victim': victim['content']
            })
        victim_entity.save()

    if (perpetrator_entity):
        perpetrator, _ = PerpetratorEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'start_index': int(perpetrator_entity['start_index']),
                'end_index': int(perpetrator_entity['end_index']),
                'perpetrator': perpetrator_entity['content']
            })
        perpetrator.save()

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
