from django.urls import path

from .views import (
    GenresListAPIView,
    ArtistsListApiView,
    ConcertListApiView,
    ConcertDetailApiView,
    create_checkout_session
)


urlpatterns = [
    path('genres/', GenresListAPIView.as_view()),
    path('artists/', ArtistsListApiView.as_view()),
    path('concerts/', ConcertListApiView.as_view()),
    path('concerts/<slug:slug>/', ConcertDetailApiView.as_view(), name='concert-detail'),
    path('concerts/<slug:slug>/purchase/', create_checkout_session)
]
