from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from mysite.models import *
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

def index(request):
  template = loader.get_template('index.html')
  context = RequestContext(request)
  return HttpResponse(template.render(context))

@login_required
def share_case(request, case_id):
  doctor=Doctor.objects.get(user_id=request.user.id)
  case=Case.objects.get(id=case_id)
    
  subject=case.name
  

  template = loader.get_template('share_case.html')
  context = RequestContext(request, {
    'doctor': doctor,
    'connections': doctor.get_li_doctors_connections(),
    'subject': subject
  })
  
  return HttpResponse(template.render(context))

@login_required
def publish_case(request):
  CASE_NAME="case_name"
  CASE_SPECICALTY="case_speciality"
  CASE_DESCRIPTIOn="case_description"
  doctor_id=1

  doctor=get_object_or_404(Doctor, id=doctor_id)

  template = loader.get_template('publish_case.html')
  context = RequestContext(request,{
    'doctor' : doctor
  })
  name=request.POST.get(CASE_NAME)
  speciality=request.POST.get(CASE_SPECICALTY)
  description=request.POST.get(CASE_DESCRIPTIOn)

  if not request.POST:
    return HttpResponse(template.render(context))

  case = Case()
  case.doctor=doctor
  case.name=name
  case.problem=description
  case.post_on_li()
  case.save()
  return HttpResponseRedirect("/case/%s/share" % case.id)
