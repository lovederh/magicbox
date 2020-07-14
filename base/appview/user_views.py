from django.shortcuts import render

import pymysql

from base import common_tools, db_tools


# 查询现有的所有用户列表
def to_user_list(request):
    context = {}
    return render(request, "base/user_list.html", context)


# 分页查询用户列表
def user_query(request):
    # 整合用户查询的from where语句
    params = {
        'realnameLike': request.GET.get('realnameLike'),  # 模糊搜索姓名
        'usernameLike': request.GET.get('usernameLike'),  # 模糊搜索账号
        'userType': request.GET.get('userType')  # 用户类型
    }
    sql_from_where = init_user_fw_sql(params)
    # 分页查询对象
    pager = {
        'page': request.GET.get('page'),  # 页码
        'limit': request.GET.get('limit'),  # 每页数量
        'sidx': request.GET.get('sidx'),  # 使用的排序字段
        'order': request.GET.get('order'),  # 使用的排序方式
        'default_sidx': ' t.userType, t.realname ',  # 默认的排序方式
    }
    page = db_tools.find_pager_by_sql(pager, " select t.* ", sql_from_where)
    return common_tools.re_ok({'page': page})


# 整合查询用户的原生sql
def init_user_fw_sql(params):
    realnameLike = params['realnameLike'] if 'realnameLike' in params else ''  # 模糊搜索姓名
    username = params['username'] if 'username' in params else ''  # 精准搜索账号
    usernameLike = params['usernameLike'] if 'usernameLike' in params else ''  # 模糊搜索账号
    userType = params['userType'] if 'userType' in params else ''  # 用户类型
    sql = " from base_user t where 1 = 1 "
    if realnameLike:
        realnameLike = pymysql.escape_string(realnameLike)  # 防止sql注入
        sql += " and t.realname like '%" + realnameLike + "%' "
    if usernameLike:
        usernameLike = pymysql.escape_string(usernameLike)
        sql += " and t.username like '%" + usernameLike + "%' "
    if userType:
        sql += " and t.userType = '" + userType + "' "
    if username:
        username = pymysql.escape_string(username)
        sql += " and t.username = '" + username + "' "
    return sql
