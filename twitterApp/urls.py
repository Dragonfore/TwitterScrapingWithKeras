from django.urls import path

from . import views

app_name = 'twitterApp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('result.png/', views.index, name='index'),
    path('result.png/static/bestClassifier.json/', views.send_classifier_data, name="send_classifier_data")
]