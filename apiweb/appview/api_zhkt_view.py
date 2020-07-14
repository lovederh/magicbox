from django.shortcuts import render

from base import constant, common_tools, db_tools

from zhkt import zhkt_tools
from zhkt.appview import act_ques_view, kt_main_view, kt_student_view, stu_act_result_view, stu_test_result_view


# 查询所有测验题目 - 进入webView页面
def zhktTestWebView(request):
    mainId = request.GET.get('mainId')
    context = {
        'quesList': zhkt_tools.init_test_ques_list(mainId)
    }
    return render(request, "apiweb/zhkt_test_web_view.html", context)


# 选择我的处于未开始的课堂 - 根据教师Id查询
def tchUseKtList(request):
    param_strs = {
        'teacherId': request.GET.get('teacherId'),  # 教师Id
        'venue': request.GET.get('venue'),  # 查询场地
        'mainStatus': constant.KT_STATUS_NEW,  # 只查询未开始的
    }
    sel_head = " select t.*, (select realname from base_user where dataid = t.teacher_id) as teacherLabel "
    kt_list = kt_main_view.find_list(param_strs, sel_head, True)
    if kt_list and len(kt_list):
        for item in kt_list:
            # 放入课堂状态汉字
            item['mainStatusLabel'] = zhkt_tools.cn_kt_status(item['mainStatus'])
    else:
        kt_list = []
    return common_tools.re_app_ok({'result': kt_list, })


# 开始上课: 1. 一体机发起socket主动连接学校服务器 2. 整合旗下的画屏, 发送消息
def startKt(request):
    mainId = request.GET.get('mainId')
    # 构造整体缓存
    zhkt_tools.build_main_caches(mainId)
    # 执行开始上课
    kt_main_view.start_kt(mainId)
    # todo 画屏切换到上课模式


# 结束课堂 (注: 一体机需要主动断开socket连接)
def endKt(request):
    mainId = request.GET.get('mainId')
    # 下课前处理: 课堂存在活跃的签到/互动/测验中, 那么先结束掉

    kt_main_view.end_kt(mainId)
    # 通知画屏端, 进入下课模式


# 查询所有参与课堂的学生 (签到时查询所有学生)
def findKtAllStu(request):
    base_list = kt_student_view.find_kt_all_stus(request.GET.get('mainId'))
    stuNum = 0  # 学生总数
    qdNum = 0  # 已签到数量
    qdStudentIds = []  # 已签到的学生Id
    stuList = []  # 最终返回的学生对象列表(驼峰命名)
    if base_list and len(base_list):
        stuNum = len(base_list)
        for item in base_list:
            if "Y" == item['kt_status']:
                qdNum += 1
                qdStudentIds.append(item['student_id'])
            stuList.append(common_tools.dict_key_camelize(item))
    return common_tools.re_app_ok({'stuList': stuList, 'stuNum': stuNum, 'qdNum': qdNum, 'qdStudentIds': qdStudentIds, })


# 开始签到功能 - 如果为第1次操作, 那么需要存储签到手势
def startQianDao(request):
    mainId = request.GET.get('mainId')  # 课堂id
    qdKey = request.GET.get('qdKey')  # 签到手势字符串
    obj = zhkt_tools.init_main_by_id(mainId)
    if qdKey:
        # 更新主表的签到手势
        obj.qd_key = qdKey
        obj.save()
    else:
        qdKey = obj.qd_key
        if not qdKey:
            return common_tools.re_error('签到手势不能为空！')
    # 推送开启签到模式


# 结束签到 - 学生/一体机进入等待状态, 并统计到课人数
def endQianDao(request):
    mainId = request.GET.get('mainId')  # 课堂id
    zhkt_tools.anls_qian_dao(mainId)
    # todo


# 一体机使用 - 查询所有的互动题目
def baseActQuesList(request):
    mainId = request.GET.get('mainId')  # 课堂id
    result = act_ques_view.find_by_main_id(mainId, True)
    return common_tools.re_app_ok({'result': result})


# 开始一个互动
def startOneAct(request):
    mainId = request.GET.get('mainId')  # 课堂id
    actQuesId = request.GET.get('actQuesId')  # 互动题目Id
    answerLimitStr = request.GET.get('answerLimit')  # 限制回答人数(抢答时有效)
    answerLimit = int(answerLimitStr) if answerLimitStr else 1
    act_ques_view.start_one_act(mainId, actQuesId, answerLimit)


