from enum import Enum

class SmsCode(Enum):
    sendSucc    = "00"  #发送成功
    parmErr     = "01"  #参数错误
    sysErr      = "02"  #系统错误
    phoneErr    = "03"  #非法手机号
    phoneExist  = "04"  #已注册
    rptReq      = "05"  #重复请求

class RegCode(Enum):
    regSucc    = "00"  #发送成功
    parmErr     = "01"  #参数错误
    sysErr      = "02"  #系统错误
    phoneErr    = "03"  #非法手机号
    phoneExist  = "04"  #已注册
    chkErr      = "05"  #验证码不正确

