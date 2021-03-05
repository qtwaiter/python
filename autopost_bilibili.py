import requests
import time
import random
url = 'https://api.live.bilibili.com/msg/send'

cookie = {'cookie':"_uuid=1F8A9C97-7351-E02F-72EC-DFBBE4E3957802012infoc; buvid3=1942D322-C7C7-4DF8-99C9-130E99F28850184979infoc; fingerprint=79f1a85241e08121999d03569eeb34ce; buvid_fp=1942D322-C7C7-4DF8-99C9-130E99F28850184979infoc; buvid_fp_plain=1942D322-C7C7-4DF8-99C9-130E99F28850184979infoc; SESSDATA=85c08bc1%2C1629890419%2C7273b%2A21; bili_jct=dccb2dd9633a08e567e8e392cc50e85e; DedeUserID=133134578; DedeUserID__ckMd5=01577e5d85e09ee5; sid=4suskagf; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u|u)~ukmlY0J'uYuRJJ)l|~; fingerprint3=9c43340b14e5745ed73fa700a7831772; fingerprint_s=aef9c33fa46d613685254cd98449d4aa; bp_video_offset_133134578=497927868011799264; bp_t_offset_133134578=497933576019183169; _dfcaptcha=f27f9b94ee81abd8dcab4c0ff526531d; LIVE_BUVID=AUTO4116149471169698; PVID=5"}
def message(msg):
    data = {
        'color': '16777215',
        'fontsize': '25',
        'mode': '1',
        'msg': msg,
        'rnd': '1614949268',
        'roomid': '22764593',
        'bubble': '0',
        'csrf_token': 'dccb2dd9633a08e567e8e392cc50e85e',
        'csrf': 'dccb2dd9633a08e567e8e392cc50e85e'
    }
    return data
# 建立列表，列表中是弹幕发送的内容
list_str = ['666','888','你好美','你说话好好听','给你点赞！！！','今晚一起学习','B站你最棒']

for str in list_str:
    new_data = message(str)
    range_second = random.randint(1,6)  # 产生随机整数
# 2.请求 (request) get拿数据 post 提交请求体 文本 text 视频，音频，图片 content
    result = requests.post(url, cookies=cookie, data=new_data).text
    print(result)
    print(range_second)
    time.sleep(range_second)  # 等待时间
