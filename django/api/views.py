from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User, CommunicateInformation
from .serializers import UserSerializer, CommunicateInformationSerializer

class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context['indent'] = 2
        return context


#class UserListView(generics.ListCreateAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#
#    def get_renderer_context(self):
#        context = super().get_renderer_context()
#        context['indent'] = 2
#        return context
#
#class UserView(generics.RetrieveUpdateDestroyAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#
#    def get_renderer_context(self):
#        context = super().get_renderer_context()
#        context['indent'] = 2
#        return context
#
#
#class CommunicateInformationListView(generics.ListCreateAPIView):
#    queryset = CommunicateInformation.objects.all()
#    serializer_class = CommunicateInformationSerializer
#
#    def get_renderer_context(self):
#        context = super().get_renderer_context()
#        context['indent'] = 2
#        return context
#
#class CommunicateInformationView(generics.RetrieveUpdateDestroyAPIView):
#    queryset = CommunicateInformation.objects.all()
#    serializer_class = CommunicateInformationSerializer
#
#    def get_renderer_context(self):
#        context = super().get_renderer_context()
#        context['indent'] = 2
#        return context

