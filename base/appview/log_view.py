from django.shortcuts import render
import pymysql

import base.common_tools as common_tools
import base.db_tools as db_tools
# from base.logs import Log

# 全局业务表表名
table_name = 'base_log'


# 查询现有的所有用户列表
def to_log_list(request):
    context = {}
    # log = Log("log", "init")
    # log.record()
    return render(request, "base/log_list.html", context)


def log_query(request):
    # 整合用户查询的from where语句
    params = {
        'module': request.GET.get('module'),  # 模糊搜索模块名
        'content': request.GET.get('content'),  # 模糊搜索日志内容
    }
    sql_from_where = init_fw_sql(params)
    # 分页查询对象
    pager = {
        'page': request.GET.get('page'),  # 页码
        'limit': request.GET.get('limit'),  # 每页数量
        'sidx': request.GET.get('sidx'),  # 使用的排序字段
        'order': request.GET.get('order'),  # 使用的排序方式
        'default_sidx': ' t.create_time ',  # 默认的排序方式
    }
    page = db_tools.find_pager_by_sql(pager, " select t.* ", sql_from_where)
    return common_tools.re_ok({'page': page})


# 整合查询用户的原生sql
def init_fw_sql(params):
    module = params['module'] if 'module' in params else ''  # 模糊搜索姓名
    content = params['content'] if 'content' in params else ''  # 模糊搜索账号
    sql = " from base_log t where 1 = 1 "
    if module:
        module = pymysql.escape_string(module)  # 防止sql注入
        sql += " and t.module like '%" + module + "%' "
    if content:
        content = pymysql.escape_string(content)
        sql += " and t.content like '%" + content + "%' "
    return sql


# 通过配置项id查询一条数据
def by_id(request):
    id = request.GET.get('id')
    entity = db_tools.find_dict_by_id(table_name, id)
    return common_tools.re_ok({'entity': entity})
