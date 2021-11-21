from django.db import models

class User(models.Model):
    name = models.CharField(max_length=32, help_text='User Name')
    job_title = models.CharField(max_length=32, help_text='Job Title')

    #def as_dict(self):
    #    return {
    #        'id': self.id,
    #        'name': self.name,
    #        'job_title': self.job_title,
    #    }

class CommunicateInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='communicate_information')
    email = models.CharField(max_length=255, help_text='Email Address')
    mobile = models.CharField(max_length=12, help_text='Mobile Phone Number')

