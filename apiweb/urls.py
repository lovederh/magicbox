from django.urls import path

from .appview import api_base_view, api_zhkt_view, wx_stu_zhkt_view
from base.appview import file_opt_view


app_name = 'apiWeb'
urlpatterns = [
    # 附件/图片相关
    path('dist/html/fileView.html', api_base_view.fileView),  # 附件预览页面
    path('api/repairTrain/viewPic', file_opt_view.viewPic),  # 预览图片
    path('api/repairTrain/viewThumbPic', file_opt_view.viewThumbPic),  # 预览缩略图
    path('wxs/common/viewPic', file_opt_view.viewPic),  # 预览图片
    path('wxs/common/viewThumbPic', file_opt_view.viewThumbPic),  # 预览缩略图
    path('wxs/common/viewMp4', file_opt_view.viewMp4),  # 预览图片
    # 智慧课堂(一体机/app端)
    path('aid/zhkt/zhktTestWebView.html', api_zhkt_view.zhktTestWebView),  # 测验题目webView
    path('api/zhkt/tchUseKtList', api_zhkt_view.tchUseKtList),  # 查找我的课堂
    path('api/zhkt/startKt', api_zhkt_view.startKt),  # 开始上课
    path('api/zhkt/endKt', api_zhkt_view.endKt),  # 下课(课堂结束)
    path('api/zhkt/findKtAllStu', api_zhkt_view.findKtAllStu),  # 查询所有参与课堂的学生
    path('api/zhkt/startQianDao', api_zhkt_view.startQianDao),  # 一体机开始签到
    path('api/zhkt/endQianDao', api_zhkt_view.endQianDao),  # 结束签到
    path('api/zhkt/baseActQuesList', api_zhkt_view.baseActQuesList),  # 一体机使用 - 查询所有的互动题目
    path('api/zhkt/startOneAct', api_zhkt_view.startOneAct),  # 开始一个互动
    path('api/zhkt/startActRandom', api_zhkt_view.startActRandom),  # 开始随机提问 - 返回所有的学生列表
    path('api/zhkt/endOneAct', api_zhkt_view.endOneAct),  # 结束1次互动
    path('api/zhkt/actQuesAnls', api_zhkt_view.actQuesAnls),  # 查看投票详情
    path('api/zhkt/saveActRandomStus', api_zhkt_view.saveActRandomStus),  # 保存随机提问时, 所选的随机学生
    path('api/zhkt/saveActStuResult', api_zhkt_view.saveActStuResult),  # 记录学生互动时答题信息 (教师选择对错/评级)
    path('api/zhkt/initTchQuotaBase', api_zhkt_view.initTchQuotaBase),  # 教师评价学生, 查询评价指标及学生列表
    path('api/zhkt/updateTchQuotas', api_zhkt_view.updateTchQuotas),  # 更新教师的评价学生数据
    path('api/zhkt/oneZhktStudent', api_zhkt_view.oneZhktStudent),  # 通过zhkt_student子表Id, 查询一条记录
    path('api/zhkt/initTestBase', api_zhkt_view.initTestBase),  # 课堂 - 测验基础信息
    path('api/zhkt/testQuesAnls', api_zhkt_view.testQuesAnls),  # 测验整体统计 (统计各题正确率)
    path('api/zhkt/testQuesDetail', api_zhkt_view.testQuesDetail),  # 测验单个题目统计
    path('api/zhkt/startKtTest', api_zhkt_view.startKtTest),  # 开始测验
    path('api/zhkt/endKtTest', api_zhkt_view.endKtTest),  # 结束测验
    # 智慧课堂(学生端)
    path('wxs/zhkt/myStartKtList', wx_stu_zhkt_view.myStartKtList),  # 返回当前盒子内, 已上课的课堂列表(一个)
    path('wxs/zhkt/sourceList', wx_stu_zhkt_view.sourceList),  # 课堂下, 所有资源列表 (不分页)
    path('wxs/zhkt/studentQianDao', wx_stu_zhkt_view.studentQianDao),  # 学生完成签到
    path('wxs/zhkt/saveTestQues', wx_stu_zhkt_view.saveTestQues),  # 保存学生测试题的结果
    path('wxs/zhkt/queryStuPjtchList', wx_stu_zhkt_view.queryStuPjtchList),  # 学生反馈 - 回显已评价数据
    path('wxs/zhkt/saveStuPjtch', wx_stu_zhkt_view.saveStuPjtch),  # 学生反馈 - 保存反馈的信息
]
