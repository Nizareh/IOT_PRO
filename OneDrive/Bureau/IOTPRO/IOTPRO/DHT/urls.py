
from django.urls import path

from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path("api",api.Dlist,name='json'),
    path("api/post",api.Dhtviews.as_view(),name='json'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('',views.table,name='table'),
    
    path('Chart/',views.graphique,name='myChart'),
    path('chart-data/',views.chart_data, name='chart-data'),
    path('chart-data-jour/',views.chart_data_jour,name='chart-data-jour'),
    path('chart-data-semaine/',views.chart_data_semaine,name='chart-data-semaine'),
    path('chart-data-mois/',views.chart_data_mois,name='chart-data-mois'),
    path('tables/',views.tables,name="tables"),
    path('add/',views.add,name="add"),
    path("addrec/",views.addrec,name="addrec"),
    path('tables/delete/<int:id>/',views.delete,name="delete"),
    path('tables/update/<int:id>/',views.update,name="update"),
    path('tables/update/uprec/<int:id>/',views.uprec,name="uprec")
   
  
  
  
 

]

