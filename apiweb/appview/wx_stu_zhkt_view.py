from base import constant, common_tools, db_tools

from zhkt import zhkt_tools
from zhkt.appview import kt_student_view, main_source_view, stu_test_result_view


# 返回当前盒子内, 已上课的课堂列表(理论上只有至多一个)
def myStartKtList(request):
    # 判断盒子内的课堂状态
    main = zhkt_tools.cache['main']
    kt_list = []
    if main and main.main_status == constant.KT_STATUS_START:
        kt_list.append(common_tools.model_camelize_2dict(main))
    return common_tools.re_ok({'result': kt_list, })


# 课堂下, 所有资源列表 (不分页)
def sourceList(request):
    mainId = request.GET.get('mainId')
    result = main_source_view.main_source_list(mainId)
    return common_tools.re_ok({'result': result, })


# 学生完成签到
def studentQianDao(request):
    param_strs = {
        'mainId': request.GET.get('mainId'),
        'studentId': request.GET.get('studentId'),
    }
    sel_head = ' select t.id, t.kt_status, t.student_id '
    kt_stu = kt_student_view.find_one(param_strs, sel_head)
    if "Y" == kt_stu['kt_status']:
        return common_tools.re_error('你已经签到过了！')
    kt_stu['kt_status'] = 'Y'
    db_tools.upd_dict_to_db(kt_student_view.table_name, kt_stu)

    # todo 推动到一体机


# 保存学生测试题的结果 - 更新学生主表的测试结果 (整体保存)
def saveTestQues(request):
    mainId = request.GET.get('mainId')
    studentId = request.GET.get('studentId')
    quesListStr = request.GET.get('quesList')
    stu_test_result_view.save_stu_test_result(mainId=mainId, studentId=studentId, quesListStr=quesListStr)
    return common_tools.re_ok()


# 学生反馈 - 查询老师被评价指标, 同时回显已评价数据
def queryStuPjtchList(request):
    param_strs = {
        'mainId': request.GET.get('mainId'),
        'studentId': request.GET.get('studentId'),
    }
    kt_stu = kt_student_view.find_one(param_strs)
    toPjTch = kt_stu['to_pj_tch'] if kt_stu['to_pj_tch'] else ''  # 学生对教师的评语
    # 整理学生评价教师使用的指标, 同时把各项已有评价结果放入
    baseQuotaList = zhkt_tools.init_tch_base_quota()
    jsonData = []
    for baseQuota in baseQuotaList:
        num = kt_stu['pj_tch_score{}'.format(baseQuota['orderNo'])]
        jsonData.append({
            'id': baseQuota['id'],
            'label': baseQuota['label'],
            'orderNo': baseQuota['orderNo'],
            'num': num,  # 当前指标项的得分
        })
    return common_tools.re_ok({'jsonData': jsonData, 'toPjTch': toPjTch})


# 学生反馈 - 保存反馈的信息
def saveStuPjtch(request):
    mainId = request.GET.get('mainId')
    studentId = request.GET.get('studentId')
    toPjTch = request.GET.get('toPjTch')  # 学生对教师的评语
    quotaStr = request.GET.get('quotaStr')
    kt_student_view.save_stu_pj_tch(mainId=mainId, studentId=studentId, toPjTch=toPjTch, quotaStr=quotaStr)
    return common_tools.re_ok()
