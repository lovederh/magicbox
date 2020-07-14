import os
from django.shortcuts import render

from base.models import Files


# app - 附件预览
def fileView(request):
    fileId = request.GET.get('fileId')  # 预览的附件id
    phoneType = request.GET.get('phoneType')  # 操作系统(安卓/ios)
    # 当前附件的对象信息
    file_info = Files.objects.filter(id=fileId).first()
    file_path = file_info.file_path
    file_type = file_info.file_type
    ext_file_name = file_info.ext_file_name  # 扩展的附件名
    file_name = file_info.file_name
    # 根据文件类型判断预览类型
    viewType = 'error'  # 默认不支持预览
    src = '/upload/' + file_path.replace(os.sep, '/') + '/' + file_name
    if file_type in ['bmp', 'gif', 'jpe', 'jpeg', 'jpg', 'png', 'ico', 'tif', 'tiff']:
        viewType = 'img'  # 图片类型
    elif file_type in ['mp4', 'webm', 'mov', 'ogg', 'swf']:
        viewType = 'video'  # 视频类型
    elif 'pdf' == file_type:
        viewType = 'pdf'  # pdf文件
    elif 'mp3' == file_type:
        viewType = 'mp3'  # mp3格式音频
    elif 'wav' == file_type:
        viewType = 'wav'  # wav格式音频
    elif ext_file_name:
        src = '/upload/' + file_path.replace(os.sep, '/') + '/' + ext_file_name
        # 判断扩展文件的类型
        ext_file_type = ext_file_name[ext_file_name.rindex('.') + 1:]
        if 'html' == ext_file_type:
            viewType = 'html'
        elif 'pdf' == ext_file_type:
            viewType = 'pdf'

    context = {
        'phoneType': phoneType if phoneType else '',
        'viewType': viewType,
        'src': src  # 最终预览文件对应的路径
    }
    return render(request, "apiweb/file_view.html", context)
