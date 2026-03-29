import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'root')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')

# 微信小程序配置
APPID = os.environ.get("APPID", 'wxa015b0bacfabc252')
APPSECRET = os.environ.get("APPSECRET", '338b44ffb4ba0b88131b06c7fcb7f06c')
