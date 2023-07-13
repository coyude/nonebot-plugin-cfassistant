import aiosqlite
import asyncio 
import os
data_path = './data/CFHelper/'
if not os.path.exists(data_path):
    os.makedirs(data_path)
db_path = os.path.join(data_path, 'reminder.db')
db_lock = asyncio.Lock()
# conn = sqlite3.connect('./data/CFHelper/reminder.db')
# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS QQUser (
#         QQ INTEGER PRIMARY KEY,
#         status INTEGER
#     )
# ''')
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS QQGroup (
#         QQGroup INTEGER PRIMARY KEY,
#         status INTEGER
#     )
# ''')

async def create_reminder():
    async with aiosqlite.connect(db_path) as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS QQUser (
                QQ INTEGER PRIMARY KEY,
                status INTEGER
            )
        ''')
        await conn.commit()
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS QQGroup (
                QQGroup INTEGER PRIMARY KEY,
                status INTEGER
            )
        ''')
        await conn.commit()

asyncio.run(create_reminder())

async def onUser(QQ):
    try:
        async with db_lock, aiosqlite.connect(db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute('''
            INSERT OR REPLACE INTO QQUser (QQ,status)
            VALUES (?, ?)
        ''', (
            QQ,
            1
        )) 
            await conn.commit()
        return True
    except:
        return False
        
        

async def onGroup(QQGroup):
    try:
        async with db_lock, aiosqlite.connect(db_path) as conn:
            cursor = await conn.cursor()        
            await cursor.execute('''
            INSERT OR REPLACE INTO QQGroup (QQGroup,status)
            VALUES (?, ?)
        ''', (
            QQGroup,
            1
        ))
            await conn.commit()
        return True
    except:
        return False

async def disUser(QQ):
    try:
        async with db_lock, aiosqlite.connect(db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute('''
            INSERT OR REPLACE INTO QQUser (QQ,status)
            VALUES (?, ?)
        ''', (
            QQ,
            0
        ))
            await conn.commit()
        return True
    except:
        return False


async def disGroup(QQGroup):
    try:
        async with db_lock, aiosqlite.connect(db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute('''
            INSERT OR REPLACE INTO QQGroup (QQGroup,status)
            VALUES (?, ?)
        ''', (
            QQGroup,
            0
        ))
            await conn.commit()
        return True
    except:
        return False
    
async def returnReminderUserList():
    ReminderUserList=[]
    async with db_lock, aiosqlite.connect(db_path) as conn:
        cursor = await conn.cursor()
        await cursor.execute('SELECT * FROM QQUser')
        RS= await cursor.fetchall()
        if not RS:
            return ReminderUserList
        for row in RS:
            QQ,status = row
            if(status==1):
                ReminderUserList.append({'QQ':QQ})
    return ReminderUserList

async def returnReminderGroupList():
    ReminderGroupList=[]
    async with db_lock, aiosqlite.connect(db_path) as conn:
        cursor = await conn.cursor()
        await cursor.execute('SELECT * FROM QQGroup')
        RS= await cursor.fetchall()
        if not RS:
            return ReminderGroupList
        for row in RS:
            QQGroup,status = row
            if(status==1):
                ReminderGroupList.append({'QQGroup':QQGroup})
    return ReminderGroupList
