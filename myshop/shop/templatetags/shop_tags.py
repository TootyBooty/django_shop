import os
import uuid
from django import template                                                                                                              
from django.conf import settings                                                                                                         

register = template.Library()                                                                                                            

@register.simple_tag(name='cache_bust')                                                                                                  
def cache_bust():                                                                                                                        

    if settings.DEBUG:                                                                                                                   
        version = uuid.uuid1()                                                                                                           
    else:                                                                                                                                
        version = os.environ.get('PROJECT_VERSION')                                                                                       
        if version is None:                                                                                                              
            version = '1'                                                                                                                

    return '__v__={version}'.format(version=version)

@register.simple_tag(name='language_path')  
def language_path(request, current_language_code, new_language_code):
    path = request.get_full_path()
    path = path.replace(current_language_code, new_language_code, 1)
    return path