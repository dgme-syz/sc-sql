from .config import connection
import json, cx_Oracle, os
from flask import request, Blueprint, current_app
s = Blueprint('s', __name__)

@s.route('/api/s', methods=['GET'])
def get_data():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM s')
    # 获取列名
    column_names = [description[0] for description in cursor.description]
    result = cursor.fetchall()
    cursor.close()

    # 将结果构造成包含列名的字典列表
    data = [dict(zip(column_names, row)) for row in result]
    return data

# 删除数据
@s.route('/api/s_del', methods=['POST'])
def delete_data():
    data = request.json
    print(data)
    try:
        sno = data['params']['sno']
        cursor = connection.cursor()
        # 先删 sc 表作为外键
        cmd = 'DELETE FROM sc WHERE sno = :sno'
        cursor.execute(cmd, sno=sno)
        # 再删 s 表
        cmd = 'DELETE FROM s WHERE sno = :sno'
        cursor.execute(cmd, sno=sno)
        connection.commit()
        cursor.close()
        return {'status': 'success'}
    except Exception as e:
        print(e)
        return {'status': 'failed'}
    
@s.route('/api/s_update', methods=['POST'])
def update_data():
    data = request.json
    print(data)
    try:
        old_sno = data['params']['old_sno']
        sno, sname, ssex, sage = data['params']['new_info']['SNO'], \
            data['params']['new_info']['SNAME'], \
            data['params']['new_info']['SSEX'], data['params']['new_info']['SAGE']
        cursor = connection.cursor()
        
        # 首先判断 sno 是否在 s 表中存在
        cmd = 'SELECT * FROM s WHERE sno = :sno'
        cursor.execute(cmd, sno=sno)
        if not cursor.fetchone():
            return {'status': 'failed', 'msg': '学号不存在'}
        
        cmd = 'UPDATE s SET sno = :sno, sname = :sname, ssex = :ssex, sage = :sage WHERE sno = :old_sno'
        cursor.execute(cmd, sno=sno, sname=sname, \
            ssex=ssex, sage=sage, old_sno=old_sno)
        connection.commit()
        cursor.close()
        return {'status': 'success'}
    except Exception as e:
        print(e)
        return {'status': 'failed'}

# 添加数据
@s.route('/api/s_add', methods=['POST'])
def add_data():
    data = request.json
    print(data)
    data = request.json
    print(data)
    try:
        sno, sname, ssex, sage = data['params']['new_info']['SNO'], \
            data['params']['new_info']['SNAME'], \
            data['params']['new_info']['SSEX'], data['params']['new_info']['SAGE']
        cursor = connection.cursor()
        
        # 首先判断 sno 是否在 s 表中存在
        cmd = 'SELECT * FROM s WHERE sno = :sno'
        cursor.execute(cmd, sno=sno)
        if cursor.fetchone():
            return {'status': 'failed', 'msg': '学号已存在'}
        
        cmd = 'INSERT INTO s VALUES (:sno, :sname, :ssex, :sage)'
        cursor.execute(cmd, sno=sno, sname=sname, \
            ssex=ssex, sage=sage)
        connection.commit()
        cursor.close()
        return {'status': 'success'}
    except Exception as e:
        print(e)
        return {'status': 'failed'}

@s.route('/api/s', methods=['POST'])
def filter_data():
    data = request.json
    print(data)
    try:
        sno = data['params']['sno']
        cursor = connection.cursor()
        if sno == '' :
            return get_data()
        else:
            cmd = 'SELECT * FROM s WHERE sno = :sno'
            cursor.execute(cmd, sno=sno)
        column_names = [description[0] for description in cursor.description]
        result = cursor.fetchall()
        cursor.close()
        data = [dict(zip(column_names, row)) for row in result]
    except Exception as e:
        print(e)
        data = []
    return data