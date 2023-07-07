from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.urls import path, include
from django.contrib import admin



from .views import start_trip, end_trip


urlpatterns = [
    #path('snippets/', views.SnippetList.as_view()),
    #path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('ping/', views.PingList.as_view()),
    #path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('trip/', views.TripList.as_view()),
    path('trip-device/<int:device_id>/', views.TripDetail.as_view()),
    path('trip-history/', views.TripHistoryList.as_view()),
    path('trip-history-batch/', views.TripHistoryBatchList.as_view()),
    path('trip-drowsiness-batch/', views.TripDrowsinessBatchList.as_view()),
    path('trip-hands-off-batch/', views.TripHandsOffBatchList.as_view()),
    path('manager/', views.ManagerList.as_view()),
    path('driver/', views.DriverList.as_view()),
    path('trip-drowsiness/', views.TripDrowsinessList.as_view()),
    path('trip-hands-off/', views.TripHandsOffList.as_view()),
    path('admin/', admin.site.urls),
    path('start-trip/<int:trip_id>/', start_trip, name='start-trip'),
    path('end-trip/<int:trip_id>/', end_trip, name='end-trip'),
]

urlpatterns = format_suffix_patterns(urlpatterns)