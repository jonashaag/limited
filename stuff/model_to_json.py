import datetime
import time
try:
    import json
except ImportError:
    import simplejson as json

from django.core.management import setup_environ
from manage import settings
settings.DATABASE_NAME = settings.DATABASE_NAME2
setup_environ(settings)

from pages.models import Page as Model

_getattr = getattr
def getattr(obj, attr):
    attr = _getattr(obj, attr)
    if isinstance(attr, datetime.datetime):
        return int(time.mktime(attr.timetuple()))
    return attr

with open(Model._meta.object_name+'.json', 'w') as fobj:
    fields = map(lambda x:x.attname, Model._meta.fields)
    instances = []
    for obj in Model.objects.all().order_by('pk'):
        instances.append(dict(((field, getattr(obj, field)) for field in fields)))
    fobj.write(json.dumps(instances, indent=4))
