import os
import re
import datetime

import zipfile
import pymysql
import requests

from wsgiref.util import FileWrapper

from django.shortcuts import HttpResponse
from django.http import StreamingHttpResponse

from base.models import Files
from base.constant import SCH_IP_CONF_KEY
from base.appview import config_view
from base import common_tools, db_tools, http_tools

# 全局业务表表名
table_name = 'base_files'


# 从远程现在压缩包, 并存储在base_file表
def down_from_remote(request):
    base_dir = os.getcwd()  # 当前工作目录(zhihuimohe4py基路径)
    remote_ids = request.GET.get('remote_ids')  # 远程的附件Id
    old_files = Files.objects.filter(id__in=remote_ids.split(','))
    if old_files and len(old_files):
        sql_list = []
        for old_file in old_files:
            # 数据库信息删除
            sql_list.append("delete from " + table_name + " where id = '" + old_file.id + "' ")
            # 删除之前版本附件
            old_file_path = os.path.join(base_dir, 'upload', old_file.file_path, old_file.file_name)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            if old_file.ext_file_name:
                old_file_path = os.path.join(base_dir, 'upload', old_file.file_path, old_file.ext_file_name)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
        db_tools.update_sql_list(sql_list)

    # 获取学校的服务器路径
    sch_url = config_view.init_val_by_key(SCH_IP_CONF_KEY)
    url = sch_url + '/sys/file/genZipByFileIds?ids=' + remote_ids  # 请求生成压缩包, 得到使用的远程文件全路径
    remote = http_tools.do_post(url)  # 生成附件信息中, 包含远程服务器的硬盘路径
    remote_path = remote['path']
    remote_separator = remote['separator']
    # 执行附件的下载(支持断点续传)
    url = sch_url + '/sys/file/downloadByPath?path=' + http_tools.encode_url_para(remote_path)  # 远程文件路径

    # 按照年月日构造文件夹
    cur_datetime = datetime.datetime.now()
    year_str = datetime.datetime.strftime(cur_datetime, '%Y')
    month_str = datetime.datetime.strftime(cur_datetime, '%m')
    day_str = datetime.datetime.strftime(cur_datetime, '%d')
    relative_path = os.path.join(year_str, month_str, day_str)
    # 最终存放所有下载附件的路径
    file_path = os.path.join(base_dir, 'upload', relative_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)  # 文件夹不存在则创建
    # 利用毫秒级时间戳作为zip文件名
    zip_name = remote_path[remote_path.rindex(remote_separator) + 1:]
    zip_path_name = os.path.join(file_path, zip_name)  # 下载文件的绝对路径

    try:
        # 先看看本地文件下载了多少(保证断点续传)
        if os.path.exists(zip_path_name):
            temp_size = os.path.getsize(zip_path_name)  # 本地已经下载的文件大小
        else:
            temp_size = 0
        headers = {'Range': 'bytes=%d-' % temp_size}  # 核心部分: 这个是请求下载时, 从本地文件已经下载过的后面下载
        # 重新请求网址, 加入新的请求头的
        r = requests.get(url, stream=True, verify=False, headers=headers)
        # "ab"表示追加形式写入文件
        with open(zip_path_name, "ab") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()

        # 解压缩zip
        zip_file = zipfile.ZipFile(zip_path_name, 'r')
        for file in zip_file.namelist():
            zip_file.extract(file, file_path)

        # 读取file_infos.txt
        txt_path_name = os.path.join(file_path, "file_infos.txt")
        txt_file = open(txt_path_name, "r", encoding="utf-8")  # 读取的文件对象
        file_list = []
        relative_path = pymysql.escape_string(relative_path)  # 执行mysql转义, 防止读取出来的路径不可用
        for line in txt_file:  # 设置文件对象并读取每一行文件
            info = line.split(',')  # id,fileName,fileRealName,fileSize,fileType,extFileName
            data = {
                'id': info[0],
                'file_name': info[1],
                'file_real_name': info[2],
                'file_size': info[3],
                'file_type': info[4],
                'ext_file_name': info[5].strip() if info[5] else '',  # 去掉首尾空白, 防止出现换行符
                'file_path': relative_path,  # 相对路径
            }
            file_list.append(data)
        # 批量保存附件集合
        db_tools.ins_batch_to_db(table_name, file_list)
    except Exception as ex:
        print("Unexpected error:", ex)
        return common_tools.re_error()
    else:
        return common_tools.re_ok()
    finally:
        if zip_file:
            zip_file.close()  # 关闭文件
        if txt_file:
            txt_file.close()  # 关闭文件
        if txt_path_name:
            os.remove(txt_path_name)  # 删除file_infos.txt
        os.remove(zip_path_name)  # 删除zip文件


# 上传附件到学校服务器(支持断点续传)
def up_file_to_sch(request):
    base_dir = os.getcwd()  # 当前工作目录(zhihuimohe4py基路径)
    id = request.GET.get('id')  # 要上传的附件id
    file_info = Files.objects.filter(id=id).first()
    if file_info and file_info.id:
        file_path_name = os.path.join(base_dir, 'upload', file_info.file_path, file_info.file_name)
        sch_url = config_view.init_val_by_key(SCH_IP_CONF_KEY)
        url = sch_url + '/sys/file/uploadRange?fileName=' + file_info.file_name  # 远程上传文件路径
        http_tools.do_upload_file(url, file_path_name)
        return common_tools.re_ok()
    return common_tools.re_error()


