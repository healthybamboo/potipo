from django.urls import path
from . import views
app_name ='pages'

urlpatterns = [
    path('termsofservice',views.TermsOfService.as_view(),name="ts"),
    path('messagefrommanager',views.MessageFromManager.as_view(),name="mm"),
]
