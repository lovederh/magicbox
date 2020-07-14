from base import constant, common_tools, db_tools

from zhkt import zhkt_tools
from zhkt.appview import kt_student_view as kt_student_view

# 全局业务表表名
table_name = 'zhkt_stu_act_result'


def find_list(param_strs={}, sel_head=" select t.* ", camelize=False, my_default_sidx=None):
    sql_from_where = init_from_where_sql(param_strs)
    sql = sel_head + sql_from_where
    if my_default_sidx:
        sql += ' order by ' + my_default_sidx
    return db_tools.find_dict_list_by_sql(sql, camelize)


# 找到指定题目的互动数据
def one_ques_rs_list(mainId, actQuesId):
    param_strs = {'mainId': mainId, 'actQuesId': actQuesId}
    sel_head = " select t.*, s.student_name, s.student_gender "
    return find_list(param_strs, sel_head, False, ' t.create_time_stamp ')


# 查询某个学生的互动结果
def one_stu_ques_rs(mainId, actQuesId, studentId):
    param_strs = {'mainId': mainId, 'actQuesId': actQuesId, 'studentId': studentId}
    base_list = find_list(param_strs)
    return base_list[0] if base_list and len(base_list) else None


# 整合查询用户的原生sql
def init_from_where_sql(params):
    mainId = params['mainId'] if 'mainId' in params else ''
    actQuesId = params['actQuesId'] if 'actQuesId' in params else ''
    isHandUp = params['isHandUp'] if 'isHandUp' in params else ''
    isReplyAnswer = params['isReplyAnswer'] if 'isReplyAnswer' in params else ''
    studentId = params['studentId'] if 'studentId' in params else ''
    sql = """ from {} t
            left join zhkt_student s on s.student_id = t.student_id and s.main_id = t.main_id
            where 1 = 1 """.format(table_name)
    if isHandUp:
        sql += " and t.is_hand_up = '" + isHandUp + "' "
    if isReplyAnswer:
        sql += " and t.is_reply_answer = '" + isReplyAnswer + "' "
    if mainId:
        sql += " and t.main_id = '" + mainId + "' "
    if actQuesId:
        sql += " and t.act_ques_id = '" + actQuesId + "' "
    if studentId:
        sql += " and t.student_id = '" + studentId + "' "
    return sql


# 互动题目统计 - 投票/举手回答 (单选/判断题有效)
def init_act_ques_anls(mainId, actQuesId):
    optAnlsMap = {}  # 各选项关键字-整体对象的对应map
    act_ques = zhkt_tools.act_ques_by_id(mainId, actQuesId)  # 判断题型
    quesAnswer = act_ques['answer']  # 互动题目答案
    if constant.QUES_TYPE_JUDGE == act_ques['ques_type']:  # 判断题
        # 放入正确对应的选项
        optAnlsMap['Y'] = {'optionKey': 'Y', 'optionNo': '对', 'isAnswer': 'Y' if 'Y' == quesAnswer else 'N', 'chooseNum': 0}
        # 放入错误对应的选项
        optAnlsMap['N'] = {'optionKey': 'N', 'optionNo': '错', 'isAnswer': 'Y' if 'N' == quesAnswer else 'N', 'chooseNum': 0}
        if quesAnswer:
            quesAnswer = '对' if 'Y' == quesAnswer else '错'
        else:
            quesAnswer = ''
    elif constant.QUES_TYPE_RADIO == act_ques['ques_type']:  # 单选题
        baseOptList = act_ques['opt_list']
        for row in baseOptList:
            optAnlsMap[row['option_no']] = {'optionKey': row['option_no'], 'optionNo': row['option_no'], 'isAnswer': row['is_answer'], 'chooseNum': 0}
    elif constant.QUES_TYPE_MULTIPLE == act_ques['ques_type']:  # 多选题
        quesAnswer = quesAnswer.replace(',', '') if quesAnswer else ''  # 多选题, 答案移除逗号

    act_rs_list = one_ques_rs_list(mainId, actQuesId)
    allStuNum = zhkt_tools.init_main_by_id(mainId).stu_num  # 参与上课的学生数量
    allStuNum = allStuNum if allStuNum else 0
    isReplyNum = 0  # 已回答人数
    handUpNum = 0  # 举手人数
    rightNum = 0  # 回答正确人数
    actNum = 0  # 参与人数
    replyStuList = []  # 真正回答问题的学生
    if act_rs_list and len(act_rs_list):
        for temp in act_rs_list:
            actNum += 1  # 参与人数累计
            if 'Y' == temp['is_hand_up']:
                handUpNum += 1  # 举手人数
            if 'Y' == temp['is_reply_answer']:
                isReplyNum += 1  # 真正回答有效的人数
                replyStuList.append({'studentId': temp['student_id'], 'studentName': temp['student_name'], 'studentGender': temp['student_gender'],
                                     'rightResult': temp['right_result'], 'result': temp['result']})
            if 'Y' == temp['right_result']:
                rightNum += 1  # 正确人数累计
            answer = temp['answer']
            if answer:
                answer = answer.replace(",", "")
                optAnls = optAnlsMap[answer]
                if not optAnls:
                    optAnls = {'optionKey': answer, 'optionNo': answer, 'isAnswer': 'Y' if answer == quesAnswer else 'N', 'chooseNum': 0}
                optAnls['chooseNum'] = optAnls['chooseNum'] + 1  # 累计选择人数
    # 统计正确率(整体)
    rightPercent = round(rightNum * 100.0 / isReplyNum, 2) if isReplyNum > 0 else 0.0
    # 统计参与率
    actPercent = round(actNum * 100.0 / allStuNum, 2) if allStuNum > 0 else 0.0
    # 整合选项统计
    optAnlsList = []
    for (k, v) in optAnlsMap.items():
        v['choosePercent'] = 0.0 if isReplyNum <= 0 else round(v['chooseNum'] * 100.0 / isReplyNum, 2)  # 计算各个项选择比例
        optAnlsList.append(v)
    # 最终的返回结果
    return {
        'allStuNum': allStuNum,
        'isReplyNum': isReplyNum,
        'handUpNum': handUpNum,
        'rightNum': rightNum,
        'rightPercent': rightPercent,
        'actNum': actNum,
        'actPercent': actPercent,
        'quesAnswer': quesAnswer,
        'optAnlsList': optAnlsList,
        'replyStuList': replyStuList,
    }


