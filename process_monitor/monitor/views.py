from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Host, ProcessSnapshot, Process
from .serializers import ProcessSerializer
from datetime import datetime
from django.conf import settings

class ReceiveProcessData(APIView):
    def post(self, request):
        if request.headers.get('X-API-KEY') != settings.API_KEY:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        hostname = data.get('hostname')
        processes = data.get('processes')
        timestamp = datetime.now()

        if not hostname or not processes:
            return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

        host, _ = Host.objects.get_or_create(hostname=hostname)
        snapshot = ProcessSnapshot.objects.create(host=host, timestamp=timestamp)

        for proc in processes:
            Process.objects.create(
                snapshot=snapshot,
                name=proc['name'],
                pid=proc['pid'],
                cpu_percent=proc['cpu_percent'],
                memory_mb=proc['memory_mb'],
                parent_pid=proc.get('parent_pid')
            )

        return Response({'message': 'Data received'}, status=status.HTTP_201_CREATED)

class RetrieveProcessData(APIView):
    def get(self, request, hostname):
        host = get_object_or_404(Host, hostname=hostname)
        timestamp = request.GET.get('timestamp')
        if timestamp:
            snapshot = get_object_or_404(ProcessSnapshot, host=host)
        else:
            snapshot = host.processsnapshot_set.latest('timestamp')
        process = Process.objects.filter(snapshot=snapshot)
        serializer = ProcessSerializer(process, many=True)
        return Response({
            "host": host.hostname,
            "timestamp": snapshot.timestamp,
            "processes": serializer.data
        })