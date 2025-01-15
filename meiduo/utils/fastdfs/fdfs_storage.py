# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/15 10:01   -- yh 
# @文件名:      fdfs_storage.py

from django.core.files.storage import Storage
from meiduo.settings import dev_settings


class FastDFSStorage(Storage):
    """自定义文件存储系统，修改存储的方案"""
    def __init__(self, fdfs_base_url=None):
        """
        构造方法，可以不带参数，也可以携带参数
        :param fdfs_base_url: Storage的IP
        """
        self.fdfs_base_url = fdfs_base_url or dev_settings.FDFS_BASE_URL

    def _open(self, name, mode='rb'):
        # 打开文件时调用 : 文档说必须重写
        pass

    def _save(self, name, content):
        # 同上
        # 将来在后台管理系统中,需要在这个方法中实现文件上传到FastDFS服务器
        pass

    def url(self, name):
        """
        返回name所指文件的绝对URL,返回文件的全路径
        :param name: 要读取文件的引用:group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
        :return: http://192.168.103.158:8888/group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
        """
        # return self.fdfs_base_url + name
        # return "http://23.95.240.187:8888/" + name
        print(f"Base URL: {self.fdfs_base_url}")  # 调试输出
        print(f"File name: {name}")  # 调试输出
        if not self.fdfs_base_url:
            raise ValueError("The base URL for file storage is not set.")
        return ''.join([self.fdfs_base_url, name])