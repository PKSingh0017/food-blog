from django.contrib import admin
from . import models as core_models


admin.site.register(core_models.Category)
admin.site.register(core_models.Item)
admin.site.register(core_models.Testimonial)
admin.site.register(core_models.Carausel)
admin.site.register(core_models.Recipes)
admin.site.register(core_models.Blog)


