from base import constant, common_tools, db_tools

# 全局业务表表名
table_name = 'zhkt_stu_danmaku'


# 插入一个弹幕(学生发送的弹幕)
def ins_stu_danmaku(mainId, studentId, ps):
    row = {
        'main_id': mainId,
        'student_id': studentId,
        'ps': ps,  # 弹幕内容
        'user_type': constant.QUOTA_TYPE_STUDENT,  # 发送用户类型为学生
        'create_time': common_tools.now(),  # 发送弹幕时间
    }
    db_tools.ins_dict_to_db(table_name, row)  # 插入一条弹幕数据
