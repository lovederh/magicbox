from base import db_tools

# 全局业务表表名
table_name = 'zhkt_base_quota'


# 通过评价使用类型, 查询指标列表
def find_by_type(type, camelize=False):
    return db_tools.find_dict_list_by_sql("select t.* from {} t where t.type = %s order by t.orderNo ".format(table_name), [type])
