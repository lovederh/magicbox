import json

from base import constant, common_tools, db_tools
from zhkt import zhkt_tools

# 全局业务表表名
table_name = 'zhkt_stu_test_result'


def find_list(param_strs={}, sel_head=" select t.* ", camelize=False, my_default_sidx=None):
    sql_from_where = init_from_where_sql(param_strs)
    sql = sel_head + sql_from_where
    if my_default_sidx:
        sql += ' order by ' + my_default_sidx
    return db_tools.find_dict_list_by_sql(sql, camelize)


# 找到指定题目的互动数据
def one_ques_rs_list(mainId, testQuesId):
    param_strs = {'mainId': mainId, 'testQuesId': testQuesId}
    sel_head = " select t.*, s.student_name, s.student_gender "
    return find_list(param_strs, sel_head, False)


# 整合查询用户的原生sql
def init_from_where_sql(params):
    mainId = params['mainId'] if 'mainId' in params else ''
    testQuesId = params['testQuesId'] if 'testQuesId' in params else ''
    studentId = params['studentId'] if 'studentId' in params else ''
    sql = """ from {} t
            left join zhkt_student s on s.student_id = t.student_id and s.main_id = t.main_id
            where 1 = 1 """.format(table_name)
    if mainId:
        sql += " and t.main_id = '" + mainId + "' "
    if testQuesId:
        sql += " and t.test_ques_id = '" + testQuesId + "' "
    if studentId:
        sql += " and t.student_id = '" + studentId + "' "
    return sql


# 测验情况 - 统计互动题目各组正确率
def test_ques_right_anls(mainId):
    # 查询各个题目的回答人数/正确人数
    baseQuesAnls = db_tools.find_dict_list_by_sql(
        """ select t.testQuesId,
                t.replyNum,
                round(case when t.replyNum = 0 then 0.0 else (t.rightNum * 100 / t.replyNum) end, 2) as rightPercent,
                round(case when t.replyNum = 0 then 0.0 else ((t.replyNum - t.rightNum) * 100 / t.replyNum) end, 2) as missPercent
        from(select t.test_ques_id as testQuesId,
                    count(*) as replyNum,
                    sum(case when t.right_result = 'Y' then 1 else 0 end) as rightNum
            from {} t
            where t.main_id = %s
            group by t.test_ques_id ) t """.format(table_name), [mainId])
    quesAnlsMap = {}  # testQuesId与整理对应的关系字典
    if baseQuesAnls and len(baseQuesAnls):
        for temp in baseQuesAnls:
            quesAnlsMap[temp['testQuesId']] = temp
    # 按各个题目整理
    quesList = zhkt_tools.init_test_ques_list(mainId)
    result = []  # 最终的返回结果
    for idx, val in enumerate(quesList):
        if constant.QUES_TYPE_SHORT_ANSWER == val['ques_type']:
            showMsg, showType = "简答题暂无法统计", "24004005"
        elif not val['answer']:
            showMsg, showType = "题目未设正确答案", "noAnswer"
        if val['id'] not in quesAnlsMap:
            if not showType:
                showType, showMsg = "0", "题目当前无人作答"
            quesAnls = {
                'testQuesId': val['id'],
                'replyNum': 0,
                'rightPercent': 0.0,  # 正确率
                'missPercent': 0.0,  # 错误率
            }
        else:
            quesAnls = quesAnlsMap[val['id']]
        quesAnls['orderno'] = idx + 1
        quesAnls['showType'] = showType
        quesAnls['showMsg'] = showMsg
        result.append(quesAnls)
    return result


