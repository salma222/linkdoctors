from mysite.models import Doctor
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from linkedin import linkedin
from mysite.settings import *

def linkedin_login(request):
  RETURN_URL = request.build_absolute_uri("linkedin_login")
  # url goes back to request

  # create authentication class:
  authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
  
  print(authentication)  

  # now its passed to the app:
  #application = linkedin.LinkedInApplication(authentication)

  code = request.GET.get('code')

  if code:
    authentication.authorization_code = code
    authentication.get_access_token()
    # save in DB
    doctor = Doctor.create_from_token(authentication)
    user = User.objects.get(id=doctor.user_id)

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect("/publish_case")

  # if I dont have code, ask for another one
  return HttpResponseRedirect(authentication.authorization_url)
