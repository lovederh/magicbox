from base import constant, common_tools, db_tools

from zhkt import zhkt_tools

# 全局业务表表名
table_name = 'zhkt_act_ques'


# 通过课堂Id查询所有互动题目
def find_by_main_id(main_id, camelize=False):
    base_list = db_tools.find_dict_list_by_sql(
            "select t.* from {} t where t.main_id = '{}' order by t.orderNo ".format(table_name, main_id))
    rs_list = []
    if base_list and len(base_list):
        for item in base_list:
            if not item['ques_status']:
                item['ques_status'] = constant.QUES_STATUS_NEW  # 默认互动为未开始
            item['ques_type_label'] = zhkt_tools.cn_ques_type(item['ques_type'])  # 整合题目类型汉字
            item['type_label'] = zhkt_tools.cn_act_type(item['type'])  # 整合互动类型汉字
            if camelize:
                rs_list.append(common_tools.dict_key_camelize(item))
            else:
                rs_list.append(item)
    return rs_list


# 通过课堂Id, 查询所有互动题目, 整合选项列表
def ques_and_opt_by_main(main_id):
    ques_list = find_by_main_id(main_id)
    # 查询所有题目选项列表
    if ques_list and len(ques_list):
        all_opt_list = db_tools.find_dict_list_by_sql(
                "select id, act_ques_id, option_describe, option_no, is_answer from zhkt_act_ques_option where main_id = %s order by orderNo", [main_id])
        if all_opt_list and len(all_opt_list):
            # 执行选项与题目列表的匹配
            ques_dict = {}
            for row in ques_list:
                row['opt_list'] = []
                ques_dict[row['id']] = row
            for item in all_opt_list:
                ques_row = ques_dict[item['act_ques_id']]
                ques_row['opt_list'].append(item)
    return ques_list


# 开始一次互动方法
def start_one_act(mainId, actQuesId, answerLimit=1):
    # 更新互动题目状态
    db_tools.update_one_sql('update {} set ques_status = %s where id = %s '.format(table_name), [constant.QUES_STATUS_START, actQuesId])
    # 查找当前互动的题目
    bean = db_tools.find_dict_by_id(table_name, actQuesId)
    # todo 执行推送