# 互动题目统计 - 投票/举手回答 (单选/判断题有效)
def one_test_ques_anls(mainId, testQues, testRsList):
    isReplyNum, rightNum = 0, 0  # 已回答人数/回答正确人数
    quesAnswer = testQues['answer']  # 测验题目的答案
    optAnlsMap = {}  # 各选项关键字-整体对象的对应map
    if constant.QUES_TYPE_JUDGE == testQues['ques_type']:  # 判断题
        # 放入正确对应的选项
        optAnlsMap['Y'] = {'optionKey': 'Y', 'optionNo': '对', 'isAnswer': 'Y' if 'Y' == quesAnswer else 'N', 'chooseNum': 0, 'answerStuList': []}
        # 放入错误对应的选项
        optAnlsMap['N'] = {'optionKey': 'N', 'optionNo': '错', 'isAnswer': 'Y' if 'N' == quesAnswer else 'N', 'chooseNum': 0, 'answerStuList': []}
        if quesAnswer:
            quesAnswer = '对' if 'Y' == quesAnswer else '错'
        else:
            quesAnswer = ''
    elif constant.QUES_TYPE_RADIO == testQues['ques_type']:  # 单选题
        baseOptList = testQues['opt_list']
        for row in baseOptList:
            optAnlsMap[row['option_no']] = {'optionKey': row['option_no'], 'optionNo': row['option_no'], 'isAnswer': row['is_answer'], 'chooseNum': 0, 'answerStuList': []}
    elif constant.QUES_TYPE_MULTIPLE == testQues['ques_type']:  # 多选题
        quesAnswer = quesAnswer.replace(',', '') if quesAnswer else ''  # 多选题, 答案移除逗号
    emptyOpt = {'optionKey': '', 'optionNo': '未作答', 'isAnswer': 'N', 'answerStuList': []}  # 未作答对象

    isReplyNum = 0  # 已回答人数
    rightNum = 0  # 回答正确人数
    if testRsList and len(testRsList):
        for temp in testRsList:
            isReplyNum += 1  # 参与回答人数累计
            if 'Y' == temp['right_result']:
                rightNum += 1  # 正确人数累计
            answerStu = {'studentId': temp['student_id'], 'studentName': temp['student_name'], '': temp['student_gender'], }
            answer = temp['answer']
            if answer:
                answer = answer.replace(",", "")
                optAnls = optAnlsMap[answer]
                if not optAnls:
                    optAnls = {'optionKey': answer, 'optionNo': answer, 'isAnswer': 'Y' if answer == quesAnswer else 'N', 'chooseNum': 0}
                optAnls['chooseNum'] = optAnls['chooseNum'] + 1  # 累计选择人数
                optAnls['answerStuList'].append(answerStu)
            else:  # 未作答统计
                emptyOpt['chooseNum'] = emptyOpt['chooseNum'] + 1  # 累计选择人数
                emptyOpt['answerStuList'].append(answerStu)

    # 统计正确率(整体)
    rightPercent = round(rightNum * 100.0 / isReplyNum, 2) if isReplyNum > 0 else 0.0
    # 整合选项统计
    optAnlsList = []
    for (k, v) in optAnlsMap.items():
        v['choosePercent'] = 0.0 if isReplyNum <= 0 else round(v['chooseNum'] * 100.0 / isReplyNum, 2)  # 计算各个项选择比例
        if 'Y' == v['isAnswer']:  # 保证正确答案置顶
            optAnlsList.insert(0, v)
        else:
            optAnlsList.append(v)
    # 放入未作答统计
    if emptyOpt['chooseNum'] > 0:
        optAnlsList.append(emptyOpt)
    # 最终的返回结果
    return {
        'isReplyNum': isReplyNum,
        'rightNum': rightNum,
        'rightPercent': rightPercent,
        'quesAnswer': quesAnswer,
        'optAnlsList': optAnlsList,
    }


# 保存学生提交的课堂测验结果
def save_stu_test_result(mainId, studentId, quesListStr):
    curTime = common_tools.now()  # 当前时间
    quesList = json.loads(quesListStr)  # 每个字典对应1个测验题目答案
    baseQuesList = zhkt_tools.init_test_ques_list(mainId)
    baseQuesMap = {ques[id]: ques for ques in baseQuesList}  # 构造测验题目Id与题目对象的对应关系
    # 每个题目都需要存储一个答题结果
    saveList = []  # 最终参与保存的学生答题结果(短线命名)
    for bean in quesList:
        baseQues = baseQuesMap[bean['testQuesId']]
        answer = bean['answer'] if 'answer' in bean and bean['answer'] else ''  # 回答的答案
        right_result = 'Y' if answer and baseQues['answer'] and answer == baseQues['answer'] else 'N'  # 是否回答正确
        saveList.append({
            'orderNo': baseQues['orderno'],
            'id': bean['id'],
            'main_id': mainId,
            'student_id': studentId,
            'test_ques_id': bean['testQuesId'],
            'right_result': right_result,
            'answer': answer,
        })
    # 保存之前先删除现有答题结果
    sql_list = [
        "delete from {} where main_id = '{}' and student_id = '{}' ".format(table_name, mainId, studentId),
        "update zhkt_student set pub_test_time = '{}' where main_id = '{}' and student_id = '{}' ".format(curTime, mainId, studentId),
    ]
    db_tools.update_sql_list(sql_list)
    db_tools.ins_batch_to_db(table_name, saveList)  # 执行批量保存
