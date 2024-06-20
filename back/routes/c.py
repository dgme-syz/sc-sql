from .config import connection
from flask import request, Blueprint
c = Blueprint('c', __name__)

@c.route('/api/c', methods=['GET'])
def get_data():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM c')
    # 获取列名
    column_names = [description[0] for description in cursor.description]
    result = cursor.fetchall()
    cursor.close()

    # 将结果构造成包含列名的字典列表
    data = [dict(zip(column_names, row)) for row in result]
    return data

# 删除数据
@c.route('/api/c_del', methods=['POST'])
def delete_data():
    data = request.json
    print(data)
    try:
        cno = data['params']['cno']
        cursor = connection.cursor()
        # 先删 sc 表作为外键
        cmd = 'DELETE FROM sc WHERE cno = :cno'
        cursor.execute(cmd, cno=cno)
        # 再删 s 表
        cmd = 'DELETE FROM c WHERE cno = :cno'
        cursor.execute(cmd, cno=cno)
        connection.commit()
        cursor.close()
        return {'status': 'success'}
    except Exception as e:
        print(e)
        return {'status': 'failed'}
    
@c.route('/api/c_update', methods=['POST'])
def update_data():
    data = request.json
    print(data)
    try:
        old_cno = data['params']['old_cno']
        cno, cname, cscore = data['params']['new_info']['CNO'], \
            data['params']['new_info']['CNAME'], \
            data['params']['new_info']['CSCORE']
        cursor = connection.cursor()
        
        # 首先判断 cno 是否在 c 表中存在
        cmd = 'SELECT * FROM c WHERE cno = :cno'
        cursor.execute(cmd, cno=cno)
        if not cursor.fetchone():
            return {'status': 'failed', 'msg': '课程号不存在'}
        
        cmd = 'UPDATE c SET cno = :cno, cname = :cname, cscore = :cscore WHERE cno = :old_cno'
        cursor.execute(cmd, cno=cno, cname=cname, \
            cscore=cscore, old_cno=old_cno)
        connection.commit()
        cursor.close()
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'failed', 'msg': str(e)}

# 添加数据
@c.route('/api/c_add', methods=['POST'])
def add_data():
    data = request.json
    print(data)
    data = request.json
    print(data)
    try:
        cno, cname, cscore = data['params']['new_info']['CNO'], \
            data['params']['new_info']['CNAME'], \
            data['params']['new_info']['CSCORE']
        cursor = connection.cursor()
        
        # 首先判断 cno 是否在 c 表中存在
        cmd = 'SELECT * FROM c WHERE cno = :cno'
        cursor.execute(cmd, cno=cno)
        if cursor.fetchone():
            return {'status': 'failed', 'msg': '课程号已存在'}
        
        cmd = 'INSERT INTO c VALUES (:cno, :cname, :cscore)'
        cursor.execute(cmd, cno=cno, cname=cname, \
            cscore=cscore)
        connection.commit()
        cursor.close()
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'failed', 'msg': str(e)}

@c.route('/api/c', methods=['POST'])
def filter_data():
    data = request.json
    print(data)
    try:
        cno = data['params']['cno']
        cursor = connection.cursor()
        if cno == '' :
            return get_data()
        else:
            cmd = 'SELECT * FROM c WHERE cno = :cno'
            cursor.execute(cmd, cno=cno)
        column_names = [description[0] for description in cursor.description]
        result = cursor.fetchall()
        cursor.close()
        data = [dict(zip(column_names, row)) for row in result]
    except Exception as e:
        data = []
    return data