# 开始随机提问 - 返回所有的学生列表
def startActRandom(request):
    mainId = request.GET.get('mainId')  # 课堂id
    actQuesId = request.GET.get('actQuesId')  # 互动题目Id
    answerLimitStr = request.GET.get('answerLimit')  # 限制回答人数(抢答时有效)
    answerLimit = int(answerLimitStr) if answerLimitStr else 1
    act_ques_view.start_one_act(mainId, actQuesId, answerLimit)
    # 查询所有上课的学生
    sel_head = 'select t.student_id, t.student_name, t.student_gender '
    stuList = kt_student_view.find_list({'mainId': mainId}, sel_head, True)
    return common_tools.re_app_ok({'stuList': stuList})


# 结束1次互动 - 整合互动题目完成情况, 一体机/学生进入等待状态
def endOneAct(request):
    mainId = request.GET.get('mainId')  # 课堂id
    actQuesId = request.GET.get('actQuesId')  # 互动题目Id
    zhkt_tools.update_act_ques_anls(mainId, True, actQuesId)
    # todo 推送画屏/一体机/学生端


# 查看投票详情 (已结束的投票, 统计使用)
def actQuesAnls(request):
    mainId = request.GET.get('mainId')  # 课堂id
    actQuesId = request.GET.get('actQuesId')  # 题目Id
    anlsObj = stu_act_result_view.init_act_ques_anls(mainId, actQuesId)
    return common_tools.re_app_ok({'allStuNum': anlsObj['allStuNum'],  # 学生总数
                                   'isReplyNum': anlsObj['isReplyNum'],  # 作答人数
                                   'rightPercent': anlsObj['rightPercent'],  # 正确率
                                   'optAnlsList': anlsObj['optAnlsList'], })  # 投票选项人数统计


# 保存随机提问时, 所选的随机学生 - 同时通知画屏
def saveActRandomStus(request):
    studentIds = request.GET.get('studentIds')  # 回答学生Id集合
    actQuesId = request.GET.get('actQuesId')  # 回答的互动表Id
    mainId = request.GET.get('mainId')  # 课堂主表Id
    if not studentIds:
        return common_tools.re_error('请选择回答问题的学生！')
    stu_act_result_view.save_act_random_stus(studentIds=studentIds, actQuesId=actQuesId, mainId=mainId)
    return common_tools.re_app_ok()


# 记录学生互动时答题信息 (教师选择对错/评级) - 单个保存
def saveActStuResult(request):
    studentId = request.GET.get('studentId')  # 回答学生Id
    mainId = request.GET.get('mainId')
    actQuesId = request.GET.get('actQuesId')
    result = request.GET.get('result')  # 评价对错/评级(5星满级)
    rightResult = request.GET.get('rightResult')  # 是否回答正确
    stu_act_result_view.save_act_stu_result(mainId=mainId, actQuesId=actQuesId, studentId=studentId, rightResult=rightResult, result=result)
    return common_tools.re_app_ok()


# 教师评价学生, 查询评价指标及学生列表
def initTchQuotaBase(request):
    mainId = request.GET.get('mainId')
    stuList = kt_student_view.find_kt_all_stus(mainId, True)  # 上课学生列表, 使用驼峰返回字段
    baseQuotaList = zhkt_tools.init_stu_base_quota()  # 学生使用的评价项
    quotaList = common_tools.dict_list_key_camelize(baseQuotaList)
    return common_tools.re_app_ok({'stuList': stuList, 'quotaList': quotaList, })


# 更新教师的评价学生数据 - 支持批量保存 (一体机使用)
def updateTchQuotas(request):
    mainId = request.GET.get('mainId')
    id = request.GET.get('id')  # 更新的学生主表Id
    ids = request.GET.get('ids')  # 更新的学生主表Id(批量)
    studentIds = request.GET.get('studentIds')  # 更新的学生主表Id(批量)
    tchQuota = request.GET.get('tchQuota')  # 教师评语
    tchQuota = tchQuota if tchQuota else ''
    # 拼接更新语句
    sql = " update zhkt_student set tch_quota = %s, "
    sql_paras = [tchQuota]
    for num in range(1, constant.QUOTA_ITEM_MAX_NUM):
        tchSocre = request.GET.get('tchSocre' + num)
        if not tchSocre:
            sql += " tch_socre{} = %s, ".format(num)
            sql_paras.append(tchSocre)
    sql += " is_tch_quota = 'Y' "  # 评价状态改为已评价
    # 拼接where条件
    if id:
        sql += ' where id = %s '
        sql_paras.append(id)
    elif ids:
        sql += ' where id in ({}) '.format(" '" + ids.replace(",", "'','") + "' ")
    elif studentIds:
        sql += " where student_id in ({}) and main_id = '{}' ".format(" '" + studentIds.replace(",", "'','") + "' ", mainId)
    else:
        return
    db_tools.update_one_sql(sql)