# 图片预览
def viewPic(request):
    base_dir = os.getcwd()  # 当前工作目录(zhihuimohe4py基路径)
    id = request.GET.get('id')  # 预览的图片id
    file_info = Files.objects.filter(id=id).first()
    # 利用图片所在路径, 提供下载
    if file_info and file_info.id:
        file_path_name = os.path.join(base_dir, 'upload', file_info.file_path, file_info.file_name)
        return _download_by_path(file_path_name, True)
    return common_tools.re_error()


# 预览图片缩略图
def viewThumbPic(request):
    base_dir = os.getcwd()  # 当前工作目录(zhihuimohe4py基路径)
    id = request.GET.get('id')  # 预览的图片id
    file_info = Files.objects.filter(id=id).first()
    # 利用图片所在路径, 提供下载
    if file_info and file_info.id:
        file_name = file_info.ext_file_name
        file_path = os.path.join(base_dir, 'upload', file_info.file_path)
        # 判断缩略图是否存在
        if not os.path.exists(os.path.join(file_path, file_name)):
            file_name = file_info.file_name  # 缩略图不存在, 则使用原图预览
        file_path_name = os.path.join(file_path, file_name)
        return _download_by_path(file_path_name, True)
    return common_tools.re_error()


# 预览mp4视频
def viewMp4(request):
    base_dir = os.getcwd()  # 当前工作目录(zhihuimohe4py基路径)
    id = request.GET.get('id')  # 预览的附件id
    file_info = Files.objects.filter(id=id).first()
    if file_info and file_info.id:
        file_size = int(file_info.file_size)
        file_path_name = os.path.join(base_dir, 'upload', file_info.file_path, file_info.file_name)
        # 判断Range
        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
        range_match = range_re.match(range_header)
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = first_byte + 1024 * 1024 * 4  # 4M每片, 响应体最大体积
            if last_byte >= file_size:
                last_byte = file_size - 1
            length = last_byte - first_byte + 1
            resp = StreamingHttpResponse(_file_iterator(file_path_name, offset=first_byte, length=length), status=206)
            resp['Content-Length'] = str(length)
            resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, file_size)
        else:
            # 不是以视频流方式的获取时, 以生成器方式返回整个文件, 节省内存
            resp = StreamingHttpResponse(FileWrapper(open(file_path_name, 'rb')))
            resp['Content-Length'] = file_info.file_size
            resp['Content-Disposition'] = 'attachment;filename="{}"'.format(file_info.file_name)  # 视频名称
        resp['Accept-Ranges'] = 'bytes'
        resp['Content-Type'] = 'application/octet-stream'
        return resp
    return common_tools.re_error()


# 通过id提供文件下载
def downloadById(request):
    base_dir = os.getcwd()  # 当前工作目录(zhihuimohe4py基路径)
    id = request.GET.get('id')  # 预览的附件id
    file_info = Files.objects.filter(id=id).first()
    # 利用图片所在路径, 提供下载
    if file_info and file_info.id:
        file_path_name = os.path.join(base_dir, 'upload', file_info.file_path, file_info.file_name)
        return _download_by_path(file_path_name)
    return common_tools.re_error()


# 通过相对路径执行下载
def downByRelativePath(request, relative_path_name):
    base_dir = os.getcwd()  # 当前工作目录(zhihuimohe4py基路径)
    file_path_name = os.path.join(base_dir, 'upload', relative_path_name.replace('/', os.sep))  # 文件所在全路径
    # 判断文件类型是否为html
    file_type = relative_path_name[relative_path_name.rindex('.') + 1:]  # 文件类型
    if 'html' == file_type:
        html_file = open(file_path_name, 'r', encoding="utf-8")
        html_txt = html_file.read()
        return HttpResponse(html_txt)
    else:
        return _download_by_path(file_path_name)


# 通过指定路径, 提供附件下载
def _download_by_path(file_path_name, img_type_flag=False):
    file_name = file_path_name[file_path_name.rindex(os.sep) + 1:]  # 文件名称
    try:
        # 设置响应头
        response = StreamingHttpResponse(_file_iterator(file_path_name))  # StreamingHttpResponse将文件进行流式传输(数据量大可用这个方法)
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)  # Content-Disposition下载默认文件名
        # 确认文件对应的Content-Type
        content_type = 'application/octet-stream'  # 以流的形式下载文件, 这样可以实现任意格式的文件下载
        if img_type_flag:
            response['Content-Type'] = 'image/png'  # 图片类型
        response['Content-Type'] = content_type
    except Exception as ex:
        print("Unexpected error:", ex)
        return common_tools.re_error()
    return response


# 切片读取附件
def _file_iterator(temp_path_name, chunk_size=1024, offset=0, length=None):
    with open(temp_path_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data
