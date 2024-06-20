import cx_Oracle, os

# 配置数据库连接信息
username = os.getenv('ORACLE_USER')
password = os.getenv('ORACLE_PASSWORD')
host = os.getenv('ORACLE_HOST')
port = os.getenv('ORACLE_PORT')
service_name = os.getenv('ORACLE_DB')
dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
connection = cx_Oracle.connect(username, password, dsn)