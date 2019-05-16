from django import template
import re

register = template.Library()
a = re.compile(r'http://[^?]+\?id=([^&]+).*')

@register.filter
def extract_id(url):
  match = a.match(url)
  if match:
    return match.groups()[0]
  return url