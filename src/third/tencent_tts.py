import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tts.v20190823 import tts_client, models
import os

print("tencent api initializing...")
global clientProfile, cred
# 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
# 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
# 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
# 实例化一个http选项，可选的，没有特殊需求可以跳过
httpProfile = HttpProfile()
httpProfile.endpoint = "tts.tencentcloudapi.com"

# 实例化一个client选项，可选的，没有特殊需求可以跳过
clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
ak = os.getenv("TENCENT_API_KEY")
sk = os.getenv("TENCENT_SECRET_KEY")
cred = credential.Credential(ak, sk)


def tts(text):
    try:
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.TextToVoiceRequest()
        # req = models.CreateTtsTaskRequest()
        params = {
            "Text": text,
            "SessionId": "123",
            "VoiceType": 101006
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个TextToVoiceResponse的实例，与请求对象对应
        resp = tts_client.TtsClient(cred, "ap-shanghai", clientProfile).TextToVoice(req)
        # 输出json格式的字符串回包
        return resp.Audio

    except TencentCloudSDKException as err:
        print(err)
        return None
