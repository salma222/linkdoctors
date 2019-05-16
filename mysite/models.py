from django.db import models
from linkedin.models import AccessToken
from linkedin import linkedin
from django.contrib.auth.models import User
from mysite.settings import *
import re

# Create your views here.
class Doctor(models.Model):
  name=models.CharField(max_length=200)
  user_id=models.IntegerField()
  linked_id=models.CharField(max_length=200)
  token=models.CharField(max_length=200)
  token_expires=models.CharField(max_length=200)
  
  @classmethod
  def create_from_token(cls, authentication):
    application = linkedin.LinkedInApplication(authentication)
    token = authentication.token
    
    profile=application.get_profile(selectors=['id', 'first-name'])
    doctor = Doctor.objects.filter(linked_id=profile['id']).first()
    if doctor:
      return doctor
    
    user = User()
    user.save()
    
    doctor = Doctor() #TODO get linkedin id and info and put it in the model attributes
    doctor.linked_id=profile['id']
    doctor.name=profile['firstName']
    doctor.user_id = user.id
    
    doctor.token = token.access_token
    doctor.token_expires = token.expires_in
    
    doctor.save()
    return doctor

  def get_li_application(self):
    authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, "", linkedin.PERMISSIONS.enums.values())
    authentication.token = AccessToken(self.token, self.token_expires)
    application = linkedin.LinkedInApplication(authentication)
    return application
    
  def get_li_doctors_connections(self):
    connections=self.get_li_application().get_connections()
    return [c for c in connections['values'] if c.has_key('industry') and c['industry'] == "Computer Software"]

  def __str__(self):
    return self.name

class Case(models.Model):
  doctor=models.ForeignKey(Doctor)
  name=models.CharField(max_length=200)
  problem=models.TextField()
  age=models.CharField(max_length=200)
  gender=models.CharField(max_length=10)

  def post_on_li(self):
    app = self.doctor.get_li_application()
    app.submit_share(
      comment='%s : %s' % (self.name, self.problem)
      )

  def __str__(self):
    return self.name


