# -*- coding:utf-8 -*-
from base import common_tools
from django.views.decorators.csrf import csrf_exempt
import json
from base.logs import Log
import logging
# 服务列表数据{'imac':(ip, port), 'ytj': (ip, port)}
logger = logging.getLogger(__name__)


class Singleton_service(object):
    services = {}

    def put(self, k, v):
        self.services[k] = v
        log = Log("services", "服务注册成功 = 》" + json.dumps(v))
        log.record()

    def get_services(self):
        return self.services

    def get_services_by_type(self, s_type):
        if s_type in self.services:
            return self.services[s_type]
        else:
            return []


singleton_service = Singleton_service()


@csrf_exempt
def service_regist(request):
    jsonData = json.loads(request.body)
    service_type = jsonData.get('service_type')
    if not service_type:
        return common_tools.re_error("service_type 不能为空")
    ip = jsonData.get('ip')
    port = jsonData.get('port')
    mac = jsonData.get('mac')
    version = jsonData.get('version')
    services = singleton_service.get_services_by_type(service_type)
    if services:
        if [True for service in services if mac in service]:
            pass
        else:
            services.append({mac: (ip, port, mac, version)})
    else:
        services = []
        services.append({mac: (ip, port, mac, version)})
    singleton_service.put(service_type, services)
    logger.info("服务注册成功了", services)
    return common_tools.re_ok()
