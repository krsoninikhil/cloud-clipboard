from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from clipboard.models import Clip
from clipboard.serializers import ClipSerializer

def list_clips(request):
    """
    List the 20 most recently copied text. I am calling them 'clips'.
    """
    clips = Clip.objects.all()
    serializer = ClipSerializer(clips, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def copy(request):
    """
    Insert the data comming from devices to the database.
    """
    if request.method == 'POST':
        clip = JSONParser().parse(request)
        serializer = ClipSerializer(data=clip)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    return HttpResponse(status=404)

@csrf_exempt
def paste(request):
    """
    Sends the latest data copied.
    """
    if request.method == 'POST':
        updated_clip = JSONParser().parse(request)
        
        try:
            clip = Clip.objects.get(user_id=updated_clip['user_id'])
        except Clip.DoesNotExist:
            return HttpResponse(status=404)

        serializer = ClipSerializer(clip, data=updated_clip)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)
    return HttpResponse(status=404) 
