from django.db import models


# 基础评价项
class Base_Quota(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    label = models.CharField(max_length=200, null=True)  # 评价题干
    type = models.CharField(max_length=10, null=True)  # 类型stu学生被评价tch教师被评价
    orderNo = models.IntegerField(null=True)  # 排序


# zhkt_main
class Main(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    teacher_id = models.CharField(max_length=50, null=True)  # 教师id
    week_index = models.SmallIntegerField(null=True)  # 周次
    day_of_week = models.SmallIntegerField(null=True)  # 周几
    part_nums = models.CharField(max_length=50, null=True)  # 第几节(汉字)
    main_status = models.CharField(max_length=20, null=True)  # 课堂状态码
    re_start_time = models.CharField(max_length=20, null=True)  # 真正开始时间
    start_time = models.CharField(max_length=20, null=True)  # 计划开始时间
    end_time = models.CharField(max_length=20, null=True)  # 结束时间
    ps = models.CharField(max_length=500, null=True)  # 教学内容
    think_ps = models.CharField(max_length=2000, null=True)  # 教学反思
    stu_num = models.SmallIntegerField(null=True)  # 学生总数
    course_label = models.CharField(max_length=100, null=True)  # 课程名称
    venue = models.CharField(max_length=32, null=True)  # 上课场地Id
    venue_label = models.CharField(max_length=100, null=True)  # 上课场地
    data_key = models.CharField(max_length=8, null=True)  # 数据表
    test_hours = models.CharField(max_length=8, null=True)  # 测试分钟数
    qd_key = models.CharField(max_length=100, null=True)  # 签到手势
    year_month = models.CharField(max_length=10, null=True)  # 上课年月
    test_status = models.CharField(max_length=20, null=True)  # 测验状态
    test_start_time = models.CharField(max_length=20, null=True)  # 测验开始时间
    main_class_labels = models.CharField(max_length=500, null=True)  # 上课的班级名称


# zhkt_act_ques
class Act_Ques(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    ques_name = models.CharField(max_length=800, null=True)  # 题干
    ques_difficulty = models.SmallIntegerField(null=True)  # 题目难度(1-5)
    ability_project_label = models.CharField(max_length=50, null=True)  # 能力项目名称
    ques_type = models.CharField(max_length=20, null=True)  # 题目类型
    type = models.CharField(max_length=20, null=True)  # 互动类型
    evaluate_type = models.CharField(max_length=20, null=True)  # 评价方式(对错/评级)
    answer = models.CharField(max_length=800, null=True)  # 答案
    ques_status = models.CharField(max_length=20, null=True)  # 互动状态
    orderNo = models.IntegerField(null=True)  # 排序
    right_num = models.SmallIntegerField(null=True)  # 正确人数
    reply_num = models.SmallIntegerField(null=True)  # 回答人数
    know_labels = models.CharField(max_length=800, null=True)  # 知识点


# zhkt_act_ques_option
class Act_Ques_Option(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    act_ques_id = models.CharField(max_length=50, null=True)  # 题目id
    option_describe = models.CharField(max_length=500, null=True)  # 选项描述
    option_no = models.CharField(max_length=5, null=True)  # 选项序号
    orderNo = models.IntegerField(null=True)  # 排序
    is_answer = models.CharField(max_length=5, null=True)  # 是否答案


# zhkt_test_ques
class Test_Ques(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    ques_name = models.TextField(null=True)  # 题干
    ques_difficulty = models.SmallIntegerField(null=True)  # 题目难度(1-5)
    ability_project_label = models.CharField(max_length=50, null=True)  # 能力项目名称
    ques_type = models.CharField(max_length=20, null=True)  # 题目类型
    answer = models.CharField(max_length=800, null=True)  # 答案
    orderNo = models.IntegerField(null=True)  # 排序
    right_num = models.SmallIntegerField(null=True)  # 正确人数
    reply_num = models.SmallIntegerField(null=True)  # 回答人数
    opt_scope = models.CharField(max_length=20, null=True)  # 操作场景(pc/app)
    file_id = models.CharField(max_length=50, null=True)  # 使用的附件Id
    know_labels = models.CharField(max_length=800, null=True)  # 知识点


# zhkt_test_ques_option
class Test_Ques_Option(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    test_ques_id = models.CharField(max_length=50, null=True)  # 题目id
    option_describe = models.TextField(null=True)  # 选项描述
    option_no = models.CharField(max_length=5, null=True)  # 选项序号
    orderNo = models.IntegerField(null=True)  # 排序
    is_answer = models.CharField(max_length=5, null=True)  # 是否答案


# zhkt_main_source
class Main_Source(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    create_time = models.CharField(max_length=20, null=True)  # 添加时间
    is_pub = models.CharField(max_length=1, null=True)  # 是否公开
    sr_status = models.CharField(max_length=20, null=True)  # 资源状态
    file_id = models.CharField(max_length=50, null=True)  # 关联附件id
    ps = models.CharField(max_length=500, null=True)  # 资源介绍
    label = models.CharField(max_length=100, null=True)  # 资源名称
    file_type = models.CharField(max_length=20, null=True)  # 资源文件类型
    file_label = models.CharField(max_length=200, null=True)  # 附件名称
    preview_num = models.SmallIntegerField(null=True)  # 预览次数
    know_labels = models.CharField(max_length=800, null=True)  # 知识点


# zhkt_main_group
class Main_Group(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    orderNo = models.IntegerField(null=True)  # 排序
    ps = models.CharField(max_length=500, null=True)  # 备注
    label = models.CharField(max_length=100, null=True)  # 小组名称
    stu_num = models.SmallIntegerField(null=True)  # 小组人数
    re_stu_num = models.SmallIntegerField(null=True)  # 小组真实人数
    total_bonus = models.SmallIntegerField(null=True)  # 小组总积分
    bonus_sort = models.SmallIntegerField(null=True)  # 积分排名


# zhkt_student
class Student(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    student_id = models.CharField(max_length=50, null=True)  # 学生id
    student_gender = models.CharField(max_length=20, null=True)  # 学生性别
    student_name = models.CharField(max_length=20, null=True)  # 学生姓名
    student_pic_path = models.CharField(max_length=100, null=True)  # 学生头像
    group_id = models.CharField(max_length=50, null=True)  # 所属小组
    is_group_leader = models.CharField(max_length=1, null=True)  # 是否小组组长
    kt_status = models.CharField(max_length=20, null=True)  # 签到状态
    bonus = models.SmallIntegerField(null=True)  # 积分
    act_num = models.SmallIntegerField(null=True)  # 参与互动次数
    is_tch_quota = models.CharField(max_length=1, null=True)  # 教师是否已对学生进行评价
    tch_quota = models.CharField(max_length=500, null=True)  # 教师对学生评价文字
    is_to_pj_tch = models.CharField(max_length=1, null=True)  # 学生是否已经反馈
    to_pj_tch = models.CharField(max_length=500, null=True)  # 学生对教师评价文字
    to_pj_tch_time = models.CharField(max_length=20, null=True)  # 学生对教师评价时间
    pub_test_time = models.CharField(max_length=20, null=True)  # 提交测验结果时间
    tch_socre0 = models.SmallIntegerField(null=True)  # 教师评价项
    tch_socre1 = models.SmallIntegerField(null=True)
    tch_socre2 = models.SmallIntegerField(null=True)
    tch_socre3 = models.SmallIntegerField(null=True)
    tch_socre4 = models.SmallIntegerField(null=True)
    tch_socre5 = models.SmallIntegerField(null=True)
    tch_socre6 = models.SmallIntegerField(null=True)
    tch_socre7 = models.SmallIntegerField(null=True)
    tch_socre8 = models.SmallIntegerField(null=True)
    tch_socre9 = models.SmallIntegerField(null=True)
    pj_tch_score0 = models.SmallIntegerField(null=True)  # 学生评价教师
    pj_tch_score1 = models.SmallIntegerField(null=True)
    pj_tch_score2 = models.SmallIntegerField(null=True)
    pj_tch_score3 = models.SmallIntegerField(null=True)
    pj_tch_score4 = models.SmallIntegerField(null=True)
    pj_tch_score5 = models.SmallIntegerField(null=True)
    pj_tch_score6 = models.SmallIntegerField(null=True)
    pj_tch_score7 = models.SmallIntegerField(null=True)
    pj_tch_score8 = models.SmallIntegerField(null=True)
    pj_tch_score9 = models.SmallIntegerField(null=True)


# zhkt_stu_act_result
class Stu_Act_Result(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    student_id = models.CharField(max_length=50, null=True)  # 学生id
    act_ques_id = models.CharField(max_length=50, null=True)  # 互动题目表的Id
    is_reply_answer = models.CharField(max_length=1, null=True)  # 是否真正参与作答Y/N(可能举手了但是没有回答)
    right_result = models.CharField(max_length=5, null=True)  # 是否回答正确Y/N
    is_hand_up = models.CharField(max_length=1, null=True)  # 举手标记Y/N
    result = models.CharField(max_length=20, null=True)  # 结果评级
    create_time_stamp = models.BigIntegerField(null=True)  # 举手抢答时间戳
    create_time = models.CharField(max_length=20, null=True)  # 回答时间
    bonus = models.SmallIntegerField(null=True)  # 单次积分


# zhkt_stu_test_result
class Stu_Test_Result(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    student_id = models.CharField(max_length=50, null=True)  # 学生id
    test_ques_id = models.CharField(max_length=50, null=True)  # 测验题目表的Id
    right_result = models.CharField(max_length=5, null=True)  # 是否回答正确Y/N
    answer = models.CharField(max_length=800, null=True)  # 回答的答案
    orderNo = models.IntegerField(null=True)  # 排序


# zhkt_stu_danmaku 学生弹幕表
class Stu_Danmaku(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    main_id = models.CharField(max_length=50, null=True)  # 课堂id
    student_id = models.CharField(max_length=50, null=True)  # 学生id
    create_time = models.CharField(max_length=20, null=True)  # 弹幕时间
    ps = models.CharField(max_length=200, null=True)  # 弹幕内容
    user_type = models.CharField(max_length=20, null=True)  # 发弹幕人员类型
