from setuptools import setup
from setuptools import find_packages


VERSION = '1.0.1'

setup(
    name='nonebot-plugin-cfassistant', 
    version=VERSION,  
    description='一个支持CF(codeforces)平台查询比赛/比赛提醒/监测分数变化的nonebot机器人插件', 
    packages=find_packages(),
    zip_safe=False,
    url='https://github.com/coyude/nonebot-plugin-cfassistant',
    author="coyude",
    install_requires=[
        "requests>=2.23.0",
        "nonebot_plugin_apscheduler>=0.3.0",
        "nonebot2>=2.0.0",
        "nonebot-adapter-onebot>=2.2.3",
        "aiosqlite>=0.17.0"
    ],
)