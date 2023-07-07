import requests
import json
import datetime
import sqlite3
user_info_baseurl="https://codeforces.com/api/user.info?handles="
import os
data_path = './data/CFHelper/'
if not os.path.exists(data_path):
    os.makedirs(data_path)
conn = sqlite3.connect('./data/CFHelper/data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id TEXT PRIMARY KEY,
        now_rating INTEGER,
        update_time INTEGER,
        QQ INTEGER,
        status INTEGER,
        last_rating INTEGER
    )
''')

class UserType:
    def __init__(self, id, now_rating, update_time,QQ,status,last_rating):
        self.id = id
        self.now_rating= now_rating if now_rating is not None else 0
        self.update_time=update_time if update_time is not None else 0
        self.QQ=QQ if QQ is not None else 0
        self.status=status if status is not None else 1
        self.last_rating=last_rating if last_rating is not None else 0


async def addUser(id,QQ):
    global user_info_baseurl,cursor,conn
    user_info_url=user_info_baseurl+id

    try:
        response = requests.get(user_info_url)
        response.raise_for_status()  # 检查响应是否成功，如果不成功会抛出异常
        data = json.loads(response.text)
    except requests.RequestException as e:
        print("请求错误:", e)
        return False 
    except json.JSONDecodeError as e:
        print("JSON解析错误:", e)
        return False
        # 处理JSON解析异常的情况
    except Exception as e:
        print("发生了其他错误:", e)
        return False
        # 处理其他未预料到的异常情况

    # 检查API响应状态
    if data["status"] == "OK":
        # 获取result列表
        results = data["result"]
        
        # 遍历每个结果并储存键值
        for result in results:
            update_time=int(datetime.datetime.now().timestamp())
            user=UserType(id,result["rating"],update_time,QQ,1,result["rating"])
            cursor.execute('''
            INSERT OR REPLACE INTO User (id, now_rating, update_time,QQ,status,last_rating)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user.id,
            user.now_rating,
            user.update_time,
            user.QQ,
            user.status,
            user.last_rating
        ))
            conn.commit()
            return True
    else:
        print("添加用户请求失败")
        return False


async def updateUser():
    Users=[]
    global user_info_baseurl,cursor,conn

    cursor.execute('SELECT * FROM User')
    RS= cursor.fetchall()
    if len(RS) == 0:
        return Users
    for row in RS:
        Oid, Onow_rating, Oupdate_time, OQQ, Ostatus ,Olast_rating = row
        user_info_url=user_info_baseurl+Oid

        try:
            response = requests.get(user_info_url)
            response.raise_for_status()  # 检查响应是否成功，如果不成功会抛出异常
            data = json.loads(response.text)
        except requests.RequestException as e:
            print("请求错误:", e)
            return Users
        except json.JSONDecodeError as e:
            print("JSON解析错误:", e)
            return Users
            # 处理JSON解析异常的情况
        except Exception as e:
            print("发生了其他错误:", e)
            return Users
            # 处理其他未预料到的异常情况

        # 检查API响应状态
        if data["status"] == "OK":
            # 获取result列表
            results = data["result"]
            
            # 遍历每个结果并储存键值
            for result in results:
                update_time=int(datetime.datetime.now().timestamp())
                user=UserType(Oid,result["rating"],update_time,OQQ,Ostatus,Onow_rating)
                Users.append(user)

                cursor.execute('''
                INSERT OR REPLACE INTO User (id, now_rating, update_time,QQ,status,last_rating)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user.id,
                user.now_rating,
                user.update_time,
                user.QQ,
                user.status,
                user.last_rating
            ))
                conn.commit()
        else:
            print("数据请求失败")

    return Users

async def returRatingChangeInfo():
    outputlist=[]
    Users=await updateUser()
    if not Users:
        return outputlist

    global cursor,conn
    for user in Users:
        output=f"当前时间：{datetime.datetime.now()}\n"
        cursor.execute('SELECT now_rating,last_rating,QQ FROM User WHERE id = ?', (user.id,))
        row = cursor.fetchone()
        now_rating,last_rating,QQ = row
        if last_rating!=now_rating:
            change=now_rating-last_rating
            output+=f"检测到您的CF账号 {user.id} 分数发生变化，从{last_rating} → {now_rating}  变动了{change}分！\n"
            outputlist.append({'QQ':QQ,'output':output})

    return outputlist
