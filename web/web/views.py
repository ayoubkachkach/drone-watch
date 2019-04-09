import dateparser

import json
import simplejson

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from web.forms import HomeForm
from web.models import Article
from web.utils import get_labels
from web.utils import get_object_or_None
from web.utils import store_label


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


@csrf_exempt
def label_article(request, idx=0):
    max_idx = len(request.session['urls']) - 1
    if (idx > max_idx):
        return render(request, 'error_message.html', {
            'error_message':
            'index {} exceeds max index ({})'.format(idx, max_idx)
        })

    url = request.session['urls'][idx]
    article = get_object_or_None(Article, url=url)
    if (not article):
        return render(request, 'error_message.html', {
            'error_message':
            'No matching article found for url: {}'.format(url)
        })

    if (request.method == 'POST'):
        results = request.POST.getlist('results[]')
        if (not results):
            pass

        results = json.loads(request.body)
        store_label(results, article)

    labels = get_labels(article)
    print(labels)
    return render(
        request, 'label_article.html', {
            'idx': idx,
            'article': article,
            'next': idx + 1,
            'prev': max(0, idx - 1),
            'article_url': url,
            'loadedLabels': simplejson.dumps(labels),
            'articleType': simplejson.dumps(article.article_type),
            'is_labeled': article.is_ground_truth,
            'id': article.id
        })
