from django.contrib import admin

# Register your models here.
from .models import Section
from .models import Drink
from .models import Topping,Chart
admin.site.register(Section)
admin.site.register(Drink)
admin.site.register(Topping)
admin.site.register(Chart)