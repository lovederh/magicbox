from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import pymysql
import json

from base.websocket_terminal import hp_sessions
from base.models import Terminal_Equ
from base import constant, common_tools, db_tools

# 全局业务表表名
table_name = 'base_terminal_equ'
# 全局缓存对象
cache_equs = {}  # key-value形式


# 查询所有终端设备列表
def to_terminal_equ_list(request):
    context = {}
    return render(request, "base/terminal_equ_list.html", context)


# 分页查询用户列表
def equ_query(request):
    # 整合用户查询的from where语句
    param_strs = {
        'equType': request.GET.get('equType'),  # 设备类型
        'aliasName': request.GET.get('aliasName'),  # 设备类型
        'equNameLike': request.GET.get('equNameLike'),  # 模糊搜索设备名称
        'macLike': request.GET.get('macLike'),  # 模糊搜索mac
    }
    sql_paras = []  # 注入的sql参数(list类型)
    sql_from_where = init_from_where_sql(param_strs, sql_paras)
    # 分页查询对象
    pager = {
        'page': request.GET.get('page'),  # 页码
        'limit': request.GET.get('limit'),  # 每页数量
        'sidx': request.GET.get('sidx'),  # 使用的排序字段
        'order': request.GET.get('order'),  # 使用的排序方式
        'default_sidx': ' t.equ_name ',  # 默认的排序方式
    }
    page = db_tools.find_pager_by_sql(pager, " select t.* ", sql_from_where, sql_paras)
    return common_tools.re_ok({'page': page})


# 整合查询用户的原生sql
def init_from_where_sql(param_strs, sql_paras):
    equType = param_strs['equType'] if 'equType' in param_strs else ''  # 设备类型
    aliasName = param_strs['aliasName'] if 'aliasName' in param_strs else ''  # 别名
    equNameLike = param_strs['equNameLike'] if 'equNameLike' in param_strs else ''  # 模糊搜索设备名称
    macLike = param_strs['macLike'] if 'macLike' in param_strs else ''  # 精确查询参数名
    mac = param_strs['mac'] if 'mac' in param_strs else ''  # mac地址
    idNot = param_strs['idNot'] if 'idNot' in param_strs else ''  # 主键不为某值
    sql = " from " + table_name + " t where 1 = 1 "
    if idNot:
        sql += " and t.id <> %s "
        sql_paras.append(idNot)
    if equNameLike:
        # 解决模糊查询, 需要在字符串前后手动拼接百分号
        equNameLike = "%%" + pymysql.escape_string(equNameLike) + "%%"  # 防止sql注入
        sql += " and t.equ_name like %s "
        sql_paras.append(equNameLike)
    if macLike:
        macLike = "%%" + pymysql.escape_string(macLike) + "%%"  # 防止sql注入
        sql += " and t.mac like %s "
        sql_paras.append(macLike)
    if equType:
        sql += " and t.equ_type = %s "
        sql_paras.append(equType)
    if aliasName:
        sql += " and t.alias_name = %s "
        sql_paras.append(aliasName)
    if mac:
        sql += " and t.mac = %s "
        sql_paras.append(mac)
    return sql


# 保存一个一体机连接
def save_ytj_equ(request):
    mac = request.GET.get('mac')  # 一体机的mac地址
    app_version = request.GET.get('app_version')  # 一体机使用的客户端版本
    # 执行现有一体机的删除
    equ_type = constant.TERMINAL_TYPE_YTJ
    db_tools.update_one_sql("delete from {} where equ_type = %s ".format(table_name), [equ_type])
    # 构造一个一体机存储对象
    cur_time = common_tools.now()
    entity = {'mac': mac, 'equ_type': equ_type, 'app_version': app_version,
              'alias_name': 'ytj', 'equ_name': '一体机', 'create_time': cur_time, 'last_online': cur_time}
    return _save(entity)  # 调用通用的保存方法


# 通过配置项id查询一条数据
def by_id(request):
    id = request.GET.get('id')
    entity = db_tools.find_dict_by_id(table_name, id)
    return common_tools.re_ok({'entity': entity})


# 保存(新增/修改)
@csrf_exempt  # 注解解决post请求500
def save(request):
    entity_str = request.POST.get('entity')
    entity = json.loads(entity_str)  # json转换为dict
    return _save(entity)  # 调用通用的保存方法


# 终端设备绑定的保存方法
def _save(entity):
    update_flag = True if 'id' in entity and entity['id'] else False
    mac = entity.get('mac')
    if not mac:
        return common_tools.re_error('mac地址不能为空！')
    # 判断是否有mac地址冲突
    param_strs = {
        'mac': mac,
        'idNot': entity['id'] if update_flag else ''
    }
    sql_paras = []  # 注入的sql参数
    sql_from_where = init_from_where_sql(param_strs, sql_paras)
    exists_num = db_tools.find_count_by_fw_sql(sql_from_where, sql_paras)
    if exists_num:
        return common_tools.re_error('mac地址已存在！')
    # 判断是否有别名冲突
    alias_name = entity.get('alias_name')
    if alias_name:
        # 判断别名是否冲突
        param_strs = {
            'aliasName': alias_name,
            'idNot': entity['id'] if update_flag else ''
        }
        sql_paras = []  # 注入的sql参数
        sql_from_where = init_from_where_sql(param_strs, sql_paras)
        exists_num = db_tools.find_count_by_fw_sql(sql_from_where, sql_paras)
        if exists_num:
            return common_tools.re_error('终端别名冲突！')
    else:
        entity['alias_name'] = ''
    if update_flag:
        db_tools.upd_dict_to_db(table_name, entity)
        del_equ_cache(mac)  # 删除缓存
    else:
        entity['create_time'] = common_tools.now()  # 绑定时间
        db_tools.ins_dict_to_db(table_name, entity)
    return common_tools.re_ok()


# 删除
@csrf_exempt
def delete(request):
    id = request.POST.get('id')
    if not id:
        return common_tools.re_error('请选择要删除的数据！')
    obj = Terminal_Equ.objects.filter(id=id).first()
    del_equ_cache(obj.mac)  # 删除缓存
    obj.delete()  # 删除数据库数据
    return common_tools.re_ok()


# 删除缓存
def del_equ_cache(mac):
    if mac in cache_equs:
        del cache_equs[mac]


# 批量设置开关及时间
@csrf_exempt
def batch_set_times(request):
    weekup_time = request.POST.get('weekup_time')
    close_time = request.POST.get('close_time')
    ids = request.POST.get('ids')
    if not ids:
        return common_tools.re_error('请选择批量的终端设备！')
    ids = " '" + ids.replace(",", "','") + "' "
    db_tools.update_one_sql("update {} set weekup_time = %s, close_time = %s where id in({}) ".format(table_name, ids),
                            [weekup_time if weekup_time else '', close_time if close_time else ''])
    cache_equs.clear()  # 清除所有缓存
    return common_tools.re_ok()


# 获取所有在线的画屏列表
def my_online_ps(request):
    onlinePs = []
    if len(hp_sessions):
        for (k, v) in hp_sessions.items():
            onlinePs.append(v['mac'])
    return common_tools.re_ok({'onlinePs': onlinePs})


# 通过mac和设备类型, 查询一个终端设备对象(存放缓存中)
def init_equ_by_mac(mac):
    if mac in cache_equs:
        return cache_equs.get(mac, {})
    # 尝试在数据库中查询
    equ = db_tools.find_obj_by_sql('select * from {} where mac = %s '.format(table_name), [mac])
    if equ:
        cache_equs.update({mac: equ})
        return equ
    return {}
