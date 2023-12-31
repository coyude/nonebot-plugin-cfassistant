import aiohttp
import json
import datetime
import aiosqlite
import asyncio 
import os
db_lock = asyncio.Lock()
contest_url = "https://codeforces.com/api/contest.list?gym=false"
data_path = './data/CFHelper/'
if not os.path.exists(data_path):
    os.makedirs(data_path)
db_path = os.path.join(data_path, 'data.db')
# conn = sqlite3.connect('./data/CFHelper/data.db')
# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Contest (
#         id INTEGER PRIMARY KEY,
#         name TEXT,
#         type TEXT,
#         phase TEXT,
#         duration INTEGER,
#         startTime INTEGER,
#         relativeTime INTEGER,
#         durationShow TEXT,
#         startTimeShow TEXT,
#         relativeTimeShow TEXT,
#         remindStatus INTEGER
#     )
# ''')

async def create_data():
    async with aiosqlite.connect(db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS Contest (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    type TEXT,
                    phase TEXT,
                    duration INTEGER,
                    startTime INTEGER,
                    relativeTime INTEGER,
                    durationShow TEXT,
                    startTimeShow TEXT,
                    relativeTimeShow TEXT,
                    remindStatus INTEGER
                )
            ''')
            await conn.commit()

asyncio.run(create_data())

class ContestType:
    def __init__(self, id, name, type, phase, duration, startTime, relativeTime,durationShow,startTimeShow,relativeTimeShow):
        self.id = id
        self.name = name
        self.type = type
        self.phase = phase
        self.duration = duration
        self.startTime = startTime
        self.relativeTime = relativeTime
        self.durationShow=durationShow
        self.startTimeShow=startTimeShow
        self.relativeTimeShow=relativeTimeShow
        self.remindStatus=0


async def updateContest():
    Contests=[]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(contest_url) as response:
                response.raise_for_status()  # 检查响应是否成功，如果不成功会抛出异常
                data = await response.json()
    except aiohttp.ClientError as e:
        print("请求错误:", e)
        return Contests
    except json.JSONDecodeError as e:
        print("JSON解析错误:", e)
        return Contests
    except Exception as e:
        print("发生了其他错误:", e)
        return Contests

    # 检查API响应状态
    if data["status"] == "OK":
        # 获取result列表
        results = data["result"]
        # 遍历每个结果并储存键值
        for result in results:
            if(result["phase"]!="BEFORE"):
                break;
            
            contest_duration_raw = result["durationSeconds"]
            contest_start_time_raw = result["startTimeSeconds"]
            contest_relative_time_raw = abs(result["relativeTimeSeconds"])

            du_hous=contest_duration_raw//3600
            du_minutes=(contest_duration_raw%3600)//60
            
            re_days = contest_relative_time_raw // (24 * 60 * 60)
            re_hours = (contest_relative_time_raw % (24 * 60 * 60)) // (60 * 60)
            re_minutes = (contest_relative_time_raw % (60 * 60)) // 60

            contest_duration=f"{du_hous}小时{du_minutes}分钟"
            contest_start_time = (datetime.datetime.fromtimestamp(result["startTimeSeconds"])).strftime("%Y-%m-%d %H:%M:%S")
            contest_relative_time=""

            if re_days==0:
                contest_relative_time=f"{re_hours}小时{re_minutes}分钟"
            else:
                contest_relative_time=f"{re_days}天{re_hours}小时{re_minutes}分钟"
            
            contest=ContestType(result["id"],result["name"],result["type"],result["phase"],result["durationSeconds"],result["startTimeSeconds"],abs(result["relativeTimeSeconds"]),contest_duration,contest_start_time,contest_relative_time)
            Contests.append(contest)

            async with db_lock, aiosqlite.connect(db_path) as conn:
                cursor = await conn.cursor()
                await cursor.execute('SELECT remindStatus FROM Contest WHERE id = ?', (contest.id,))
                remind_status=0

                status = await cursor.fetchone()
                if status is not None:
                    remind_status = status[0]

                await cursor.execute('''
                INSERT OR REPLACE INTO Contest (id, name, type, phase, duration, startTime, relativeTime, durationShow, startTimeShow, relativeTimeShow, remindStatus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                contest.id,
                contest.name,
                contest.type,
                contest.phase,
                contest.duration,
                contest.startTime,
                contest.relativeTime,
                contest.durationShow,
                contest.startTimeShow,
                contest.relativeTimeShow,
                remind_status
            ))
                await conn.commit()
    else:
        print("数据请求失败")

    return Contests

