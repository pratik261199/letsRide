from django.db import models
import uuid



class UserModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, max_length=255)
    user_type = models.CharField(
        null=False, blank=False, max_length=32, choices=(('RIDER','rider'), ('REQUESTER', 'requester'))
    )
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'users'

class Requester(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    pickup_from = models.CharField(blank=True, null = False, max_length=64)
    deliver_to = models.CharField(blank=True, null = False, max_length=64)
    pickup_date = models.DateField(null = True, blank = True)
    pickup_time = models.TimeField(null = True, blank = True)
    total_assets = models.IntegerField(null = True, blank = True)
    asset_type = models.CharField(
        null=True, blank=True, max_length=32, choices=(('LAPTOP','Laptop'), ('TRAVEL_BAG','Travel bag'), ('PACKAGE', 'Package'))
    )
    user_id = models.ForeignKey(
        UserModel,
        null=True,
        blank=True,
        related_name="requester_travel",
        on_delete=models.SET_NULL,
    )
    sensitivity = models.CharField(
        null=True, blank=True, max_length=32,   choices=(('HIGHLY_SENSITIVE', 'Highly sensetive'), ('SENSITIVE','Sensetive'),('NORMAL', 'Normal'))
    )
    delivering_to = models.CharField(blank=True, null=True, max_length=64)
    status = models.CharField(
        null=True, blank=True, max_length=32, choices=(('Pending','pending'),('Expired', 'expired')), default = 'Pending'
    )
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'requester'

class RiderTravel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    travel_from  = models.CharField(blank=True, null = False, max_length=64)
    travel_to = models.CharField(blank=True, null = False, max_length=64)
    travel_date = models.DateField(null = True, blank = True)
    travel_time = models.TimeField(null = True, blank = True)
    is_flexible = models.BooleanField(default = False)
    medium = models.CharField(
        null=False, blank=False, max_length=32, choices=(('BUS','Bus'), ('CAR', 'Car'), ('TRAIN', 'Train'))
    )
    asset_quantity = models.IntegerField()
    user_id = models.ForeignKey(
        UserModel,
        null=True,
        blank=True,
        related_name="rider_travel",
        on_delete=models.SET_NULL,
    )
    status = models.CharField(
        null=False, blank=False, max_length=32, choices=(('APPLIED', 'Applied'),('NOT_APPLIED', 'Not applied')), default = 'NOT_APPLIED'
    )
    requester = models.OneToOneField(
        Requester, related_name="riders", null = True, on_delete=models.SET_NULL,
    )
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'rider_travel'



