# 智慧魔盒

### 项目初始化

* 安装Django框架
```shell 
    pip3 install Django
```    
* 安装pymysql
```shell
    pip3 install pymysql
```    
* 安装websocket框架
```shell
    pip3 install dwebsocket
```    
* 安装op设备管理
```shell
    pip3 install openwrt-luci-rpc
```

# 当通过 python3 manage.py runserver的时候，会调用二次BaseConfig的ready()方法，其中一个是监听文件是否被改变的
# 在正式环境中，如果也采用python3 manage.py runserver 应该加参数 python3 manage.py runserver --noreload
