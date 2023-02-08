from django.contrib import admin

# Register your models here.

from .models import Tag, IhbarUser, KayipUser, Ihbar,TagArabic,KayipStatus

admin.site.register(Tag)
admin.site.register(TagArabic)
admin.site.register(IhbarUser)
admin.site.register(KayipUser)
admin.site.register(Ihbar)
admin.site.register(KayipStatus)


