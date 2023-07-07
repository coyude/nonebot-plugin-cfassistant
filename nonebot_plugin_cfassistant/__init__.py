from nonebot import on_command, require, get_bots
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from .updateContest import *
from .updateUser import *
from .changeRemind import *
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent,GroupMessageEvent
import asyncio
import os

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-cfassistant",
    description="一个支持CF(codeforces)平台查询比赛/比赛提醒/监测分数变化的nonebot机器人插件",
    usage="/cfhelp查看插件帮助\n",
    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。
    homepage="https://github.com/coyude/nonebot-plugin-cfassistant",
    # 发布必填。
    supported_adapters={"~onebot.v11"}
)



data_path = './data/CFHelper/'
if not os.path.exists(data_path):
    os.makedirs(data_path)

timing = require("nonebot_plugin_apscheduler").scheduler
getCF = on_command("CF", rule=to_me(), aliases={"查CF","查cf","cf"}, priority=10, block=True)
PluginHelp=on_command("CFHELP", rule=to_me(), aliases={"cfhelp"}, priority=10, block=True)
bind= on_command("绑定", rule=to_me(), aliases={"订阅","用户"}, priority=10, block=True)
onGroupRemind = on_command("群提醒", rule=to_me(), priority=10, block=True)
disGroupdRemind = on_command("取消群提醒", rule=to_me(), priority=10, block=True)
onPrivateRemind = on_command("提醒", rule=to_me(), priority=10, block=True)
disPrivateRemind = on_command("取消提醒", rule=to_me(), priority=10, block=True)


@getCF.handle()
async def getCF_fun():
    tasks_list = [
        asyncio.create_task(returnContestInfo())
    ]
    status = await asyncio.gather(*tasks_list)
    if status:
        await getCF.finish(status[0])
    else:
        await getCF.finish("获取失败！")


@PluginHelp.handle()
async def PluginHelp_fun():
    await PluginHelp.finish("""nonebot-plugin-CFReminder 使用方法👇\n        
1.输入:/CF 或 /cf 或 /查CF 或 /查cf 即可进行查询近期比赛\n
2.在好友私聊下输入:/绑定 你的CF个人ID 即可对该账户分数进行监测(一个ID只能绑定一个QQ号)\n
3.在群聊下输入:/群提醒 即可对本群开启比赛提醒功能(分别在48小时，11小时，3小时提醒一次)\n
4.在群聊下输入:/取消群提醒 即可关闭本群的比赛提醒功能\n
5.在好友私聊下输入:/提醒 即可开启比赛提醒功能(分别在48小时，11小时，3小时提醒一次)\n
6.在好友私聊下输入:/取消提醒 即可关闭比赛提醒功能\n
如有问题或建议，请在 https://github.com/coyude/nonebot-plugin-cfreminder 上反馈，感谢🤗""")

@bind.handle()
async def bind_fun(bot: Bot, event: PrivateMessageEvent,args: Message = CommandArg()):
    if id := args.extract_plain_text():
        tasks_list = [
            asyncio.create_task(addUser(str(id),int(event.get_user_id())))
        ]
        status = (await asyncio.gather(*tasks_list))[0]
        if status:
            await bot.send_private_msg(user_id=event.user_id, message=f'绑定用户{str(id)}成功！')
        else:
            await bot.send_private_msg(user_id=event.user_id, message=f'绑定用户{str(id)}失败！请检查该用户是否有效或格式正确！')
    else:
        await bind.finish("绑定失败，请按照此格式：/绑定 jiangly")



@onGroupRemind.handle()
async def onGroupRemind_fun(bot: Bot, event: GroupMessageEvent):
    tasks_list = [
        asyncio.create_task(onGroup(int(event.group_id)))
    ]
    status = (await asyncio.gather(*tasks_list))[0]
    if status:
        await bot.send_group_msg(group_id=event.group_id, message=f'本群订阅提醒成功！')
    else:
        await bot.send_group_msg(group_id=event.group_id, message=f'本群订阅提醒失败！')

@disGroupdRemind.handle()
async def disGroupdRemind_fun(bot: Bot, event: GroupMessageEvent):
    tasks_list = [
        asyncio.create_task(disGroup(int(event.group_id)))
    ]
    status = (await asyncio.gather(*tasks_list))[0]
    if status:
        await bot.send_group_msg(group_id=event.group_id, message=f'本群取消订阅提醒成功！')
    else:
        await bot.send_group_msg(group_id=event.group_id, message=f'本群取消订阅提醒失败！')

@onPrivateRemind.handle()
async def onPrivateRemind_fun(bot: Bot, event: PrivateMessageEvent):
    tasks_list = [
        asyncio.create_task(onUser(int(event.get_user_id())))
    ]
    status = (await asyncio.gather(*tasks_list))[0]
    if status:
        await bot.send_private_msg(user_id=event.user_id, message=f'订阅提醒成功！')
    else:
        await bot.send_private_msg(user_id=event.user_id, message=f'订阅提醒失败！')

@disPrivateRemind.handle()
async def disPrivateRemind_fun(bot: Bot, event: PrivateMessageEvent):
    tasks_list = [
        asyncio.create_task(disUser(int(event.get_user_id())))
    ]
    status = (await asyncio.gather(*tasks_list))[0]
    if status:
        await bot.send_private_msg(user_id=event.user_id, message=f'取消订阅提醒成功！')
    else:
        await bot.send_private_msg(user_id=event.user_id, message=f'取消订阅提醒失败！')


@timing.scheduled_job("cron", second="1", id="ratingReminder")
async def ratingReminder():
    (selfbot,) = get_bots().values()
    messlist=await returRatingChangeInfo()
    for mess in messlist:
        print(mess['QQ'])
        print(mess['output'])
        await selfbot.send_private_msg(user_id=mess['QQ'], message=mess['output'])
        await asyncio.sleep(5)

@timing.scheduled_job("cron", second="31", id="contestReminder")
async def contestReminder():
    (selfbot,) = get_bots().values()
    output=await returnreminderInfo()
    if output!="":
        private=await returnReminderUserList()
        group=await returnReminderGroupList()
        for p in private:
            print('发送给订阅者：'+str(p['QQ']))
            await selfbot.send_private_msg(user_id=p['QQ'], message=output)
            await asyncio.sleep(5)
        for g in group:
            print('发送给QQ群：'+str(g['QQGroup']))
            await selfbot.send_group_msg(group_id=g['QQGroup'], message=output)
            await asyncio.sleep(5)
