from django.urls import path

from .appview import kt_main_view


app_name = 'zhkt'
urlpatterns = [
    path('main/to_zhkt_list', kt_main_view.to_zhkt_list, name="zhkt_list"),
    path('main/zhkt_query', kt_main_view.zhkt_query),
    path('main/by_id/<str:id>', kt_main_view.by_id),
]
