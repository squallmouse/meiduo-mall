# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/4 08:37   -- yh 
# @文件名:      ccp_sms.py

from ronglian_sms_sdk import SmsSDK

accId = '2c94811c9416ed0101942b2644db0294'
accToken = '108832996b4d4d98aad789bf1d7ed3c9'
appId = '2c94811c9416ed0101942b26468b029c'


class CCP(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls._instance.rest = SmsSDK(accId, accToken, appId)
        return cls._instance


    def send_message(self,mobile,smsCode):

        tid = '1'
        datas = (smsCode, '5')# 4 为短信时间
        resp = self.rest.sendMessage(tid, mobile, datas)


if __name__ == '__main__':
    CCP().send_message("13693542024","5678")
