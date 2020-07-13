from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404, JsonResponse
import random
from django.utils.http import is_safe_url
from django.conf import settings

from .serializers import NotionSerializer, NotionActionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .models import Notion
from .forms import NotionForm

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Here here</h1>")
    return render(request,"pages/home.html",context={},status=200)


@api_view(['GET']) #method the client send is get
def notion_detail_view(request, notion_id, *args, **kwargs):
    query_set = Notion.objects.filter(id=notion_id)
    if not query_set.exists():
        return Response({},status=404)
    obj = query_set.first()
    serializer = NotionSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE','POST']) #method the client send is delete or post
@permission_classes([IsAuthenticated]) #user needs to be authenticated
def notion_delete_view(request, notion_id, *args, **kwargs):
    query_set = Notion.objects.filter(id=notion_id)
    if not query_set.exists():
        return Response({},status=404)
    query_set = query_set.filter(user=request.user)
    if not query_set.exists():
        return Response({"message":"you cannot delete this notion"},status=404)
    obj = query_set.first()
    obj.delete()
    return Response({"message":"Notion deleted"}, status=200)

@api_view(['GET']) #method the client send is get
def notion_list_view(request, *args, **kwargs):
    query_set = Notion.objects.all()
    serializer = NotionSerializer(query_set, many=True)
    return Response(serializer.data)

@api_view(['POST']) #method the client send is post
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated]) 
def notion_create_view(request, *args, **kwargs):
    serializer = NotionSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({},status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def notion_like_toggle_view(request, *args, **kwargs):
    '''
    pre: id is required, user is logged in
    Action options are: like, unlike, share
    '''
    serializer = NotionActionSerializer(request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        notion_id = data.get("id")
        action = data.get("action")

        qs = Notion.objects.filter(id=notion_id)
        if not qs.exists():
            return Response({},status=404)
        obj.qs.first()
        if action == "like":
            obj.likes.add(request.user)
        elif action=="unlike":
            obj.likes.remove(request.user)
        elif action == "share":
            pass #todo

    return Response({"message": "Notion"},status=200)`

def notion_detail_view_pure_django(request, notion_id, *args, **kwargs):
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

def notion_list_view_pure_django(request, *args, **kwargs):
    query_set = Notion.objects.all()
    notion_list = [x.serialize() for x in query_set]
    data = {
        "isUser": False,
        "response": notion_list
    }
    return JsonResponse(data)

def notion_create_view_pure_django(request, *args, **kwargs):
    # print("ajax",request.is_ajax())
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({},status=401)
        return redirect(settings.LOGIN_URL)
    form = NotionForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(),status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = NotionForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})