import dateparser

import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from web.forms import HomeForm
from web.models import Article, DateEntity, LocationEntity, KilledEntity, InjuredEntity, PerpetratorEntity


class LabelHomeView(TemplateView):
    template_home = 'label.html'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_home, {'form':form})

    def post(self, request):
        form = HomeForm(request.POST)
        #form.save()
        if form.is_valid():
            urls = form.cleaned_data['urls']
            urls = urls.split()
        request.session['urls'] = urls
        args = {'form': form, 'urls': urls}
        return redirect(label_article, idx = 0)

def store_label(results, article):
    #['date', 'location', 'deaths', 'injured']
    date_entity = results.get('date', None)
    location_entity = results.get('location', None)
    killed_entity = results.get('deaths', None)
    injured_entity = results.get('injured', None)
    perpetrator_entity = results.get('perpetrator', None)

    if(date_entity):
        date_str = date_entity['content']
        print(dateparser.parse(date_str))
        date = DateEntity(seed=article, start_index=int(date_entity['start_index']), end_index=int(date_entity['end_index']), date_str=date_str, date=dateparser.parse(date_str))
        date.save()
    if(location_entity):
        location = LocationEntity(seed=article, start_index=int(location_entity['start_index']), end_index=int(location_entity['end_index']), location=location_entity['content'])
        location.save()
    if(killed_entity):
        killed = KilledEntity(seed=article, start_index=int(killed_entity['start_index']), end_index=int(killed_entity['end_index']), num_killed=int(killed_entity['content']))
        killed.save()
    if(injured_entity):
        injured = InjuredEntity(seed=article, start_index=int(injured_entity['start_index']), end_index=int(injured_entity['end_index']), num_injured=int(injured_entity['content']))
        injured.save()
    if(perpetrator_entity):
        perpetrator = PerpetratorEntity(seed=article, start_index=int(perpetrator_entity['start_index']), end_index=int(perpetrator_entity['end_index']), perpetrator=perpetrator_entity['content'])
        perpetrator.save()

    
@csrf_exempt
def label_article(request, idx = None):
    
    template_label_article = 'label_article.html'
    url = request.session['urls'][idx]
    article = Article.objects.get(url=url)
    
    if(request.method == 'POST'):
        results=request.POST.getlist('results[]')
        if(not results):
            pass 
        results = json.loads(request.body)
        print(results)
        store_label(results, article)

    #get title and body from DB
    return render(request, template_label_article, {'idx':idx, 'article':article, 'next':idx+1, 'prev':max(0,idx-1), 'article_url':url})