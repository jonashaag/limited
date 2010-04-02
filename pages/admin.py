from django.db.models.base import ModelBase
from django.contrib.admin import site as admin_site
from django.contrib.admin.sites import AlreadyRegistered, ModelAdmin
from limited.pages import models as limited_models
import models.admin

def register_model(*model):
    return admin_site.register(*model)

for obj in dir(limited_models):
    model = getattr(limited_models, obj)
    if not isinstance(model, ModelBase):
        continue
    admin_model = getattr(models.admin, '%sAdmin' % obj, None)
    try:
        register_model(model, admin_model)
    except AlreadyRegistered, e:
        print e
