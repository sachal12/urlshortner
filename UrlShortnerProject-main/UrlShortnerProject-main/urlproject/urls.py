from django.urls import path
from .import views

urlpatterns = [
     path('',views.home,name="test"),
     path('all-analytics',views.all_analytics),
     # path('analytics/<slug:shorturl>/',views.analytic,name="analytic"),
     path('analytics/<int:id>/',views.analytic,name="analytic"),
     # path('analytics/cc-ranklist/<slug:shorturl>/',views.analytic,name="analytic"),
     path('<slug:shorturl>',views.redirect_url,name="redirect_url"),
     
]