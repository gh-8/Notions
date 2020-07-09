from django.shortcuts import render
from django.http import HttpResponse,Http404, JsonResponse

from .models import Notion

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
    notion_list = [{"id": x.id, "content":x.content} for x in query_set]
    data = {
        "isUser": False,
        "response": notion_list
    }
    return JsonResponse(data)

