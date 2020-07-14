from base import common_tools, http_tools

from django.test import TestCase

from zhkt.models import Main


class ModelTest(TestCase):

    def setUp(self):
        pass

    def test_dict_list_key_camelize(self):
        arr = [{'test_id': '123', 'test_name': '张三'}, {'test_id': '123456', 'test_name': '张三2'}]
        rs = common_tools.dict_list_key_camelize(arr)
        # print(rs)
        self.assertEqual(rs[0].get('testId'), '123')

    def test_dict_key_camelize(self):
        arr = {'test_id': '123', 'test_name': '张三', 'testLabel': '张三555'}
        rs = common_tools.dict_key_camelize(arr)
        # print(rs)
        self.assertEqual(rs.get('testId'), '123')

    def test_get_host_ip(self):
        rs = http_tools.get_host_ip()
        print('get_host_ip: ', rs, type(rs))
        self.assertEqual(str(type(rs)), "<class 'str'>")

    def test_html_find_img_ids(self):
        content_str = r'''<p>单选 - 测验&nbsp;
                        <img src="/hongyang-security/sys/file/viewPic?id=2ecda1271d0f41f59429db7725e968d0" width="112" height="25"/>, 试证明, 勾股定理
                        <img src="/hongyang-security/sys/file/viewPic?id=2ecda1271d0f41f59429db7725e968d2" width="111" height="22"/>, 试证明, xx定理</p> '''
        rs = common_tools.html_find_img_ids(content_str)
        print('html_find_img_ids: ', rs, type(rs), len(rs))
        rs = common_tools.html_imgs_add_http(content_str)
        print('html_imgs_add_http: ', rs)
        self.assertEqual(str(type(rs)), "<class 'str'>")

    def test_model_key_camelize(self):
        main = Main(teacher_id="菜鸟教程", week_index=30, part_nums="菜鸟出版社", re_start_time="2008-8-8", ps='ps', think_ps='think_ps')
        rs = common_tools.model_camelize_2dict(main)
        print('model_camelize_2dict: ', rs)
        self.assertEqual(rs['teacherId'], "菜鸟教程")
