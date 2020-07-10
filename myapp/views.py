from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404, JsonResponse
import random

from .models import Notion
from .forms import NotionForm

# Create your views here.

def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Here here</h1>")
    return render(request,"pages/home.html",context={},status=200)

def notion_detail_view(request, notion_id, *args, **kwargs):
    """
    REST API View
    return json data
    """
    data = {
        "id": notion_id,
    }
    status = 200
    try:
        obj = Notion.objects.get(id=notion_id)
        data['content']=obj.content
        #"image_path": obj.image.url,
    except:
        data['message']="Not Found"
        status = 404


    return JsonResponse(data, status=status)
    #return HttpResponse(f"<h1>The notion id is: {notion_id} - {obj.content}</h1>")

def notion_list_view(request, *args, **kwargs):
    query_set = Notion.objects.all()
    notion_list = [{"id": x.id, "content":x.content, "likes": random.randint(0,100)} for x in query_set]
    data = {
        "isUser": False,
        "response": notion_list
    }
    return JsonResponse(data)

def notion_create_view(request, *args, **kwargs):
    form = NotionForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None:
            return redirect(next_url)
        form = NotionForm()
    return render(request, 'components/form.html', context={"form": form})