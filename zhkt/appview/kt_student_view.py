import json

from base import common_tools, db_tools

# 全局业务表表名
table_name = 'zhkt_student'
# 全局默认的排序(学生姓名排序)
default_sidx = ' convert(t.student_name using gbk) '


def find_list(param_strs={}, sel_head=" select t.* ", camelize=False, my_default_sidx=None):
    sql_from_where = init_from_where_sql(param_strs)
    sql = sel_head + sql_from_where + ' order by ' + (my_default_sidx if my_default_sidx else default_sidx)
    return db_tools.find_dict_list_by_sql(sql, None, camelize)


# 传入条件, 查询一条
def find_one(param_strs={}, sel_head=" select t.* ", camelize=False):
    stu_list = find_list(param_strs, sel_head, camelize)
    return stu_list[0] if stu_list and len(stu_list) else None


# 整合查询用户的原生sql
def init_from_where_sql(param_strs):
    id = param_strs['id'] if 'id' in param_strs else ''
    mainId = param_strs['mainId'] if 'mainId' in param_strs else ''
    studentId = param_strs['studentId'] if 'studentId' in param_strs else ''
    groupId = param_strs['groupId'] if 'groupId' in param_strs else ''
    isToPjTch = param_strs['isToPjTch'] if 'isToPjTch' in param_strs else ''
    toPjTchNotNull = param_strs['toPjTchNotNull'] if 'toPjTchNotNull' in param_strs else ''
    isTchQuota = param_strs['isTchQuota'] if 'isTchQuota' in param_strs else ''
    ktStatus = param_strs['ktStatus'] if 'ktStatus' in param_strs else ''
    sql = " from " + table_name + " t where 1 = 1 "
    if ktStatus:
        sql += " and t.kt_status = '" + ktStatus + "' "
    if isTchQuota:
        sql += " and t.is_tch_quota = '" + isTchQuota + "' "
    if toPjTchNotNull:
        sql += " and ifnull(t.to_pj_tch, '') <> '' "
    if isToPjTch:
        sql += " and t.is_to_pj_tch = '{}' ".format(isToPjTch)
    if mainId:
        sql += " and t.main_id = '{}' ".format(mainId)
    if groupId:
        sql += " and t.group_id = '{}' ".format(groupId)
    if studentId:
        sql += " and t.student_id = '{}' ".format(studentId)
    if id:
        sql += " and t.id = '{}' ".format(id)
    return sql


# 学生测验情况 - 整体统计(班级总人数/到课人数/测验提交人数)
def test_total_map(mainId):
    return db_tools.find_dict_list_by_sql("""select count(*) as stuNum,
                                                    sum(case kt_status when 'Y' then 1 else 0 end) as daoKeNum
                                                    sum(case when ifnull(pub_test_time, '') != '' then 1 else 0 end) as testPubNum
                                            from {}
                                            where main_id = %s """.format(table_name), [mainId])


# 查询教师评价所有学生 - 查询列表使用(使用驼峰命名)
def find_kt_all_stus(mainId, camelize=False):
    param_strs = {'mainId': mainId}
    # 学生姓名/到课状态/评价状态/学生反馈状态
    sel_head = """  select t.id, t.student_id, t.student_name, t.student_gender,
                        t.kt_status, t.is_tch_quota, t.is_to_pj_tch """
    return find_list(param_strs, sel_head, camelize)  # 使用驼峰命名


# 更新课堂参与学生表, 互动次数/积分
def stus_add_bonus_num(mainId, studentIds, bonus=0, actNum=0):
    studentIdsSql = " '" + studentIds.replace(",", "','") + "' "
    db_tools.update_one_sql(
        """ update {} set bonus = ifnull(bonus, 0) + ({}),
                        act_num = ifnull(act_num, 0) + ({})
            where student_id in {} and main_id = %s """.format(table_name, bonus, actNum, studentIdsSql), mainId)


# 学生反馈 - 保存反馈的信息
def save_stu_pj_tch(mainId, studentId, toPjTch, quotaStr):
    curTime = common_tools.now()  # 当前时间
    quotaList = json.loads(quotaStr)  # 每个字典对应1个测验题目答案
    sql_sb = ' update {} set '.format(table_name)  # 拼接后的更新sql
    sql_paras = []
    for row in quotaList:
        pjTchScore = str(row['num']) if row['num'] else 0  # 单项评价分, 若未选择则置为0星
        sql_sb += ' pj_tch_score{} = %s, '.format(row['orderNo'])
        sql_paras.append(pjTchScore)
    sql_sb += """   is_to_pj_tch = 'Y',
                    to_pj_tch = %s,
                    to_pj_tch_time = %s
                where main_id = %s
                and student_id = %s """
    sql_paras.append(toPjTch if toPjTch else '')
    sql_paras.append(curTime)
    sql_paras.append(mainId)
    sql_paras.append(studentId)
    db_tools.update_one_sql(sql_sb, sql_paras)
