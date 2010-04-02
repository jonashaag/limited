import datetime
try:
    import json
except ImportError:
    import simplejson as json

from django.core.management import setup_environ
from manage import settings
setup_environ(settings)
from django.contrib.auth.models import User

from pages.models import Page as Model
for obj in Model.objects.all():
    obj.delete()

merge = {'edited':'edit_time', 'created':'creation_time'}

with open(Model._meta.object_name+'.json') as fobj:
    for index, dic in enumerate(json.load(fobj)):
        m = Model()
        for key, value in dic.iteritems():
            if key == 'user':
                setattr(m, 'user', User.objects.all()[0])
            elif key in merge:
                setattr(m, merge[key], datetime.datetime.fromtimestamp(int(value)))
            else:
                setattr(m, key, value)
        m.save()
        print m.id
