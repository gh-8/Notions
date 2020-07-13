import random
from .serializers import NotionSerializer, NotionActionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .models import Notion
from .forms import NotionForm
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['POST'])  # http method that the client has to send is === POST
@permission_classes([IsAuthenticated])
def notion_create_view(request, *args, **kwargs):
    serializer = NotionSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])  # http method that the client has to send is === GET
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def notion_list_view(request, *args, **kwargs):
    qs = Notion.objects.all()
    serializer = NotionSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])  # http method that the client has to send is === GET
def notion_detail_view(request, notion_id, *args, **kwargs):
    qs = Notion.objects.filter(id=notion_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = NotionSerializer(obj)
    return Response(serializer.data, status=200)

# http method that the client has to send is === GET
@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def notion_delete_view(request, notion_id, *args, **kwargs):
    qs = Notion.objects.filter(id=notion_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this notion"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Notion deleted successfully"}, status=200)
# http method that the client has to send is === GET

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def notion_action_view(request, *args, **kwargs):
    '''
    Action options: like, unlike and share
    '''
    serializer = NotionActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        # print(data)
        notion_id = data.get("id")
        action = data.get("action")
        content=data.get("content")
        qs = Notion.objects.filter(id=notion_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = NotionSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "share":
            new_notion = Notion.objects.create(
                user=request.user, parent=obj, content=content,)
            serializer = NotionSerializer(new_notion)
            return Response(serializer.data, status=200)
    return Response({}, status=200)

def notion_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = NotionForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.is_ajax():
            # 201 == creatd items
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = NotionForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})

def notion_list_view_pure_django(request, *args, **kwargs):
    qs = Notion.objects.all()
    notion_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": notion_list,
    }
    return JsonResponse(data)

def notion_detail_view_pure_django(request, notion_id, *args, **kwargs):
    data = {
        "id": notion_id,
    }
    status = 200
    try:
        obj = Notion.objects.get(id=notion_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404
    return JsonResponse(data, status=status)
    # return HttpResponse(f"<h1>Hello, World! The notion id is {notion_id} - {obj.content}</h>")