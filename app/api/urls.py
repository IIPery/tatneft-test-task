from django.urls import path, include

app_name = "api"

urlpatterns =[
    path('', include('app.api.auth.urls', namespace='auth')),
    path('', include('app.api.metrics.urls', namespace='metrics')),
]
