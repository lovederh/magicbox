#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import connection

import math

from base import common_tools

"""
# 注: 涉及的sql_para_list均使用list类型即可
find_dict_by_id(table_name, id, id_col_name='id', camelize=False)
find_dict_by_sql(sql, sql_para_list=None, camelize=False)
find_obj_by_sql(sql, sql_para_list=None)
find_count_by_fw_sql(sql_from_where, sql_para_list=None)

find_dict_list_by_sql(sql, sql_para_list=None, camelize=False)
find_pager_by_sql(page_obj, sql_head, sql_from_where, sql_para_list=None, camelize=False)
find_obj_list_by_sql(sql, sql_para_list=None)

update_one_sql(sql, sql_para_list=None)
update_sql_list(sql_list)
del_by_id(table_name, id, id_col_name='id')
save_dict_to_db(table_name, data, ins_uu_id=True, id_col_name='id')
ins_dict_to_db(table_name, data, ins_uu_id=True, id_col_name='id')
upd_dict_to_db(table_name, data, id_col_name='id')
ins_batch_to_db(table_name, data_list, ins_uu_id=True, id_col_name='id')
"""


# 查询一行数据(dict形式返回)
def find_dict_by_sql(sql, sql_para_list=None, camelize=False):  # sql_para_list参数, 传递list过来就行
    sql_paras = tuple(sql_para_list) if sql_para_list and len(sql_para_list) > 0 else None
    cursor = connection.cursor()  # 获得一个游标(cursor)对象
    cursor.execute(sql, sql_paras)
    raw = cursor.fetchone()
    cursor.close()  # 关闭连接
    col_names = [desc[0] for desc in cursor.description]
    if camelize:
        camelize_names = [common_tools.key_str_camelize(desc[0]) for desc in cursor.description]
    obj = {}  # 最终返回结果
    if raw:
        # 把每一行的数据遍历出来放到Dict中
        for index, value in enumerate(raw):
            if camelize:
                obj[camelize_names[index]] = value
            else:
                obj[col_names[index]] = value
    return obj


# 通过主键id, 查询一条数据(字典结果)
def find_dict_by_id(table_name, id, id_col_name='id', camelize=False):
    sql = " select * from " + table_name + " where " + id_col_name + " = %s "
    cursor = connection.cursor()  # 获得一个游标(cursor)对象
    cursor.execute(sql, (id, ))
    raw = cursor.fetchone()
    cursor.close()  # 关闭连接
    col_names = [desc[0] for desc in cursor.description]
    if camelize:
        camelize_names = [common_tools.key_str_camelize(desc[0]) for desc in cursor.description]
    obj = {}  # 最终返回结果
    if raw:
        # 把每一行的数据遍历出来放到Dict中
        for index, value in enumerate(raw):
            if camelize:
                obj[camelize_names[index]] = value
            else:
                obj[col_names[index]] = value
    return obj


# 通过子查询语句, 查询数量
def find_count_by_fw_sql(sql_from_where, sql_para_list=None):
    num = find_obj_by_sql('select count(*) ' + sql_from_where, sql_para_list)
    return num if num else 0


# 查询一个对象(相当于jfinal的queryOne), 若对象不存在, 则返回空字符串
def find_obj_by_sql(sql, sql_para_list=None):
    sql_paras = tuple(sql_para_list) if sql_para_list and len(sql_para_list) > 0 else None
    cursor = connection.cursor()  # 获得一个游标(cursor)对象
    cursor.execute(sql, sql_paras)
    raw = cursor.fetchone()
    cursor.close()  # 关闭连接
    return raw[0] if raw and raw[0] else ''  # 三目运算: 真的结果 if 条件 else


# 通过原生sql查询结果, 转换为字典的list
def find_dict_list_by_sql(sql, sql_para_list=None, camelize=False):
    sql_paras = tuple(sql_para_list) if sql_para_list and len(sql_para_list) > 0 else None
    cursor = connection.cursor()  # 获得一个游标(cursor)对象
    cursor.execute(sql, sql_paras)
    raw_data = cursor.fetchall()
    cursor.close()  # 关闭连接
    col_names = [desc[0] for desc in cursor.description]
    if camelize:
        camelize_names = [common_tools.key_str_camelize(desc[0]) for desc in cursor.description]
    result = []
    for row in raw_data:
        obj = {}
        # 把每一行的数据遍历出来放到Dict中
        for index, value in enumerate(row):
            if camelize:
                obj[camelize_names[index]] = value
            else:
                obj[col_names[index]] = value
        result.append(obj)
    return result


# 通过原生sql, 查询一组值的list(内部为空的对象会转换为空字符串)
def find_obj_list_by_sql(sql, sql_para_list=None):
    sql_paras = tuple(sql_para_list) if sql_para_list and len(sql_para_list) > 0 else None
    cursor = connection.cursor()  # 获得一个游标(cursor)对象
    cursor.execute(sql, sql_paras)
    raw_data = cursor.fetchall()
    cursor.close()  # 关闭连接
    result = []  # 最终返回结果
    for raw in raw_data:
        if raw:
            result.append(raw[0])
        else:
            result.append('')
    return result


