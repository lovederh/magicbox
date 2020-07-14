from base import constant, db_tools

# 全局业务表表名
table_name = 'zhkt_main_source'


def find_list(param_strs={}, sel_head=" select t.* ", camelize=False, my_default_sidx=None):
    sql_from_where = init_from_where_sql(param_strs)
    sql = sel_head + sql_from_where
    if my_default_sidx:
        sql += ' order by ' + my_default_sidx
    return db_tools.find_dict_list_by_sql(sql, camelize)


# 整合查询用户的原生sql
def init_from_where_sql(params):
    mainId = params['mainId'] if 'mainId' in params else ''
    srStatus = params['srStatus'] if 'srStatus' in params else ''
    isPub = params['isPub'] if 'isPub' in params else ''
    fileType = params['fileType'] if 'fileType' in params else ''
    sql = " from base_files f, {} t where f.id = t.file_id ".format(table_name)
    if isPub:
        sql += " and t.is_pub = '" + isPub + "' "
    if srStatus:
        sql += " and t.sr_status = '" + srStatus + "' "
    if fileType:
        sql += " and t.file_type = '" + fileType + "' "
    if mainId:
        sql += " and t.main_id = '" + mainId + "' "
    return sql


# 查询课堂使用的资源列表(学生app端使用)
def main_source_list(mainId):
    param_strs = {
        'mainId': mainId,
        'srStatus': constant.SOURCE_STATUS_OK,  # 只查询已发布的
    }
    sel_head = """ select t.id,
                        t.file_id as fileId,
                        t.ps,
                        t.file_type as fileType,
                        t.label as fileRealName,
                        f.file_path as filePath,
                        f.file_name as fileName,
                        f.ext_file_name as extFileName """
    srList = find_list(param_strs, sel_head)
    if srList and len(srList):
        for row in srList:
            fileType = row['fileType']  # 整合文件类型对应汉字
            if fileType in ['bmp', 'gif', 'jpe', 'jpeg', 'jpg', 'png', 'ico', 'tif', 'tiff']:
                row['fileTypeLabel'] = '图片'
            elif fileType in ['mp4', 'webm', 'mov', 'ogg', 'swf']:
                row['fileTypeLabel'] = '视频'
            elif fileType in ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']:
                row['fileTypeLabel'] = '文档'
            else:
                row['fileTypeLabel'] = '图片'
    return srList
