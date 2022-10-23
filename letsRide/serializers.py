from rest_framework import serializers
from .models import RiderTravel, UserModel, Requester
class RiderSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = RiderTravel
        fields = (
            "id",
            "travel_from",
            "travel_to",
            "travel_date",
            "travel_time",
            "is_flexible",
            "asset_quantity",
            "medium",
            "name",
            "user_id",
            "requester",
            "status"
        )
    def get_name(self, obj):
        return obj.user_id.name
class RequesterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Requester
        fields = (
            "id",
            "pickup_from",
            "pickup_date",
            "pickup_time",
            "total_assets",
            "asset_type",
            "sensitivity",
            "deliver_to",
            "delivering_to",
            "name",
            "status",
            "user_id"
        )
    def get_name(self, obj):
        return obj.user_id.name

  
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "id",
            "name",
            "user_type"
        )
