from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'complaints', views.ComplaintViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'issue-category', views.IssueCatViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/', include(router.urls)),
]