# 通过zhkt_student子表Id, 查询一条记录
def oneZhktStudent(request):
    param_strs = {
        'mainId': request.GET.get('mainId'),
        'studentId': request.GET.get('studentId'),
    }
    result = kt_student_view.find_one(param_strs=param_strs, camelize=True)
    return common_tools.re_app_ok({'result': result})


# 课堂 - 测验基础信息
def initTestBase(request):
    mainId = request.GET.get('mainId')
    main = zhkt_tools.init_main_by_id(mainId)
    testHours = main.test_hours if main.test_hours else ''  # 测验分钟数
    testStatus = main.main_status if main.main_status else constant.QUES_STATUS_NEW
    quesTotal = len(zhkt_tools.init_test_ques_list())
    return common_tools.re_app_ok({'testHours': testHours, 'testStatus': testStatus, 'quesTotal': quesTotal, })


# 测验整体统计 (统计各题正确率) showType: 24004005 简答题, 0 无人回答, noAnswer 未设置正确答案
def testQuesAnls(request):
    mainId = request.GET.get('mainId')
    # 上课人数/回答人数统计
    totalMap = kt_student_view.test_total_map(mainId)
    # 统计各个测验题目的正确率(orderno/replyNum/rightPercent/missPercent/showType/showMsg)
    anlsData = stu_test_result_view.test_ques_right_anls(mainId)
    return common_tools.re_app_ok({
                'stuNum': totalMap['stuNum'],  # 班级总人数
                'daoKeNum': totalMap['daoKeNum'],  # 到课人数
                'testPubNum': totalMap['testPubNum'],  # 测验提交人数
                'anlsData': anlsData, })  # 各题目统计


# 测验单个题目统计
def testQuesDetail(request):
    mainId = request.GET.get('mainId')
    testQuesId = request.GET.get('testQuesId')
    testQues = zhkt_tools.test_ques_by_id(testQuesId)
    # 查询学生参与的测验答题结果
    testRsList = stu_test_result_view.one_ques_rs_list(mainId, testQuesId)
    if constant.QUES_TYPE_SHORT_ANSWER == testQues['ques_type']:  # 简答题
        quesAnswer = testQues['answer']  # 测验题的答案
        quesAnswer = common_tools.html_imgs_add_http(quesAnswer)  # 正则处理内部可能包含的图片
        stuAnswerList = common_tools.dict_list_key_camelize(testRsList)  # 转换为驼峰式, 供app端使用
        return common_tools.re_app_ok({'stuAnswerList': stuAnswerList, 'quesAnswer': quesAnswer, })
    else:  # 选择题/判断题, 统计各个选项
        anlsObj = stu_test_result_view.one_test_ques_anls(mainId, testQues, testRsList)
        return common_tools.re_app_ok({'optAnlsList': anlsObj['optAnlsList'], 'quesAnswer': anlsObj['quesAnswer'], })


# 开始测验
def startKtTest(request):
    mainId = request.GET.get('mainId')
    testHours = request.GET.get('testHours')  # 重新填写的测验分钟数
    main = zhkt_tools.init_main_by_id(mainId)
    main.test_status = constant.QUES_STATUS_START  # 测验进入开始状态
    main.test_start_time = common_tools.now()  # 测验开始时间
    if testHours:
        main.test_hours = testHours
    main.save()

    # todo 给画屏和学生端推消息


# 结束测验
def endKtTest(request):
    mainId = request.GET.get('mainId')
    main = zhkt_tools.init_main_by_id(mainId)
    main.test_status = constant.QUES_STATUS_END  # 测验进入结束状态
    main.save()

    # todo 通知画屏测验结束
