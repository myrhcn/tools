from email.mime import application

import requests, re, time, json, schedule

flag = ""


def getNews():
    try:
        reslist = []
        api = "https://api.github.com/search/repositories?q=CVE-2021&sort=updated"
        req = requests.get(api).text
        cve_total_count = re.findall('"total_count":*.{1,10}"incomplete_results"', req)[0][14:17]
        cve_description = re.findall('"description":*.{1,200}"fork"', req)[0].replace("\",\"fork\"", '').replace(
            "\"description\":\"", '')
        cve_url = re.findall('"svn_url":*.{1,200}"homepage"', req)[0].replace("\",\"homepage\"", '').replace(
            "\"svn_url\":\"", '')
        reslist.append(cve_total_count)
        reslist.append(cve_description)
        reslist.append(cve_url)

        return reslist
    except Exception as e:
        print(e, "github链接不通")


def sendNews():
    try:
        # msg1 = str(getNews()) #获取getNews()内容
        global flag
        api = "https://api.github.com/search/repositories?q=CVE-2021&sort=updated"
        req = requests.get(api).text
        total_count = re.findall('"total_count":*.{1,10}"incomplete_results"', req)[0][14:17]

        # time.sleep(60)
        msg = getNews()
        res_msg = ""
        for i in msg:
            res_msg += " " + str(i)

        if flag != total_count:
            if total_count == msg[0]:
                api = 'https://oapi.dingtalk.com/robot/send?access_token=8b1d72a7080011bbfbcc5a4d92d13e2af426c75a5fe6a3641d57f39d9ce3cf1c'
                headers = {
                    'User-Agnet': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)',
                    'Content-Type': 'application/json;charset=utf-8'
                }

                json_text = {
                    "msgtype": "text",
                    "at": {
                        "atMobiles": [
                            "11111"
                        ],
                        "isAtAll": False
                    },
                    "text": {
                        "content": "呱呱" + res_msg
                    }
                }
                response = requests.post(url=api, data=json.dumps(json_text), headers=headers)
                res = json.loads(response.text)
                try:
                    if res['errmsg'] == 'ok' or res['errcode'] == 0:
                        flag = total_count
                        return '发送成功'
                    else:
                        return '发送失败'
                except Exception:
                    return '异常错误'
            else:
                pass
    except Exception as e:
        print(e, "呱呱,出错了！")
        raise e


# 任务
def job():
    sendNews()


# 定时任务计划
# 每一个小时运行一次
# schedule.every(30).minutes.do(job)
schedule.every(30).minutes.do(job)

if __name__ == '__main__':
    # 定时任务循环
    while True:
        schedule.run_pending()
        time.sleep(1)
