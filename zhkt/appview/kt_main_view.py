from django.shortcuts import render

from base import constant, common_tools, db_tools

from zhkt.models import Main
from zhkt import zhkt_tools

# 全局业务表表名
table_name = 'zhkt_main'
# 全局默认的排序
default_sidx = ' t.week_index desc, t.start_time desc '


# 查询盒子下已有的全部课堂
def to_zhkt_list(request):
    context = {}
    return render(request, "zhkt/zhkt_list.html", context)


# 分页查询用户列表
def zhkt_query(request):
    # 整合用户查询的from where语句
    param_strs = {

    }
    sql_paras = []  # 注入的sql参数(list类型)
    sql_from_where = init_from_where_sql(param_strs, sql_paras)
    # 分页查询对象
    pager = {
        'page': request.GET.get('page'),  # 页码
        'limit': request.GET.get('limit'),  # 每页数量
        'sidx': request.GET.get('sidx'),  # 使用的排序字段
        'order': request.GET.get('order'),  # 使用的排序方式
        'default_sidx': default_sidx,  # 默认的排序方式
    }
    page = db_tools.find_pager_by_sql(pager, " select t.* ", sql_from_where, sql_paras)
    return common_tools.re_ok({'page': page})


def find_list(param_strs={}, sel_head=" select t.* ", camelize=False, my_default_sidx=None):
    sql_paras = []  # 注入的sql参数(list类型)
    sql_from_where = init_from_where_sql(param_strs, sql_paras)
    sql = sel_head + sql_from_where + ' order by ' + (my_default_sidx if my_default_sidx else default_sidx)
    return db_tools.find_dict_list_by_sql(sql, sql_paras, camelize)


# 整合查询用户的原生sql
def init_from_where_sql(param_strs, sql_paras):
    mainStatus = param_strs['mainStatus'] if 'mainStatus' in param_strs else ''  # 状态
    teacherId = param_strs['teacherId'] if 'teacherId' in param_strs else ''  # 教师Id
    venue = param_strs['venue'] if 'venue' in param_strs else ''  # 场地Id
    sql = " from " + table_name + " t where 1 = 1 "
    if mainStatus:
        sql += " and t.main_status = %s "
        sql_paras.append(mainStatus)
    if venue:
        sql += " and t.venue = %s "
        sql_paras.append(venue)
    if teacherId:
        sql += " and t.teacher_id = %s "
        sql_paras.append(teacherId)
    return sql


# 通过课堂id查询一条数据
def by_id(request, id):
    entity = db_tools.find_dict_by_id(table_name, id)
    return common_tools.re_ok({'entity': entity})


# 开始上课
def start_kt(id):
    # 更新资源状态
    db_tools.update_one_sql(""" update zhkt_main_source
                                set sr_status = %s
                                where main_id = %s """, [constant.SOURCE_STATUS_OK, id])

    obj = zhkt_tools.init_main_by_id(id)
    obj.main_status = constant.KT_STATUS_START  # 课堂状态改为开始
    if not obj.re_start_time:
        obj.re_start_time = common_tools.get_ymdhms_time()  # 真正开始时间
        obj.year_month = common_tools.get_year_month()  # 年月
    obj.save()  # 执行主表更新
    # todo 推送数据


# 下课
def end_kt(id):
    obj = Main.objects.filter(id=id).first()
    obj.main_status = constant.KT_STATUS_END  # 课堂状态改为结束
    obj.end_time = common_tools.get_ymdhms_time()  # 课堂结束时间
    if constant.QUES_STATUS_START == obj.test_status:
        obj.test_status = constant.QUES_STATUS_END  # 如果测验已开始, 那么改为结束状态
    obj.save()  # 执行主表更新

    # todo, 执行推送
