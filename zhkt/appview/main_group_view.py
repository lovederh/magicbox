from base import db_tools

# 全局业务表表名
table_name = 'zhkt_main_group'


# 通过课堂Id查询所有小组
def find_by_main_id(main_id, camelize=False):
    return db_tools.find_dict_list_by_sql(
            "select t.* from {} t where t.main_id = %s order by t.orderNo ".format(table_name), [main_id], camelize)
