import os


# 当通过 python3 manage.py runserver的时候，会调用二次BaseConfig的ready()方法，其中一个是监听文件是否被改变的
# 在正式环境中，如果也采用python3 manage.py runserver 应该加参数 python3 manage.py runserver --noreload
if os.environ.get('RUN_MAIN', None) != 'true':
    default_app_config = 'base.apps.BaseConfig'
