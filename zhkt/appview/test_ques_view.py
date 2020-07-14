from base import common_tools, db_tools

from zhkt import zhkt_tools


# 全局业务表表名
table_name = 'zhkt_test_ques'


# 通过课堂Id查询所有互动题目
def find_by_main_id(main_id, camelize=False):
    base_list = db_tools.find_dict_list_by_sql(
            "select t.* from {} t where t.main_id = '{}' order by t.orderNo ".format(table_name, main_id))
    rs_list = []
    if base_list and len(base_list):
        for item in base_list:
            item['ques_type_label'] = zhkt_tools.cn_ques_type(item['ques_type'])  # 整合题目类型汉字
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
                "select id, test_ques_id, option_describe, option_no, is_answer from zhkt_test_ques_option where main_id = %s order by orderNo", [main_id])
        if all_opt_list and len(all_opt_list):
            ques_dict = {}  # 整合题目id与题目对象, 为了选项匹配方便
            for row in ques_list:
                row['opt_list'] = []
                ques_dict[row['id']] = row
            print(ques_dict)
            # 匹配各题目下的选项列表
            for item in all_opt_list:
                test_ques_id = item['test_ques_id']
                if test_ques_id in ques_dict:  # 防止程序出错终止, 加一步dict中key判断
                    ques_row = ques_dict[test_ques_id]
                    ques_row['opt_list'].append(item)
    return ques_list
