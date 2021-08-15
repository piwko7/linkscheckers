from django.urls import path
from .views import new_project, update_project, index, load_project, delete_project, check_url

urlpatterns = [
    path('', index, name='index'),
    path('new', new_project, name='new_project'),
    path('project/<int:id>/', load_project, name='load_project'),
    path('update/<int:id>/', update_project, name='update_project'),
    path('delete/<int:id>/', delete_project, name='delete_project'),
    path('check/', check_url, name='check_url'),

]
