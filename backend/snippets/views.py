from snippets.models import Snippet, Ping, Manager, Trip, TripHistory, Driver, TripDrowsiness, TripHandsOff
from snippets.serializers import SnippetSerializer
from rest_framework import generics, status
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer, PingSerializer, ManagerSerializer, TripSerializer, \
    TripHistorySerializer, DriverSerializer, TripDrowsinessSerializer, TripHandsOffSerializer
from rest_framework import permissions
from rest_framework.response import Response
from snippets.permissions import IsOwnerOrReadOnly


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from django.shortcuts import redirect
from datetime import datetime


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class PingList(generics.ListCreateAPIView):
    queryset = Ping.objects.all()
    serializer_class = PingSerializer

    def perform_create(self, serializer):
        serializer.save()


class PingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ping.objects.all()
    serializer_class = PingSerializer


class ManagerList(generics.ListCreateAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def perform_create(self, serializer):
        serializer.save()


class ManagerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class TripList(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        serializer.save()


class TripDetail(generics.ListAPIView):
    queryset = Trip.objects.all().first()
    serializer_class = TripSerializer
    lookup_field = "device_id"

    def get_queryset(self):
        return Trip.objects.filter(device_id=self.kwargs['device_id']).order_by('-real_start')

class TripHistoryList(generics.ListCreateAPIView):
    queryset = TripHistory.objects.all()
    serializer_class = TripHistorySerializer

    def perform_create(self, serializer):
        serializer.save()


class TripHistoryBatchList(generics.ListCreateAPIView):
    queryset = TripHistory.objects.all()
    serializer_class = TripHistorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripHistoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TripHistory.objects.all()
    serializer_class = TripHistorySerializer


class DriverList(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def perform_create(self, serializer):
        serializer.save()


class DriverDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class TripDrowsinessList(generics.ListCreateAPIView):
    queryset = TripDrowsiness.objects.all()
    serializer_class = TripDrowsinessSerializer

    def perform_create(self, serializer):
        serializer.save()


class TripDrowsinessBatchList(generics.ListCreateAPIView):
    queryset = TripDrowsiness.objects.all()
    serializer_class = TripDrowsinessSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripDrowsinessDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TripDrowsiness.objects.all()
    serializer_class = TripDrowsinessSerializer


class TripHandsOffList(generics.ListCreateAPIView):
    queryset = TripHandsOff.objects.all()
    serializer_class = TripHandsOffSerializer

    def perform_create(self, serializer):
        serializer.save()


class TripHandsOffBatchList(generics.ListCreateAPIView):
    queryset = TripHandsOff.objects.all()
    serializer_class = TripHandsOffSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripHandsOffDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TripHandsOff.objects.all()
    serializer_class = TripHandsOffSerializer


def start_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    # Lógica para iniciar a viagem...
    if trip.is_started == False:
        trip.is_started = True
        trip.real_start = datetime.now()
        trip.save()
    # Redirecionar o usuário para a página atual
    return redirect(request.META['HTTP_REFERER'])

def end_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    # Lógica para iniciar a viagem...

    if trip.is_ended == False and trip.is_started == True:
        trip.is_ended = True   
        trip.real_end = datetime.now()
        trip.save()

    # Redirecionar o usuário para a página atual
    return redirect(request.META['HTTP_REFERER'])
