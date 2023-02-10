from .models import Ihbar, KayipUser, Tag, Countries, KayipStatus,IhbarUser
from datetime import datetime
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_FROM_EMAIL = os.environ.get('MAIL_SENDGRID_FROM_EMAIL')
SENDGRID_API_KEY = os.environ.get('MAIL_SENDGRID_API_KEY')


def CleanBadRecords():
    ihbarlar = Ihbar.objects.filter(kayip_user__isnull=True).delete()

def FixNonHavingDates():
    date_time_str = '06/02/23 00:00:00'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
    ihbarlar = Ihbar.objects.filter(created_time__isnull=True).update(created_time=date_time_obj)




def SendAccessCode(to_email, dynamic_template_data):
    message = Mail(SENDGRID_FROM_EMAIL, to_email)
    message.dynamic_template_data = dynamic_template_data
    message.template_id = "d-1220bb5e2a3642a88c3380ac06bc7c52"

    

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(e)
