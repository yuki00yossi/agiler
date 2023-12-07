from django.shortcuts import render
from rest_framework import viewsets

from project.serializer import ProjectSerializer
from project.models import Project

# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    """ プロジェクトのビュー """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
