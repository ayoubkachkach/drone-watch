from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView
from web.forms import HomeForm
from web.models import Article
from django.views.decorators.csrf import csrf_exempt
import json


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

@csrf_exempt
def label_article(request, idx = None):
    if(request.method == "POST"):
        results=request.POST.getlist('results[]')
        if(not results):
            pass 
        results = json.loads(request.body)
        print(results)
        
    template_label_article = 'label_article.html'
    url = request.session['urls'][idx]
    article = Article.objects.get(url=url)
    #get title and body from DB
    return render(request, template_label_article, {'idx':idx, 'article':article, 'next':idx+1, 'prev':max(0,idx-1)})
    