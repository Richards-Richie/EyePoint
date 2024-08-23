from django.urls import path
from . import views

urlpatterns = [
    # Example endpoint to start the video feed (if necessary)
    path('start/', views.start_video_feed, name='start_video_feed'),
    # Example endpoint to stop the video feed (if necessary)
    path('stop/', views.stop_video_feed, name='stop_video_feed'),
    # Add other endpoints as needed
]
