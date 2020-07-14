from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import pymysql
import json

import base.common_tools as common_tools
import base.db_tools as db_tools
from sr.models import Hardware
from base.socket_manager import singleton_service


# 全局业务表表名
table_name = 'sr_hardware'


# 查询现有的所有设备列表
def to_hardware_list(request):
    print(singleton_service.get_services())
    context = {}
    return render(request, "sr/hardware_list.html", context)


def hardware_query(request):
    # 整合用户查询的from where语句
    params = {
        'ip': request.GET.get('ip'),  # 模糊搜索模块名
        'hardware_type': request.GET.get('hardware_type'),  # 模糊搜索日志内容
        'alias_name': request.GET.get('alias_name'),
    }
    sql_paras = []
    sql_from_where = init_fw_sql(params, sql_paras)
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
def init_fw_sql(params, sql_paras):
    ip = params['ip'] if 'ip' in params else ''  # 模糊搜索ip
    mac = params['mac'] if 'mac' in params else ''  # 模糊搜索ip
    hardware_type = params['hardware_type'] if 'hardware_type' in params else ''  # 模糊搜索mac
    alias_name = params['alias_name'] if 'alias_name' in params else ''  # 模糊搜索mac
    id_not = params['id_not'] if 'id_not' in params else ''  # 主键不为某值
    sql = " from sr_hardware t where 1 = 1 "
    if id_not:
        sql += " and t.id <> %s "
        sql_paras.append(id_not)
    if ip:
        ip = pymysql.escape_string(ip)  # 防止sql注入
        sql += " and t.ip like '%" + ip + "%' "
    if mac:
        mac = pymysql.escape_string(mac)  # 防止sql注入
        sql += " and t.mac = '" + mac + "' "
    if hardware_type:
        hardware_type = pymysql.escape_string(hardware_type)
        sql += " and t.hardware_type = '" + hardware_type + "' "
    if alias_name:
        alias_name = pymysql.escape_string(alias_name)
        sql += " and t.alias_name like '%" + alias_name + "%' "
    return sql


# 通过配置项id查询一条数据
def by_id(request):
    id = request.GET.get('id')
    sql = '''
        select * from sr_hardware
        where id = %s
    '''
    entity = db_tools.find_dict_by_sql(sql, sql_para_list=[id, ])
    return common_tools.re_ok({'entity': entity})


# 保存(新增/修改)
@csrf_exempt  # 注解解决post请求500
def save(request):
    entity_str = request.POST.get('entity')
    entity = json.loads(entity_str)  # json转换为dict
    mac = entity.get('mac')
    if not mac:
        return common_tools.re_error('Mac地址不能为空！')
    # 判断是否有参数名冲突
    param_strs = {
        'mac': mac,
        'id_not': entity['id'] if 'id' in entity else ''
    }
    sql_paras = []  # 注入的sql参数
    sql_from_where = init_fw_sql(param_strs, sql_paras)
    exists_num = db_tools.find_count_by_fw_sql(sql_from_where, sql_paras)
    if exists_num:
        return common_tools.re_error('此Mac设备已存在！')
    entity['create_time'] = common_tools.now()
    db_tools.save_dict_to_db(table_name, entity, True)  # 执行保存
    return common_tools.re_ok()


def saveBatch(hardwares):
    sql_list = []
    for i in hardwares:
        hardware = hardwares[i]
        sql = (
            "insert into sr_hardware (id, hostname, ip, mac, create_time, hardware_type)",
            "select * from (select '",
            common_tools.gen_uuid(),
            "','", hardware.get_mac(),
            "'  as mac,'",
            hardware.get_hostname(),
            "','",
            hardware.get_ip(),
            "','",
            hardware.get_mac(),
            "','",
            common_tools.now(),
            "','1002') x ",
            " where not exists( select 1 from sr_hardware t where t.mac = x.mac )"
        )
        print("sql = > ", "".join(sql))
        sql_list.append("".join(sql))
    # 更新一组sql
    db_tools.update_sql_list(sql)


# 删除
@csrf_exempt
def delete(request):
    id = request.POST.get('id')
    if not id:
        return common_tools.re_error('请选择要删除的数据！')
    obj = Hardware.objects.filter(id=id).first()
    obj.delete()  # 删除数据库数据
    return common_tools.re_ok()


# 在线设备列表
def to_online_hardware(request):
    context = {}
    return render(request, "sr/online_hardware_list.html", context)


# 查询在线设备列表
def query_online(request):
    from sr.magicbox import MagicBox
    mb = MagicBox()
    mb.get_device_list()
    hardwares = mb.hardwares
    totalCount = 0
    rows = []
    limit = 100
    totalPage = 1
    if hardwares and len(hardwares) > 0:
        totalCount = len(hardwares)
        # 遍历设备列表，取出每一个设备信息
        for mac in hardwares:
            hardware = hardwares[mac]
            rows.append({"mac": hardware.get_mac(), "ip": hardware.get_ip(), "hostname": hardware.get_hostname()})

    page = {
        'totalCount': totalCount,  # 总数量
        'list': rows,  # 分页数据的列表
        'pageSize': limit,  # 每页条数
        'totalPage': totalPage,  # 总页码数
    }
    return common_tools.re_ok({'page': page})


# 将设备和盒子绑定
def bind_hardware(request):
    mac = request.POST.get('mac')
    ip = request.POST.get('ip')
    hostname = request.POST.get('hostname')
    if not mac:
        return common_tools.re_error('请选择要帮定的数据！')
    sql_paras = [mac]  # 注入的sql参数
    sql_from_where = " from sr_hardware t where t.mac = %s "
    exists_num = db_tools.find_count_by_fw_sql(sql_from_where, sql_paras)
    if exists_num:
        return common_tools.re_error('此Mac设备已绑定过了！')
    entity = {"mac": mac, "ip": ip, "hostname": hostname, "create_time": common_tools.now()}
    db_tools.save_dict_to_db(table_name, entity, True)  # 执行保存
    return common_tools.re_ok()


def get_box_mac(request):
    return common_tools.re_ok({'mac': common_tools.get_mac_address()})
