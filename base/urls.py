from django.urls import path

from .appview import user_views, config_view, file_opt_view, terminal_equ_view
from .appview import log_view
from base.socket_manager import service_regist

app_name = 'base'
urlpatterns = [
    # 用户管理
    path('base/user/to_user_list', user_views.to_user_list, name="user_list"),
    path('base/user/user_query', user_views.user_query),
    # 参数管理
    path('base/config/to_config_list', config_view.to_config_list, name="config_list"),
    path('base/config/config_query', config_view.config_query),
    path('base/config/by_id', config_view.by_id),
    path('base/config/save', config_view.save),
    path('base/config/delete', config_view.delete),
    # 附件操作
    path('sys/file/down_from_remote', file_opt_view.down_from_remote),
    path('sys/file/up_file_to_sch', file_opt_view.up_file_to_sch),
    path('sys/file/downloadById', file_opt_view.downloadById),
    path('sys/file/viewPic', file_opt_view.viewPic),
    path('sys/file/viewThumbPic', file_opt_view.viewThumbPic),
    path('sys/file/viewMp4', file_opt_view.viewMp4),
    path('upload/<path:relative_path_name>', file_opt_view.downByRelativePath),  # 基于upload路径预览(path匹配任何非空字符串, 包含路径分隔符)
    # 日志管理
    path('base/log/to_log_list', log_view.to_log_list, name="log_list"),
    path('base/log/log_query', log_view.log_query),
    path('base/log/by_id', log_view.by_id),
    # 服务注册
    path('base/service/service_regist', service_regist),
    # 终端设备绑定
    path('base/terminal/to_terminal_equ_list', terminal_equ_view.to_terminal_equ_list, name="terminal_equ_list"),
    path('base/terminal/equ_query', terminal_equ_view.equ_query),
    path('base/terminal/save_ytj_equ', terminal_equ_view.save_ytj_equ),  # 保存一个一体机终端设置
    path('base/terminal/by_id', terminal_equ_view.by_id),
    path('base/terminal/save', terminal_equ_view.save),
    path('base/terminal/delete', terminal_equ_view.delete),
    path('base/terminal/batch_set_times', terminal_equ_view.batch_set_times),  # 批量设置开关机时间
    path('base/terminal/my_online_ps', terminal_equ_view.my_online_ps),  # 获取在线的画屏集合
]
