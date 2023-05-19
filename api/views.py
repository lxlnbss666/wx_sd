from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from  rest_framework.exceptions import ValidationError
import re
# Create your views here.

def phone_validators(value):
     if not re.match(r"^(1[3|4|5|6|7|8|9])\d{9}$",value):
          raise ValidationError("手机格式错误")


class MessageSerializer(serializers.Serializer):
     phone = serializers.CharField(label='手机号',validators=[phone_validators,])

class MessageView(APIView):
     def get(self,request,*args,**kwargs):
          """
          发送手机短信验证码
          :param request:
          :param args:
          :param kwargs:
          :return:
          """
          # 1.获取手机号
          # 2.手机式校验
          ser = MessageSerializer(data=request.query_params)
          if not ser.is_valid():
               return Response({'status':False,'message':'手机格式错误'})
          phone = ser.validated_data.get('phone')
          # 3.生成随机验证码
          import random
          random_code = random.randint(1000,9999)
          # 4.验证码发送到手机上，购买服务器进行发送短信: 腾讯云
          # TODO tencent.send_message(phone,random_code)

          """
          1.注册腾讯云，开通腾讯云短信。
          2.创建应用
               SDK AppID = 1400822164
          3.申请签名（个人：小程序）
             ID               名称
             529976       熊猫天天吃麻薯
          4.申请模板
             ID               名称
             1799503      miniprogram 
          5.申请腾讯云API https://console.cloud,tencent,com/cam/capi
               SecretId:
               SecretKey:
          6.调用相关接口去发送短信
               SDK，写好的工具。
          """

          # # -*- coding: utf-8 -*-
          # from tencentcloud.common import credential
          # from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
          # from tencentcloud.sms.v20210111 import sms_client, models
          # from tencentcloud.common.profile.client_profile import ClientProfile
          # from tencentcloud.common.profile.http_profile import HttpProfile
          # try:
          #      cred = credential.Credential("secretId", "secretKey")
          #      client = sms_client.SmsClient(cred, "ap-guangzhou")
          #      req = models.SendSmsRequest()
          #
          #      req.SmsSdkAppId = "1400822164"
          #      # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名
          #      # 签名信息可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-sign) 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-sign) 的签名管理查看
          #      req.SignName = "熊猫天天吃麻薯"
          #      # 模板 ID: 必须填写已审核通过的模板 ID
          #      # 模板 ID 可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-template) 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-template) 的正文模板管理查看
          #      req.TemplateId = "1799503"
          #      # 模板参数: 模板参数的个数需要与 TemplateId 对应模板的变量个数保持一致，，若无模板参数，则设置为空
          #      req.TemplateParamSet = ["1234"]
          #      # 下发手机号码，采用 E.164 标准，+[国家或地区码][手机号]
          #      # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
          #      req.PhoneNumberSet = ["+8617719560056"]
          #      # 用户的 session 内容（无需要可忽略）: 可以携带用户侧 ID 等上下文信息，server 会原样返回
          #
          #      resp = client.SendSms(req)
          #
          #      # 输出json格式的字符串回包
          #      print(resp.to_json_string(indent=2))
          #
          #      # 当出现以下错误码时，快速解决方案参考
          #      # - [FailedOperation.SignatureIncorrectOrUnapproved](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Afailedoperation.signatureincorrectorunapproved-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
          #      # - [FailedOperation.TemplateIncorrectOrUnapproved](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Afailedoperation.templateincorrectorunapproved-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
          #      # - [UnauthorizedOperation.SmsSdkAppIdVerifyFail](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Aunauthorizedoperation.smssdkappidverifyfail-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
          #      # - [UnsupportedOperation.ContainDomesticAndInternationalPhoneNumber](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Aunsupportedoperation.containdomesticandinternationalphonenumber-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
          #      # - 更多错误，可咨询[腾讯云助手](https://tccc.qcloud.com/web/im/index.html#/chat?webAppId=8fa15978f85cb41f7e2ea36920cb3ae1&title=Sms)
          #
          # except TencentCloudSDKException as err:
          #      print(err)
          #
          # # 5.把验证码+手机号，进行保留（30秒）
          # # 5.1 搭建redis服务器 (云redis)
          # # 5.2 django 中方便使用redis的模块 django-redis
          #
          # from django_redis import get_redis_connection
          # conn = get_redis_connection()
          # conn.set(phone,random_code,ex=30)
          #
          #
          return Response({"status":True,'message':'验证码发送成功'})

class LoginView(APIView):
     def post(self,request,*args,**kwargs):
          print(request.data)
          return Response({"status":True})

