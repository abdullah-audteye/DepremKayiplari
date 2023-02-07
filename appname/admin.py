from django.contrib import admin

# Register your models here.

from .models import Tag, IhbarUser, KayipUser, Ihbar

admin.site.register(Tag)
admin.site.register(IhbarUser)
admin.site.register(KayipUser)
admin.site.register(Ihbar)


