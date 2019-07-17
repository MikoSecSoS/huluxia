# -*- coding: utf-8 -*-

import time
import configparser

import requests

# from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor

nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def spider(url, user_id):
	url = url + "&user_id={user_id}".format(user_id=user_id)
	userNotFound = '{"msg":"用户不存在","code":104,"title":null,"status":0}'
	header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
	req = requests.get(url, headers=header)
	if req.status_code != 200 or req.text == userNotFound:
		print("ID为{user_id}的用户不存在...".format(user_id))
		return
	result = req.text
	data = formatData(result)
	download("UserData_" + nowTime +".txt", data)
	print("已写入", data)
	download("SourceUserData_" + nowTime +".txt", result)

def formatData(data):
	userID = data.get("userID")
	avatar = data.get("avatar")
	location = data.get("location")
	try:
		lastLoginTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get("lastLoginTime"[:-3])))
	except:
		lastLoginTime = "null"
	nick = data.get("nick")
	level = "LV" +data.get("level")
	gender = "♀女" if int(data.get("gender")) == 1 else "♂男"
	age =  data.get("age")
	identityTitle = data.get("identityTitle")
	integral = data.get("integral")
	integralNick = data.get("integralNick")
	credits = data.get("credits")
	postCount	= data.get("postCount")
	commentCount = Countdata.get("commentCount")
	followingCountFormated = data.get("followingCountFormated")
	followerCountFormated = data.get("favoriteCount")
	medalList = data.get("medalList")
	photos = [i.get(url) for i in data.get("photos")]
	signature = data.get("signature")
	hometown = [i.get("hometown_province") + " - "+  i.get("hometown_city") for i in data.get("hometown")]
	workinfo = [i.get("work_industry_detail") + " - "+ i.get("work_company")for i in data.get("workinfo")]
	schoolInfo = [i.get("school_name") + " - " + i.get("school_name") + "级" for i in data.get("schoolInfo")]
	info = {
		"签名": signature,
		"家乡": hometown,
		"职业": workinfo,
		"学校": schoolInfo,
	}
	beenLocations = data.get("beenLocations")
	tags = [i.get("title") for i in data.get("tags")]

	return {
		"用户ID": userID,
		"头像": avatar,
		"昵称": nick,
		"昵称": location,
		"昵称": nick,
		"等级": level,
		"性别": gender,
		"年龄": age,
		"头衔": identityTitle,
		"贡献值": identity,
		"贡献称号": followingCountFormated,
		"葫芦": credits,
		"帖子": postCount,
		"回复": comment,
		"关注": followingCountFormated,
		"粉丝": followerCountFormated,
		"收藏": favoriteCount,
		"勋章": str(medalList).replace("name", "勋章名称").replace("url", "勋章图片"),
		"照片": photos,
		"个人信息": info,
		"去过的地方": beenLocations,
		"标签": favoriteCount
	}

def download(filename, datas):
	filename = filename.replace("/", "_").replace("\\", "_")
	with open(filename, "a+") as f:
		f.write(str(data) + "\n")

def main():
	config = configparser.ConfigParser()
	config.read("config.ini")
	key = config.get("config", "key")
	startId = config.get("config", "startId")
	endId = config.get("config", "endId")
	thread = config.get("config", "thread")
	url = "http://floor.huluxia.com/user/info/ANDROID/2.1?_key={key}".format(key=key)
	# pool = Pool(int(thread))
	# pool.map(spider, [i for i in range(int(startId), int(endId)+1)])
	with ThreadPoolExecutor(int(thread)) as p:
		[p.submit(main, i) for i in range(int(startId), int(endId)+1)]

if __name__ == '__main__':
	main()