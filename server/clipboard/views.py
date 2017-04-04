from django.shortcuts import render
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from clipboard.models import Clip
from clipboard.serializers import ClipSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 


class ListClip(APIView):
    """
    List the most recently copied texts. I am calling them 'clips'.
    """
    def get(self, request):
        clips = Clip.objects.all()
        serializer = ClipSerializer(clips, many=True)
        return Response(serializer.data)

            
class CopyPaste(APIView):
    """
    Insert the data comming from devices to the database.
    """
    def get_clip(self, user_id):
        try:
            clip = Clip.objects.get(user_id=int(user_id))
        except Clip.DoesNotExist:
            raise Http404
    
    def post(self, request, user_id):
        serializer = ClipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        clip = self.get_clip(user_id)
        serializer = ClipSerializer(clip, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        clip = self.get_clip(user_id)
        serializer = ClipSerializer(clip)
        return Response(serializer.data)

