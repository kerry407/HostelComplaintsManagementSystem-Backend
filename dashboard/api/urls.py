from django.urls import path, include
from . import views 
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register("students", views.StudentViewSet, basename="students")
routers.register("porters", views.PorterViewSet, basename="porters")
routers.register("hostels", views.HostelViewSet, basename="hostels")

urlpatterns = [
    path("", include(routers.urls)),
    path('complaints/create/', views.ComplaintsViewSet.as_view({'post': 'create'}), name='create-complaint'),
    path('complaints/', views.ComplaintsViewSet.as_view({'get':'list'}), name='complaints-list'),
    path('complaints/<str:pk>/', views.ComplaintsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='complaint-details'),
    path('dashboard-count/', views.DashBoardCountView.as_view(), name='dashboard-count'),
]