# 传递原生sql, 构造分页数据
def find_pager_by_sql(page_obj, sql_head, sql_from_where, sql_para_list=None, camelize=False):
    page = int(page_obj['page'])  # 页码
    limit = int(page_obj['limit'])  # 每页数量
    default_sidx = page_obj['default_sidx']  # 默认的排序语句
    sidx = page_obj['sidx']  # 使用的排序字段
    order = page_obj['order']  # 使用的排序方式
    order = ' desc ' if order and 'desc' == order else ' asc '  # 降序需要减号

    # 先查询总数
    totalCount = find_count_by_fw_sql(sql_from_where, sql_para_list)
    rows = []  # 当前分页的用户列表
    totalPage = 0  # 总页数
    if totalCount:
        start_pos = (page - 1) * limit
        end_pos = page * limit
        # 拼接最终的查询sql
        sql = sql_head + ' ' + sql_from_where
        if sidx:
            sql += ' order by ' + sidx + ' ' + order
        elif default_sidx:
            sql += ' order by ' + default_sidx
        sql += ' limit ' + str(start_pos) + ', ' + str(end_pos)
        rows = find_dict_list_by_sql(sql, sql_para_list, camelize)
        totalPage = math.ceil(totalCount * 1.0 / limit)  # 计算总页数
    else:
        totalCount = 0
    # 最终返回的分页对象使用结果
    return {
        'totalCount': totalCount,  # 总数量
        'list': rows,  # 分页数据的列表
        'pageSize': limit,  # 每页条数
        'totalPage': totalPage,  # 总页码数
    }


# 批量执行1条sql
def update_one_sql(sql, sql_para_list=None):
    sql_paras = tuple(sql_para_list) if sql_para_list and len(sql_para_list) > 0 else None
    cursor = connection.cursor()
    cursor.execute(sql, sql_paras)
    cursor.close()


# 批量更新一组sql
def update_sql_list(sql_list):
    cursor = connection.cursor()
    for sql in sql_list:
        cursor.execute(sql)
    cursor.close()


# 通过主键id, 执行删除
def del_by_id(table_name, id, id_col_name='id'):
    sql = " delete from " + table_name + " where " + id_col_name + " = %s "
    update_one_sql(sql, [id])  # 执行删除语句


# 通过字典对象, 完成插入/修改
def save_dict_to_db(table_name, data, ins_uu_id=True, id_col_name='id'):
    # 更新操作
    if id_col_name in data:
        upd_dict_to_db(table_name, data, id_col_name)
    else:
        # 执行插入操作
        ins_dict_to_db(table_name, data, ins_uu_id, id_col_name)


# 插入操作
def ins_dict_to_db(table_name, data, ins_uu_id=True, id_col_name='id'):
    # 有可能存在指定id但也是执行插入的情况
    id = data[id_col_name] if id_col_name in data else None
    if not id and ins_uu_id:
        data.update({id_col_name: common_tools.gen_uuid()})  # id未指定, 且使用uuid的情况
    sql_head = ''
    sql_val = ''
    sql_paras = []
    index = 0
    for (k, v) in data.items():
        if index == 0:
            index = 1
        else:
            sql_head += ','
            sql_val += ','
        sql_head += ' `' + k + '` '
        if v:
            sql_val += ' %s '
            sql_paras.append(v)
        else:
            sql_val += ' null '
    sql = 'insert into ' + table_name + '(' + sql_head + ')values(' + sql_val + ')'
    update_one_sql(sql, sql_paras)


# 更新操作
def upd_dict_to_db(table_name, data, id_col_name='id'):
    index = 0  # 控制下标, 保证第0项前面无逗号
    sql_paras = []
    sql = ' update ' + table_name + ' set '
    for (k, v) in data.items():
        if index == 0:
            index = 1
        else:
            sql += ','
        if v:
            sql += ' `' + k + '` = %s '
            sql_paras.append(v)
        else:
            sql += ' `' + k + '` = null '
    sql += ' where ' + id_col_name + ' = %s '
    sql_paras.append(data.get(id_col_name))
    update_one_sql(sql, sql_paras)


# 批量保存
def ins_batch_to_db(table_name, data_list, ins_uu_id=True, id_col_name='id'):
    sql_list = []
    for data in data_list:
        # 有可能存在指定id但也是执行插入的情况
        id = data[id_col_name] if id_col_name in data else None
        if not id and ins_uu_id:
            data.update({id_col_name: common_tools.gen_uuid()})  # id未指定, 且使用uuid的情况
        sql_head = ''
        sql_val = ''
        index = 0
        for (k, v) in data.items():
            if index == 0:
                index = 1
            else:
                sql_head += ','
                sql_val += ','
            sql_head += ' `' + k + '` '
            if v:
                sql_val += " '" + v + "' "
            else:
                sql_val += " null "
        sql_list.append('insert into ' + table_name + '(' + sql_head + ')values(' + sql_val + ')')
    update_sql_list(sql_list)
