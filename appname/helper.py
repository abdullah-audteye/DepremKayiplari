from .models import Ihbar, KayipUser, Tag, Countries, KayipStatus,IhbarUser
from datetime import datetime

def CleanBadRecords():
    ihbarlar = Ihbar.objects.filter(kayip_user__isnull=True).delete()

def FixNonHavingDates():
    date_time_str = '06/02/23 00:00:00'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
    ihbarlar = Ihbar.objects.filter(created_time__isnull=True).update(created_time=date_time_obj)
