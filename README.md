<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-cfassistant

_✨ NoneBot 插件简单描述 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-example.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-example">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-example.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

  
一个支持CF(codeforces)平台查询比赛/比赛提醒/监测分数变化的nonebot机器人插件  
插件启动后，将会在nonebot机器人项目创建 `data/CFHelper/`，并存放`data.db`(储存比赛和绑定用户)和`reminder.db`(储存订阅比赛提醒的用户和群聊)

## 📖 介绍

本插件支持以下功能：
- 查询当前CF平台上还未开始的比赛
- 比赛前48小时，11小时，3小时定时提醒。可以群提醒或好友私聊提醒
- 绑定用户ID 当检测到绑定用户分数发生变化时通过好友私聊发送分数变化消息

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-cfassistant

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-cfassistant
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-cfassistant
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-cfassistant
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-cfassistant
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_cfassistant"]

</details>


## 🎉 使用
### 指令表
- **输入:/CFHELP获取插件帮助 如**
  `/CFHELP`
- 输入:/CF 或 /cf 或 /查CF 或 /查cf 即可进行查询近期比赛 如
   `/CF`
- 在好友私聊下输入:/绑定 你的CF个人ID 即可对该账户分数进行监测(一个ID只能绑定一个QQ号) 如
  `/绑定 jiangly`
- 在群聊下输入:/群提醒 即可对本群开启比赛提醒功能(分别在48小时，11小时，3小时提醒一次) 如
  `/群提醒`
- 在群聊下输入:/取消群提醒 即可关闭本群的比赛提醒功能 如
  `/取消群提醒`
- 在好友私聊下输入:/提醒 即可开启比赛提醒功能(分别在48小时，11小时，3小时提醒一次) 如
  `/提醒`
- 在好友私聊下输入:/取消提醒 即可关闭比赛提醒功能 如
  `/取消提醒`

## 🖼️ 效果图
- 输入`/CFHELP`  
  ![](https://github.com/coyude/nonebot-plugin-cfassistant/blob/master/img/cfhelp.png)

- 输入`/CF`  
  ![](https://github.com/coyude/nonebot-plugin-cfassistant/blob/master/img/cf.png)

- 输入`/绑定 用户id`  
  ![](https://github.com/coyude/nonebot-plugin-cfassistant/blob/master/img/%E7%BB%91%E5%AE%9A%E7%94%A8%E6%88%B7.png)  
  **当监测到分数变化后自动发送**  
  ![](https://github.com/coyude/nonebot-plugin-cfassistant/blob/master/img/%E5%88%86%E6%95%B0%E5%8F%98%E5%8C%96%E6%8F%90%E9%86%92.png)

- 输入`/群提醒`  
  ![](https://github.com/coyude/nonebot-plugin-cfassistant/blob/master/img/%E7%BE%A4%E6%8F%90%E9%86%92.png)

- 输入`/取消群提醒`  
  ![](https://github.com/coyude/nonebot-plugin-cfassistant/blob/master/img/%E5%8F%96%E6%B6%88%E7%BE%A4%E6%8F%90%E9%86%92.png)

- 输入`/提醒`  
  ![](https://github.com/coyude/nonebot-plugin-cfassistant/blob/master/img/%E5%A5%BD%E5%8F%8B%E6%8F%90%E9%86%92.png)

- 输入`/取消提醒`  
  ![](https://github.com/coyude/nonebot-plugin-cfassistant/blob/master/img/%E5%8F%96%E6%B6%88%E5%A5%BD%E5%8F%8B%E6%8F%90%E9%86%92.png)    

- **群提醒&好友提醒的效果**  
  ![](https://github.com/coyude/nonebot-plugin-cfassistant/blob/master/img/%E6%8F%90%E9%86%92%E5%B1%95%E7%A4%BA.png)  
  
