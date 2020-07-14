from django.urls import path
from .appview import hardware_view

app_name = 'sr'
urlpatterns = [
    path('sr/hardware/to_hardware_list', hardware_view.to_hardware_list, name="hd_list"),
    path('sr/hardware/query', hardware_view.hardware_query),
    path('sr/hardware/by_id', hardware_view.by_id),
    path('sr/hardware/save', hardware_view.save),
    path('sr/hardware/delete', hardware_view.delete),
    path('sr/hardware/to_online_hardware', hardware_view.to_online_hardware),
    path('sr/hardware/query_online', hardware_view.query_online),
    path('sr/hardware/bind_hardware', hardware_view.bind_hardware),
    path('sr/hardware/get_box_mac', hardware_view.get_box_mac),
]
