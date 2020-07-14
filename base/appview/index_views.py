from django.shortcuts import render


# 首页
def to_index(request):
    context = {}
    return render(request, "base/index.html", context)
