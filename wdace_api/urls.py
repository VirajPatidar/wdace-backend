from django.urls import path
from .views import TestView, ClassifyAnalyseView

urlpatterns = [

    path('classify', ClassifyAnalyseView.as_view(), name="classify"),
    path('test', TestView.as_view(), name="test"),

]