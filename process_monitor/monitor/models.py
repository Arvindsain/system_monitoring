from django.db import models

# Create your models here.

class Host(models.Model):
    hostname = models.CharField(max_length=255, unique=True)

class ProcessSnapshot(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Process(models.Model):
    snapshot = models.ForeignKey(ProcessSnapshot, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    pid = models.IntegerField()
    cpu_percent = models.FloatField()
    memory_mb = models.FloatField()
    parent_pid = models.IntegerField(null=True, blank=True)