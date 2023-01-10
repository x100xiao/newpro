# code:utf-8
import requests
import json
import os



singer = input('请输入歌曲或歌手名称:')
num = input('请输入页数（一页10首歌曲）:')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63",
    "Cookie": "_ga=GA1.2.1083049585.1590317697; _gid=GA1.2.2053211683.1598526974; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1597491567,1598094297,1598096480,1598526974; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1598526974; kw_token=HYZQI4KPK3P",
    "Referer": "http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6",
    "csrf": "HYZQI4KPK3P",
}
params = {
    "key": singer,
    "pn": num,
    "rn": "10",
    "httpsStatus": "1",
    "reqId": "cc337fa0-e856-11ea-8e2d-ab61b365fb50",
}
music_list = []
music_url = []


#访问音乐列表
url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
res = requests.get(url=url, headers=headers, params=params)
if res.status_code == 200:
    res.encoding = "utf-8"
    text = res.text
    json_list = json.loads(text)
    datapack = json_list["data"]["list"]
    for i in datapack:
        #获取列表中音乐的下载地址
        music_name = i["name"]
        music_singer = i["artist"]
        rid = i["rid"]
        api_music = "https://antiserver.kuwo.cn/anti.s?type=convert_url&rid={}&format=mp3&response=url".format(rid)
        api_res = requests.get(url=api_music)
        music_url = api_res.text
        print(music_name + "  " + music_singer + "   " + music_url)
        music_dict = {}
        music_dict["name"] = music_name
        music_dict["singer"] = music_singer

        #下载音乐到本地
        root = './歌曲文件/'
        if not os.path.exists(root):
            os.mkdir(root)
        music_content = requests.get(url=music_url).content
        with open(root + "{}({}).mp3".format(music_name, music_singer), "wb") as f:
            f.write(music_content)