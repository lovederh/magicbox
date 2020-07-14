import requests
import urllib.request
import urllib
import socket


# 转码url字符串
def encode_url_para(para_str):
    res = urllib.parse.quote(para_str, '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


# 获取客户端ip
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# 向指定url发起get请求
def do_get(base_url, url_path, p={}):
    r = requests.get(base_url + url_path, params=p)
    return r.json()


# 向指定url发送post方法的请求
def do_post(base_url, url_path, json_data={}):
    r = requests.post(base_url + url_path, json=json_data)
    return r.json()


# 向指定url请求附件
def do_url_get_file(url, path_name):
    urllib.request.urlretrieve(url, path_name)


# 向指定url上传附件
def do_upload_file(url, file_path_name):
    files = {'file': open(file_path_name, 'rb')}
    r = requests.post(url, files=files)
    return r.json()


# 获取本机ip地址
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
