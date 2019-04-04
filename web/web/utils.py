from django.shortcuts import _get_queryset
from text2digits import text2digits
from web.models import Article
from web.models import CasualtyEntity
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

    t2d = text2digits.Text2Digits()

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
            num_killed = 1
        num_killed = t2d.convert(killed_entity['content'])
        killed, _ = KilledEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'start_index': int(killed_entity['start_index']),
                'end_index': int(killed_entity['end_index']),
                'num_killed': int(num_killed)
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


def make_labels_dict(article):
    entity_labels = {}
    entity_labels['date'] = get_related_object(article, 'date_entity')
    entity_labels['location'] = get_related_object(article, 'location_entity')
    entity_labels['killed'] = get_related_object(article, 'killed_entities')
    entity_labels['injured'] = get_related_object(article, 'injured_entities')
    entity_labels['perpetrator'] = get_related_object(article,
                                                      'perpetrator_entity')
    if (entity_labels['date']):
        entity_labels['date'] = entity_labels['date'].__dict__

    if (entity_labels['location']):
        entity_labels['location'] = entity_labels['location'].__dict__

    if (entity_labels['killed']):
        entity_labels['killed'] = killed_entity.entity_labels['killed'].all

    if (entity_labels['injured']):
        entity_labels['injured'] = entity_labels['injured'].__dict__

    if (entity_labels['perpetrator']):
        entity_labels['perpetrator'] = entity_labels['perpetrator'].__dict__

    entity_labels = {
        key: val for key, val in entity_labels.items() if val is not None
    }

    key_to_remove = '_state'
    for key in entity_labels.keys():
        if entity_labels[key] and key_to_remove in entity_labels[key]:
            if (key == 'date'):
                del entity_labels['date']['date']
            del entity_labels[key][key_to_remove]

    return entity_labels