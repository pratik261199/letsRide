from .models import Requester
from datetime import datetime
from datetime import date
from django.db.models import Q
def check_expiry( user_id):
    date_today = date.today()
    c_time = datetime.now()
    c_time = c_time.strftime("%H:%M:%S")
    queryset = Requester.objects.filter((Q(pickup_date__lte = date_today) | Q(pickup_time__lte = c_time)), status = "Pending", pickup_date__lt = date_today).update(status ="Expired")
    return True
