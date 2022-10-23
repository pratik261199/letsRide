from rest_framework import viewsets, parsers, status, permissions
from stack_data import Serializer
from .models import RiderTravel, Requester, UserModel
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import RiderPagination
from .serializers import RiderSerializer, UserSerializer, RequesterSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .filters import RequesterFilter
from .utils import check_expiry
class RiderViewSet(viewsets.ModelViewSet):
    model = RiderTravel
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = RiderTravel.objects.none()
    parser_classes = (parsers.JSONParser,)
    serializer_class = RiderSerializer
    pagination_class = RiderPagination
    # filter_backends = (DjangoFilterBackend,)
    def get_queryset(self):
        queryset = RiderTravel.objects.all()
        return queryset

    def get_serializer_context(self):
        context = super(RiderViewSet, self).get_serializer_context()
        context.update(context={"request_user": self.request.user})
        return context

    def get_serializer_class(self):
        if self.action in ["update", "retrieve", "partial_update", "create"]:
            return RiderSerializer
        elif self.action in ["list"]:
            return RiderSerializer

    def create(self, request, *args, **kwargs):
        serializer = RiderSerializer(
            data=request.data #, context={"request_user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = RiderSerializer(
            instance, data=request.data, context={"request_user": request.user}, partial = partial
        )
        serializer.is_valid(raise_exception=True)        
        serializer.save(created_by = request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=["GET"])
    def matched_requests(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        req_queryset = Requester.objects.filter(user_id = request.query_params.get("user_id"))
        queryset = queryset.filter(travel_date__in = req_queryset.values_list("pickup_date", flat = True),
            travel_from__in = req_queryset.values_list("pickup_from", flat = True),
            travel_to__in = req_queryset.values_list("deliver_to", flat = True) )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RiderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RiderSerializer(queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BaseModelViewSet(viewsets.ModelViewSet):
    class Meta(object):
        abstract = True
class UserViewSet(BaseModelViewSet):
    model = UserModel
    permission_classes = (
    )
    queryset = UserModel.objects.all()
    parser_classes = (parsers.JSONParser,)
    serializer_class = UserSerializer
    # pagination_class = RiderPagination
    filter_backends = (DjangoFilterBackend,)
    # filter_class = QuadrantFilter
    def get_queryset(self):
        queryset = UserModel.objects.none()
        if self.action in ["create", "update", "retrieve", "list"]:
            queryset = UserModel.objects.all()
        return queryset


    def get_serializer_context(self):
        context = super(UserViewSet, self).get_serializer_context()
        context.update(context={"request_user": self.request.user})
        return context

    def get_serializer_class(self):
        if self.action in ["update", "retrieve", "partial_update", "create", "list"]:
            return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(
            data=request.data #, context={"request_user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequesterViewSet(viewsets.ModelViewSet):
    model = Requester
    permission_classes = (
    #    permissions.IsAuthenticated,
    )
    queryset = Requester.objects.all()
    parser_classes = (parsers.JSONParser,)
    serializer_class = RequesterSerializer
    # pagination_class = RiderPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RequesterFilter
    def get_queryset(self):
        queryset = Requester.objects.none()
        if self.action in ["create", "update", "retrieve", "list", "destroy", "list_requests", "matched_requests"]:
            queryset = Requester.objects.all()
        return queryset

    # def destroy(self, request, *args, **kwargs):
    #     return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 
    def get_serializer_context(self):
        context = super(RequesterViewSet, self).get_serializer_context()
        context.update(context={"request_user": self.request.user})
        return context

    def get_serializer_class(self):
        if self.action in ["update", "retrieve", "partial_update", "create", "list"]:
            return RequesterSerializer

    def create(self, request, *args, **kwargs):
        serializer = RequesterSerializer(
            data=request.data #, context={"request_user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["GET"])
    def list_requests(self, request, *args, **kwargs):
        check_expiry(request.query_params.get("user_id"))
        queryset = self.get_queryset()
        queryset = queryset.filter(user_id = request.query_params.get("user_id")).orrde_by("-pickup_date", "-pickup_time")
        queryset = self.filter_queryset(queryset)
        serializer = RequesterSerializer(queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
