from django.http import JsonResponse

import re
import time
import uuid
import binascii

from base.appview import config_view


# 字典key, 下划线转换为驼峰
def key_str_camelize(s):
    if "_" in s:
        temp_arr = s.split("_")
        arr = [temp.capitalize() for temp in temp_arr[1:]]  # 驼峰转换从第2个单词开始
        return temp_arr[0] + "".join(arr)
    else:
        return s


# 字典对象, 转换为驼峰形式key
def dict_key_camelize(data):
    return {key_str_camelize(k): (v if v else '') for (k, v) in data.items()}


# django Model 转换为驼峰式对象
def model_camelize_2dict(model):
    field_list = model._meta.get_fields()  # model下所有的字段
    result = {}  # 最终返回结果
    for x in field_list:
        val = model.__getattribute__(x.attname)
        result[key_str_camelize(x.attname)] = val if val else ''
    return result


# 字典集合, key转换为驼峰式
def dict_list_key_camelize(arr):
    rs = []
    if arr and len(arr):
        # 取第一个字典, 整理key与驼峰key对应关系
        key_2camelize = {key: key_str_camelize(key) for key in arr[0]}
        for data in arr:
            rs.append({key_2camelize[k]: (v if v else '') for (k, v) in data.items()})
    return rs


# 获取当前时间
def now():
    return get_ymdhms_time()


# 获取当前日期
def today():
    return get_ymd_date()


# 格式化当前时间(年-月-日)格式字符串
def get_ymd_date(time_array=None):
    time_array = time_array if time_array else time.localtime()
    return time.strftime("%Y-%m-%d", time_array)


# 格式化当前时间(年-月-日 时:分:秒)格式字符串
def get_ymdhms_time(time_array=None):
    time_array = time_array if time_array else time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


# 格式化当前时间, 得到YYYY-MM格式字符串
def get_year_month(time_array=None):
    time_array = time_array if time_array else time.localtime()
    return time.strftime("%Y-%m", time_array)


# 返回成功结果(code=0), 传递字典 - pc/小程序原接口使用
def re_ok(data={}):
    return _re_json(data)


# 返回成功结果(code=200), 传递字典 - app端使用
def re_app_ok(data={}):
    data['code'] = 200
    return _re_json(data)


# 返回错误提示(code=500)
def re_error(msg=''):
    data = {'msg': msg}
    return _re_json(data, True)


def _re_json(data, error_flag=False):
    if error_flag:
        if 'code' not in data:
            data['code'] = '500'
        if 'msg' not in data or not data['msg']:
            data['msg'] = '处理失败，请重试！'
    else:
        if 'code' not in data:
            data['code'] = '0'
        if 'msg' not in data:
            data['msg'] = '处理成功！'
    return JsonResponse(data)


# <img>标签处理 - 获取包含的附件id集合
def html_find_img_ids(content_str):
    result = []
    if content_str:
        match_list = re.findall(r'<img[^>]*?src=("[^>]*?/sys/file/viewPic\?id=([^>]*?)"){1}[^>]*?\/>', content_str)
        if match_list and len(match_list):
            for match_arr in match_list:
                result.append(match_arr[1])
    return result


# <img>标签处理 - 处理为外网地址相关路径(小程序展示时使用)
def html_imgs_add_http(content_str):
    result = content_str  # 最终替换后的图片访问路径
    if content_str:
        match_list = re.findall(r'<img[^>]*?src=("[^>]*?/sys/file/viewPic\?id=([^>]*?)"){1}[^>]*?\/>', content_str)
        if match_list and len(match_list):
            mh_http = config_view.load_mh_http()  # 盒子的http://ip:端口
            for match_arr in match_list:
                old_src = match_arr[0]
                new_src = '"{mh_http}/sys/file/viewPic?id={pic_id}"'.format(mh_http=mh_http, pic_id=match_arr[1])
                result = result.replace(old_src, new_src)
    return result


# 生成一串uuid
def gen_uuid():
    return str(uuid.uuid1()).replace("-", "")


# 字符串 >> 二进制 >> hex >> hex 字符串
def str_to_hexstr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')


# hex 字符串 >> hex >> 二进制 >> 字符串
def hexstr_to_str(hex_str):
    hex = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hex)
    return str_bin.decode('utf-8')


# byte 转hexstr
def bytes_to_hexstr(bytestr):
    return bytestr.hex()


# hexstr 转 bytes
def hexstr_to_bytes(hex_str):
    return bytes.fromhex(hex_str)


# bytes >> str
def bytes_to_str(bytestr):
    return hexstr_to_str(bytes_to_hexstr(bytestr))


# 获取设备mac地址
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return mac
