from rest_framework import serializers
from .models import Host, ProcessSnapshot, Process

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'

class ProcessSnapshotSerializer(serializers.ModelSerializer):
    processes = ProcessSerializer(many=True, read_only=True)

    class Meta:
        model = ProcessSnapshot
        fields = ['id', 'timestamp', 'processes']

class HostSerializer(serializers.ModelSerializer):
    snapshots = ProcessSnapshotSerializer(many=True, read_only=True)

    class Meta:
        model = Host
        fields = ['hostname', 'snapshots']