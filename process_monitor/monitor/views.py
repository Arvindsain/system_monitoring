from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Host, ProcessSnapshot, Process
from .serializers import ProcessSerializer, HostSerializer
from datetime import datetime
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Host, Process, ProcessSnapshot
from datetime import datetime

class ReceiveProcessData(APIView):
    def post(self, request):
        api_key = request.headers.get("X-API-KEY")
        if api_key != settings.API_KEY:
            return Response({"error": "Invalid API key"}, status=status.HTTP_403_FORBIDDEN)

        hostname = request.data.get("hostname")
        processes = request.data.get("processes", [])
        timestamp = request.data.get("timestamp", datetime.utcnow().isoformat())

        if not hostname:
            return Response({"error": "Hostname required"}, status=status.HTTP_400_BAD_REQUEST)

        # create or get host
        host, _ = Host.objects.get_or_create(hostname=hostname)

        # create snapshot
        snapshot = ProcessSnapshot.objects.create(host=host, timestamp=timestamp)

        # bulk insert processes
        process_objects = [
            Process(
                snapshot=snapshot,
                pid=p["pid"],
                parent_pid=p.get("ppid"),
                name=p["name"],
                cpu_percent=p.get("cpu_percent", 0),
                memory_mb=round((p.get("mem_rss", 0) or 0) / (1024*1024), 2)  # convert bytes → MB
            )
            for p in processes
        ]
        Process.objects.bulk_create(process_objects)

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)



class RetrieveProcessData(APIView):
    def get(self, request, hostname):
        host = get_object_or_404(Host, hostname=hostname)
        snapshot = get_object_or_404(ProcessSnapshot, host=host)
        process = Process.objects.filter(snapshot=snapshot)
        serializer = ProcessSerializer(process, many=True)
        return Response({
            "host": host.hostname,
            "timestamp": snapshot.timestamp,
            "processes": serializer.data
        })

class RetrieveHosts(APIView):
    def get(self, request):
        hosts = Host.objects.all()
        serializer = HostSerializer(hosts, many=True)
        return  Response(serializer.data)