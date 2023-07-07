import sqlite3
import os
data_path = './data/CFHelper/'
if not os.path.exists(data_path):
    os.makedirs(data_path)
conn = sqlite3.connect('./data/CFHelper/reminder.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS QQUser (
        QQ INTEGER PRIMARY KEY,
        status INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS QQGroup (
        QQGroup INTEGER PRIMARY KEY,
        status INTEGER
    )
''')

async def onUser(QQ):
    global cursor,conn
    try:
        cursor.execute('''
        INSERT OR REPLACE INTO QQUser (QQ,status)
        VALUES (?, ?)
    ''', (
        QQ,
        1
    ))
        conn.commit()
        return True
    except:
        return False
        
        

async def onGroup(QQGroup):
    global cursor,conn
    try:
        cursor.execute('''
        INSERT OR REPLACE INTO QQGroup (QQGroup,status)
        VALUES (?, ?)
    ''', (
        QQGroup,
        1
    ))
        conn.commit()
        return True
    except:
        return False

async def disUser(QQ):
    global cursor,conn
    try:
        cursor.execute('''
        INSERT OR REPLACE INTO QQUser (QQ,status)
        VALUES (?, ?)
    ''', (
        QQ,
        0
    ))
        conn.commit()
        return True
    except:
        return False


async def disGroup(QQGroup):
    global cursor,conn
    try:
        cursor.execute('''
        INSERT OR REPLACE INTO QQGroup (QQGroup,status)
        VALUES (?, ?)
    ''', (
        QQGroup,
        0
    ))
        conn.commit()
        return True
    except:
        return False
    
async def returnReminderUserList():
    ReminderUserList=[]
    global cursor,conn
    cursor.execute('SELECT * FROM QQUser')
    RS= cursor.fetchall()
    if len(RS) == 0:
        return ReminderUserList
    for row in RS:
        QQ,status = row
        if(status==1):
            ReminderUserList.append({'QQ':QQ})
    return ReminderUserList

async def returnReminderGroupList():
    ReminderGroupList=[]
    global cursor,conn
    cursor.execute('SELECT * FROM QQGroup')
    RS= cursor.fetchall()
    if len(RS) == 0:
        return ReminderGroupList
    for row in RS:
        QQGroup,status = row
        if(status==1):
            ReminderGroupList.append({'QQGroup':QQGroup})
    return ReminderGroupList
