# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/4 08:37   -- yh 
# @文件名:      ccp_sms.py
import json
import logging

from ronglian_sms_sdk import SmsSDK

expiration_time = 300

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

    def send_message(self, tid, mobile, smsCode):
        """
        发送短信验证码
        :param mobile:
        :param smsCode:
        :return: 短信发送成功 0 ; 短信发送失败 -1
        """

        # tid = '1'
        time_str = str(expiration_time // 60)
        datas = (smsCode, time_str)  # time_str 为短信时间
        resp_str = self.rest.sendMessage(tid, mobile, datas)
        respDict = json.loads(resp_str)
        if respDict.get('statusCode') == '000000':
            # 正常返回0
            print("短信发送成功")
            print(respDict.get('statusCode'))
            return 0
        else:
            print("短信发送失败")
            return -1


if __name__ == '__main__':
    CCP().send_message('1',"13693542024", "5678")


