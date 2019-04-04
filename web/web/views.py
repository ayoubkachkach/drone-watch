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
from web.utils import make_labels_dict
from web.utils import get_related_object
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
    if (idx >= len(request.session['urls'])):
        return render(request, 'no_article.html')

    url = request.session['urls'][idx]
    article = Article.objects.get(url=url)
    if (request.method == 'POST'):
        results = request.POST.getlist('results[]')
        if (not results):
            pass
        results = json.loads(request.body)
        store_label(results, article)

    labels = make_labels_dict(article)

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
