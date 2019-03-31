import dateparser

import simplejson
import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from web.forms import HomeForm
from web.models import Article, DateEntity, LocationEntity, KilledEntity, InjuredEntity, PerpetratorEntity, Types


class LabelHomeView(TemplateView):
    template_home = 'label.html'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_home, {'form': form})

    def post(self, request):
        form = HomeForm(request.POST)
        #form.save()
        if form.is_valid():
            urls = form.cleaned_data['urls']
            urls = urls.split()
        request.session['urls'] = urls
        args = {'form': form, 'urls': urls}
        return redirect(label_article, idx=0)


def store_label(results, article):
    #['date', 'location', 'deaths', 'injured']
    date_entity = results.get('date', None)
    location_entity = results.get('location', None)
    killed_entity = results.get('killed', None)
    injured_entity = results.get('injured', None)
    perpetrator_entity = results.get('perpetrator', None)
    article_type = results.get('article_type', None)
    
    DateEntity.objects.filter(seed=article).delete()
    LocationEntity.objects.filter(seed=article).delete()
    KilledEntity.objects.filter(seed=article).delete()
    InjuredEntity.objects.filter(seed=article).delete()
    PerpetratorEntity.objects.filter(seed=article).delete()
    
    if(not article_type):
        article_type = Types.NOT_DRONE.value
    else:
        article_type = getattr(Types, article_type).value

    article.is_ground_truth = True
    article.article_type = article_type

    if(article_type == Types.STRIKE):
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
    if (location_entity):
        location, _ = LocationEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'start_index': int(location_entity['start_index']),
                'end_index': int(location_entity['end_index']),
                'location': location_entity['content']
            })
        #location.save()
    if (killed_entity):
        killed, _ = KilledEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'start_index': int(killed_entity['start_index']),
                'end_index': int(killed_entity['end_index']),
                'num_killed': int(killed_entity['content'])
            })
        #killed.save()
    if (injured_entity):
        injured, _ = InjuredEntity.objects.update_or_create(
            seed=article,
            defaults={
                'seed': article,
                'start_index': int(injured_entity['start_index']),
                'end_index': int(injured_entity['end_index']),
                'num_injured': int(injured_entity['content'])
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

def get_labels_dict(article):
    entity_labels = {}
    entity_labels['date'] = get_related_object(article, 'date_entity')
    entity_labels['location'] = get_related_object(article, 'location_entity')
    entity_labels['killed'] = get_related_object(article, 'killed_entity')
    entity_labels['injured'] = get_related_object(article, 'injured_entity')
    entity_labels['perpetrator'] = get_related_object(article, 'perpetrator_entity')
    if(entity_labels['date']):
        entity_labels['date'] = entity_labels['date'].__dict__

    if(entity_labels['location']):
        entity_labels['location'] = entity_labels['location'].__dict__

    if(entity_labels['killed']):
        entity_labels['killed'] = entity_labels['killed'].__dict__

    if(entity_labels['injured']):
        entity_labels['injured'] = entity_labels['injured'].__dict__

    if(entity_labels['perpetrator']):
        entity_labels['perpetrator'] = entity_labels['perpetrator'].__dict__

    entity_labels = {key:val for key, val in entity_labels.items() if val is not None}

    return entity_labels


@csrf_exempt
def label_article(request, idx=None):

    template_label_article = 'label_article.html'
    url = request.session['urls'][idx]
    article = Article.objects.get(url=url)

    if (request.method == 'POST'):
        results = request.POST.getlist('results[]')
        if (not results):
            pass
        results = json.loads(request.body)
        store_label(results, article)
    labels = get_labels_dict(article)
    key_to_remove = '_state'
    for key in labels.keys():
        if labels[key] and key_to_remove in labels[key]:
            del labels[key][key_to_remove]

    #get title and body from DB
    return render(
        request, template_label_article, {
            'idx': idx,
            'article': article,
            'next': idx + 1,
            'prev': max(0, idx - 1),
            'article_url': url,
            'loadedLabels': simplejson.dumps(labels),
            'articleType': simplejson.dumps(article.article_type)
        })
