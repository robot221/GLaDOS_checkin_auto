import requests,json,os
# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
# pushplus秘钥 申请地址 http://www.pushplus.plus
    sckey = os.environ.get("PUSHPLUS_TOKEN", "")
# 推送内容
    sendContent = ''
# glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("GLADOS_COOKIE", []).split("&")
    if cookies[0] == "":
        print('未获取到COOKIE变量') 
        cookies = []
        exit(0)
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    url3= "https://glados.cloud/api/user/points" #points
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload={
        'token': 'glados.one'
    }
    for cookie in cookies:
        checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
        points = requests.get(url3,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    #--------------------------------------------------------------------------------------------------------#  
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        curpoints = points.json()['points'].split('.')[0]
        email = state.json()['data']['email']
        if 'message' in checkin.text:
            mess = checkin.json()['message']
            print(email+'----结果--'+mess+'----剩余('+time+')天----当前points: '+curpoints)  # 日志输出
            sendContent += email+'----'+mess+'----剩余('+time+')天----当前points: '+curpoints+'\n'
        else:
            requests.get('http://www.pushplus.plus/send?token=' + sckey + '&content='+email+'cookie已失效')
            print('cookie已失效')  # 日志输出
     #--------------------------------------------------------------------------------------------------------#   
    if sckey != "":
         requests.get('http://www.pushplus.plus/send?token=' + sckey + '&title='+email+'签到成功'+'&content='+sendContent)

    # --- 新增 Telegram 推送逻辑 ---
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    tg_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    print(f"tg_token:{tg_token},tg_chat_id:{tg_chat_id}")
    if tg_token != "" and tg_chat_id != "":
        print('gogogo')
        tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
        tg_payload = {
            "chat_id": tg_chat_id,
            "text": f"GLaDOS 签到结果:\n{sendContent}"
        }
        try:
            requests.post(tg_url, data=tg_payload)
        except Exception as e:
            print(f"Telegram 推送失败: {e}")
    # ------------------------------

