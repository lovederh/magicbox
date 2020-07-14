from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import pymysql
import json

from base.models import Config
from base.constant import SCH_IP_CONF_KEY, MH_PORT_CONF_KEY
from base import common_tools, db_tools, http_tools

# 全局业务表表名
table_name = 'base_config'
# 全局缓存对象
cache_dict = {}  # key-value形式


# 查询现有的所有用户列表
def to_config_list(request):
    context = {}
    return render(request, "base/config_list.html", context)


# 分页查询用户列表
def config_query(request):
    # 整合用户查询的from where语句
    param_strs = {
        'keyLike': request.GET.get('keyLike'),  # 模糊搜索姓名
        'valueLike': request.GET.get('valueLike'),  # 模糊搜索账号
    }
    sql_paras = []  # 注入的sql参数(list类型)
    sql_from_where = init_config_fw_sql(param_strs, sql_paras)
    # 分页查询对象
    pager = {
        'page': request.GET.get('page'),  # 页码
        'limit': request.GET.get('limit'),  # 每页数量
        'sidx': request.GET.get('sidx'),  # 使用的排序字段
        'order': request.GET.get('order'),  # 使用的排序方式
        'default_sidx': ' t.key ',  # 默认的排序方式
    }
    page = db_tools.find_pager_by_sql(pager, " select t.* ", sql_from_where, sql_paras)
    return common_tools.re_ok({'page': page})


# 整合查询用户的原生sql
def init_config_fw_sql(param_strs, sql_paras):
    keyLike = param_strs['keyLike'] if 'keyLike' in param_strs else ''  # 模糊搜索参数key
    valueLike = param_strs['valueLike'] if 'valueLike' in param_strs else ''  # 模糊搜索参数值
    key = param_strs['key'] if 'key' in param_strs else ''  # 精确查询参数名
    id_not = param_strs['id_not'] if 'id_not' in param_strs else ''  # 主键不为某值
    sql = " from " + table_name + " t where 1 = 1 "
    if id_not:
        sql += " and t.id <> %s "
        sql_paras.append(id_not)
    if keyLike:
        # 解决模糊查询, 需要在字符串前后手动拼接百分号
        keyLike = "%%" + pymysql.escape_string(keyLike) + "%%"  # 防止sql注入
        sql += " and t.key like %s "
        sql_paras.append(keyLike)
    if valueLike:
        valueLike = "%%" + pymysql.escape_string(valueLike) + "%%"  # 防止sql注入
        sql += " and t.value like %s "
        sql_paras.append(valueLike)
    if key:
        sql += " and t.key = %s "
        sql_paras.append(key)
    return sql


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
    key = entity.get('key')
    if not key:
        return common_tools.re_error('参数名不能为空！')
    # 判断是否有参数名冲突
    param_strs = {
        'key': key,
        'id_not': entity['id'] if 'id' in entity else ''
    }
    sql_paras = []  # 注入的sql参数
    sql_from_where = init_config_fw_sql(param_strs, sql_paras)
    exists_num = db_tools.find_count_by_fw_sql(sql_from_where, sql_paras)
    if exists_num:
        return common_tools.re_error('参数名已存在！')
    db_tools.save_dict_to_db(table_name, entity, False)  # 执行保存
    del_config_cache(key)  # 删除缓存
    return common_tools.re_ok()


# 删除
@csrf_exempt
def delete(request):
    id = request.POST.get('id')
    if not id:
        return common_tools.re_error('请选择要删除的数据！')
    obj = Config.objects.filter(id=id).first()
    del_config_cache(obj.key)  # 删除缓存
    obj.delete()  # 删除数据库数据
    return common_tools.re_ok()


# 删除缓存
def del_config_cache(key):
    if key in cache_dict:
        del cache_dict[key]


# 接收推送到的配置项列表, 并保存
def syn_sch_all_configs(configs_json_str):
    all_configs = json.loads(configs_json_str)  # 每个字典对应1个配置项
    # 先删除所有的配置
    db_tools.update_one_sql('delete from ' + table_name)
    if all_configs:
        config_list = []
        for k, v in all_configs.items():
            config_list.append({'key': k, 'value': v})
        db_tools.ins_batch_to_db(table_name, config_list, False)  # 批量保存
    global cache_dict
    cache_dict.clear()  # 执行缓存删除


# 通过key查询配置值
def init_val_by_key(key):
    if key in cache_dict:
        return cache_dict.get(key, '')
    # 尝试在数据库中查询
    val = db_tools.find_obj_by_sql('select value from ' + table_name + ' where `key` = %s ', [key])
    if val:
        cache_dict.update({key: val})
        return val
    return ''


# 获取学校服务器对应的访问路径
def load_sch_url():
    return init_val_by_key(SCH_IP_CONF_KEY)


# 获取学校服务器对应的访问路径
def load_mh_http():
    ip = http_tools.get_host_ip()
    mh_port = init_val_by_key(MH_PORT_CONF_KEY)  # 魔盒对外开放的端口号
    mh_port = mh_port if mh_port else '80'
    return r'http://{ip}:{mh_port}'.format(ip=ip, mh_port=mh_port)