# 保存随机提问时, 所选的随机学生 - 同时通知画屏
def save_act_random_stus(mainId, actQuesId, studentIds):
    # 构造随机回答学生结果
    actStuList = []
    for studentId in studentIds.split(','):
        actStuList.append({
            'main_id': mainId,
            'act_ques_id': actQuesId,
            'student_id': studentId,
            'bonus': 1,  # 随机提问到的学生+1积分
            'is_hand_up': 'N',  # 随机提问不为举手
            'create_time': common_tools.now(),  # 当前回答时间
        })
    db_tools.ins_batch_to_db(table_name, actStuList, True)
    # 更新课堂学生表的积分/得分情况
    addBonus, addActNum = 1, 1
    kt_student_view.stus_add_bonus_num(mainId=mainId, studentIds=studentIds, bonus=addBonus, actNum=addActNum)
    # todo 给画屏推送参与随机提问的人


# 保护课堂互动时 - 学生答题结果 (教师选择对错)
def save_act_stu_result(mainId, actQuesId, studentId, rightResult, result):
    createTime = common_tools.now()  # 当前时间
    addBonus = 0  # 本次回答后, 学生增加的积分
    if "Y" == rightResult:
        addBonus = 1  # 回答正确加1分
    elif result and int(result) >= 3:
        addBonus = 1  # 评价超过3星, 加1分
    addActNum = 0  # 增加的互动次数
    actStu = one_stu_ques_rs(mainId=mainId, actQuesId=actQuesId, studentId=studentId)
    if actStu:
        if 'create_time' not in actStu or not actStu['create_time']:
            actStu['create_time'] = createTime
        bonus = actStu['bonus']
        actStu['bonus'] = (bonus if bonus else 0) + addBonus  # 最终本次积分
        actStu['right_result'] = rightResult
        actStu['result'] = result
        actStu['is_reply_answer'] = "Y"  # 回答问题标记
        db_tools.upd_dict_to_db(table_name, actStu)
    else:
        addActNum = 1
        actStu = {
            'main_id': mainId,
            'act_ques_id': actQuesId,
            'student_id': studentId,
            'create_time': createTime,
            'is_reply_answer': 'Y',  # 回答问题标记
            'result': result,
            'right_result': rightResult,
            'bonus': addBonus
        }
        db_tools.ins_dict_to_db(table_name, actStu)
    # 更新学生表积分
    if addBonus != 0 or addActNum != 0:
        kt_student_view.stus_add_bonus_num(mainId=mainId, studentIds=studentId, bonus=addBonus, actNum=addActNum)
