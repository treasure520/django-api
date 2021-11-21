from rest_framework import serializers
from .models import User, CommunicateInformation

class CommunicateInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicateInformation
        fields = ('email', 'mobile')

class UserSerializer(serializers.ModelSerializer):
    communicate_information = CommunicateInformationSerializer(many=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'job_title', 'communicate_information']

    def create(self, validated_data):
        communicate_information = validated_data.pop('communicate_information')
        user = User.objects.create(**validated_data)
        CommunicateInformation.objects.create(user=user, **communicate_information)
        return user

    def update(self, instance, validated_data):
        communicate_information_data = validated_data.pop('communicate_information')
        instance.communicate_information.email = communicate_information_data.get('email', instance.communicate_information.email)
        instance.communicate_information.mobile = communicate_information_data.get('mobile', instance.communicate_information.mobile)
        instance.communicate_information.save()
        instance.name = validated_data.get('name', instance.name)
        instance.job_title = validated_data.get('job_title', instance.job_title)
        instance.save()
        return instance

