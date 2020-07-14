from base import constant, db_tools

from zhkt.models import Main
from zhkt.appview import base_quota_view, act_ques_view, test_ques_view

# 盒子内, 当前活跃课堂的缓存数据
cache = {
    'main_id': '',
    'main': None,
    'act_ques_list': [],
    'test_ques_list': [],
    'test_wx_ques_list': [],  # 学生app端使用的测验题目(包含盒子ip)
    'has_groups': '',  # 是否有小组Y/N
    'tch_base_quota': [],  # 教师评价使用的指标
    'stu_base_quota': [],  # 学生评价使用的指标
}


# 根据课堂状态码, 获取课堂状态汉字
def cn_kt_status(key):
    return {
        constant.KT_STATUS_NEW: '未开始',
        constant.KT_STATUS_START: '进行中',
        constant.KT_STATUS_END: '已结束',
    }.get(key, '') if key else ''


# 根据题型码, 整合汉字
def cn_ques_type(key):
    return {
        constant.QUES_TYPE_RADIO: '单选题',
        constant.QUES_TYPE_MULTIPLE: '多选题',
        constant.QUES_TYPE_JUDGE: '判断题',
        constant.QUES_TYPE_SHORT_ANSWER: '简答题',
    }.get(key, '') if key else ''


# 根据, 整合汉字
def cn_act_type(key):
    return {
        constant.ACT_TYPE_HAND_UP: '举手',
        constant.ACT_TYPE_RUSH_FIRST: '抢答',
        constant.ACT_TYPE_RANDOM: '随机',
        constant.ACT_TYPE_VOTE_ANSWER: '投票',
    }.get(key, '') if key else ''


# 开始上课, 整合课堂缓存
def build_main_caches(main_id):
    # 主表对象
    main = Main.objects.filter(id=main_id).first()
    # 所有的互动题目
    act_ques_list = act_ques_view.ques_and_opt_by_main(main_id)
    # 所有的测验题目
    test_ques_list = test_ques_view.ques_and_opt_by_main(main_id)
    # 确认当前是否有小组
    group_num = db_tools.find_count_by_fw_sql('from zhkt_main_group where main_id = %s', [main_id])
    has_groups = 'Y' if group_num else 'N'
    # 查询教师/学生评价使用的指标列表
    tch_base_quota = base_quota_view.find_by_type(constant.QUOTA_TYPE_TEACHER)
    stu_base_quota = base_quota_view.find_by_type(constant.QUOTA_TYPE_STUDENT)
    global cache
    cache = {
        'main_id': main_id,
        'main': main,
        'act_ques_list': act_ques_list,
        'test_ques_list': test_ques_list,
        'test_wx_ques_list': [],  # 学生app端使用的测验题目(包含盒子ip)
        'has_groups': has_groups,  # 是否有小组Y/N
        'tch_base_quota': tch_base_quota,
        'stu_base_quota': stu_base_quota,
    }


# 教师评价使用的指标列表
def init_tch_base_quota():
    tch_base_quota = cache['tch_base_quota']
    if tch_base_quota and len(tch_base_quota):
        pass
    else:
        tch_base_quota = base_quota_view.find_by_type(constant.QUOTA_TYPE_TEACHER)
        cache['tch_base_quota'] = tch_base_quota
    return tch_base_quota


# 学生评价使用的指标列表
def init_stu_base_quota():
    stu_base_quota = cache['stu_base_quota']
    if stu_base_quota and len(stu_base_quota):
        pass
    else:
        stu_base_quota = base_quota_view.find_by_type(constant.QUOTA_TYPE_STUDENT)
        cache['stu_base_quota'] = stu_base_quota
    return stu_base_quota


# 获取主表Main对象
def init_main_by_id(main_id):
    main = cache['main']
    if not main:
        main = Main.objects.filter(id=main_id).first()
        cache['main'] = main
    return main


# 获取当前活跃课堂的互动题目列表
def init_act_ques_list(main_id):
    act_ques_list = cache['act_ques_list']
    if act_ques_list and len(act_ques_list):
        pass
    else:
        act_ques_list = act_ques_view.ques_and_opt_by_main(main_id)
        cache['act_ques_list'] = act_ques_list
    return act_ques_list


# 整合题目对象
def act_ques_by_id(main_id, act_ques_id):
    act_ques_list = init_act_ques_list(main_id)
    for row in act_ques_list:
        if row.id == act_ques_id:
            return row
    return {}


# 确认互动题目的互动类型
def act_type_by_ques_id(main_id, act_ques_id):
    row = act_ques_by_id(main_id, act_ques_id)
    return row['type'] if row else ''


# 获取当前活跃课堂的测验题目列表
def init_test_ques_list(main_id):
    test_ques_list = cache['test_ques_list']
    if test_ques_list and len(test_ques_list):
        pass
    else:
        test_ques_list = test_ques_view.ques_and_opt_by_main(main_id)
        cache['test_ques_list'] = test_ques_list
    return test_ques_list if test_ques_list else []


# 整合题目对象
def test_ques_by_id(main_id, test_ques_id):
    test_ques_list = init_test_ques_list(main_id)
    for row in test_ques_list:
        if row.id == test_ques_id:
            return row
    return {}


# 签到结束 - 计算到课人数
def anls_qian_dao(id):
    db_tools.update_one_sql("""update zhkt_main m, (select count(*) as stu_num,
                                                        sum(case when ifnull(t.kt_status, 'N') = 'N' then 1 else 0 end) as miss_num,
                                                        t.main_id
                                                from zhkt_student t
                                                where t.main_id = %s
                                                group by t.main_id) t
                            set m.stu_num = t.stu_num, m.miss_num = t.miss_num
                            where m.id = t.main_id and m.id = %s """, [id, id])


# 更新互动题目 - 回答人数和正确人数的sql
def update_act_ques_anls(main_id, ques2End=True, actQuesId=None):
    quesStatuSql = (" '" + constant.QUES_STATUS_END + "' ") if ques2End else ' a.ques_status '
    actQuesSql = " and a.id = '{}' ".format(actQuesId) if actQuesId else ''
    db_tools.update_one_sql(
        """update zhkt_act_ques a, (select sum(case when 'Y' = t.is_reply_answer then 1 else 0 end) as reply_num,
                                                    sum(case when 'Y' = t.right_result then 1 else 0 end) as right_num,
                                                    a.id as act_ques_id
                                            from zhkt_act_ques a
                                            left join zhkt_stu_act_result t on t.main_id = a.main_id and t.act_ques_id = a.id
                                            where a.main_id = %s
                                            {actQuesSql}
                                            group by a.id ) t
                        set a.reply_num = ifnull(t.reply_num, 0),
                            a.right_num = ifnull(t.right_num, 0),
                            a.ques_status = {quesStatuSql}
                    where a.id = t.act_ques_id
                    {actQuesSql}
                    and a.main_id = %s """.format(quesStatuSql=quesStatuSql, actQuesSql=actQuesSql), [main_id, main_id])