async def returnreminderInfo():
    Contests=await updateContest()
    output=""
    async with db_lock, aiosqlite.connect(db_path) as conn:
        remind_status=3
        cursor = await conn.cursor()
        for contest in Contests:
            await cursor.execute('SELECT remindStatus FROM Contest WHERE id = ?', (contest.id,))
            ids = await cursor.fetchone()
            if ids is not None:
                remind_status = ids[0]
            
            current_time_raw = datetime.datetime.now()
            current_time = int(current_time_raw.timestamp())
            if contest.startTime+contest.duration<=current_time:
                await cursor.execute('''
                    UPDATE Contest
                    SET phase = ?
                    WHERE id = ?
                ''', ("FINISHED", contest.id))
                await conn.commit() 
                await cursor.execute('SELECT remindStatus FROM Contest WHERE id = ?', (contest.id,))
                ids = await cursor.fetchone()
                if ids is not None:
                    remind_status = ids[0]
            
            if contest.relativeTime<=3*3600 and remind_status<3:
                output+=f"3小时内将有以下比赛：\n" \
                f"比赛ID：{contest.id}\n" \
                f"比赛名称：{contest.name}\n" \
                f"比赛开始时间：{contest.startTimeShow}\n" \
                f"比赛时长：{contest.durationShow}\n" \
                f"距离比赛开始时间：{contest.relativeTimeShow}\n\n"
                await cursor.execute('''
                    UPDATE Contest
                    SET remindStatus = ?
                    WHERE id = ?
                ''', (3, contest.id))
                await conn.commit()     
                await cursor.execute('SELECT remindStatus FROM Contest WHERE id = ?', (contest.id,))
                ids = await cursor.fetchone()
                if ids is not None:
                    remind_status = ids[0]

            if contest.relativeTime<=11*3600 and remind_status<2:
                output+=f"11小时内将有以下比赛：\n" \
                f"比赛ID：{contest.id}\n" \
                f"比赛名称：{contest.name}\n" \
                f"比赛开始时间：{contest.startTimeShow}\n" \
                f"比赛时长：{contest.durationShow}\n" \
                f"距离比赛开始时间：{contest.relativeTimeShow}\n\n"
                await cursor.execute('''
                    UPDATE Contest
                    SET remindStatus = ?
                    WHERE id = ?
                ''', (2, contest.id))
                await conn.commit()       
                await cursor.execute('SELECT remindStatus FROM Contest WHERE id = ?', (contest.id,))
                ids = await cursor.fetchone()
                if ids is not None:
                    remind_status = ids[0]

            if contest.relativeTime<=48*3600 and remind_status<1:
                output+=f"48小时内将有以下比赛：\n" \
                f"比赛ID：{contest.id}\n" \
                f"比赛名称：{contest.name}\n" \
                f"比赛开始时间：{contest.startTimeShow}\n" \
                f"比赛时长：{contest.durationShow}\n" \
                f"距离比赛开始时间：{contest.relativeTimeShow}\n\n"
                await cursor.execute('''
                    UPDATE Contest
                    SET remindStatus = ?
                    WHERE id = ?
                ''', (1, contest.id))
                await conn.commit()
                await cursor.execute('SELECT remindStatus FROM Contest WHERE id = ?', (contest.id,))
                ids = await cursor.fetchone()
                if ids is not None:
                    remind_status = ids[0]

        if(output!=""):
            print(output)

    return output

async def returnContestInfo():
    Contests=await updateContest()
    output=f"当前时间：{datetime.datetime.now()}\n\n"
    for contest in Contests:
        output+=f"比赛ID：{contest.id}\n" \
                f"比赛名称：{contest.name}\n" \
                f"比赛开始时间：{contest.startTimeShow}\n" \
                f"比赛时长：{contest.durationShow}\n" \
                f"距离比赛开始时间：{contest.relativeTimeShow}\n\n"
    return output

# def markdata():
#     current_time_raw = datetime.datetime.now()
#     current_time = int(current_time_raw.timestamp())
#     cursor.execute('SELECT * FROM Contest')
#     RS= cursor.fetchall()
#     for row in RS:
#         id, name, type, phase, duration, startTime, relativeTime, durationShow, startTimeShow, relativeTimeShow, remindStatus = row
#         if startTime+duration<=current_time:
#             cursor.execute('''
#                 UPDATE Contest
#                 SET phase = ?
#                 WHERE id = ?
#             ''', ("FINISHED", id))
#             conn.commit() 
