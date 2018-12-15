from django.urls import path
from . import views

app_name = 'map'

urlpatterns = [
    path('',views.index,name='index'),
    path('map-view/',views.map_view,name='map-view'),
    path('category/',views.category,name='category'),
    path('features/',views.get_features,name='features'),
    path('area/',views.get_area,name='area'),
    path('about/',views.about,name='about'),
    path('response/',views.submit_response,name='submit-response'),
    # path('<int:question_id>/',views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]