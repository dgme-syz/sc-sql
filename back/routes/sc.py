from .config import connection
from flask import request, Blueprint
sc = Blueprint('sc', __name__)

@sc.route('/api/sc', methods=['GET'])
def get_data():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM sc')
    # 获取列名
    column_names = [description[0] for description in cursor.description]
    result = cursor.fetchall()
    cursor.close()

    # 将结果构造成包含列名的字典列表
    data = [dict(zip(column_names, row)) for row in result]
    
    return data
@sc.route('/api/sc', methods=['POST'])
def filter_data():
    data = request.json
    print(data)
    try:
        sno, cno= data['params']['sno'], data['params']['cno']
        cursor = connection.cursor()
        if sno == '' and cno == '':
            return get_data()
        elif sno == '':
            cmd = 'SELECT * FROM sc WHERE cno = :cno'
            cursor.execute(cmd, cno=cno)
        elif cno == '':
            cmd = 'SELECT * FROM sc WHERE sno = :sno'
            cursor.execute(cmd, sno=sno)
        else:
            cmd = 'SELECT * FROM sc WHERE sno = :sno AND cno = :cno'
            cursor.execute(cmd, sno=sno, cno=cno)
        column_names = [description[0] for description in cursor.description]
        result = cursor.fetchall()
        cursor.close()
        data = [dict(zip(column_names, row)) for row in result]
    except Exception as e:
        print(e)
        data = []
    return data

# 删除数据
@sc.route('/api/sc_del', methods=['POST'])
def delete_data():
    data = request.json
    print(data)
    try:
        sno, cno= data['params']['sno'], data['params']['cno']
        cursor = connection.cursor()
        cmd = 'DELETE FROM sc WHERE sno = :sno AND cno = :cno'
        cursor.execute(cmd, sno=sno, cno=cno)
        connection.commit()
        cursor.close()
        return {'status': 'success'}
    except Exception as e:
        print(e)
        return {'status': 'failed'}
# 修改
@sc.route('/api/sc_update', methods=['POST'])
def update_data():
    data = request.json
    print(data)
    try:
        old_sno, old_cno = data['params']['old_sno'], data['params']['old_cno']
        sno, cno, sscore = data['params']['sno'], data['params']['cno'], data['params']['sscore']
        cursor = connection.cursor()
        
        # 首先判断 sno 是否在 s 表中存在, cno 是否在 c 表中存在
        cmd = 'SELECT * FROM s WHERE sno = :sno'
        cursor.execute(cmd, sno=sno)
        if not cursor.fetchone():
            return {'status': 'failed', 'msg': '学号不存在'}
        cmd = 'SELECT * FROM c WHERE cno = :cno'
        cursor.execute(cmd, cno=cno)
        if not cursor.fetchone():
            return {'status': 'failed', 'msg': '课程号不存在'}
        
        cmd = 'UPDATE sc SET sno = :sno, cno = :cno, sscore = :sscore WHERE sno = :old_sno AND cno = :old_cno'
        cursor.execute(cmd, sno=sno, cno=cno, sscore=sscore, old_sno=old_sno, old_cno=old_cno)
        connection.commit()
        cursor.close()
        return {'status': 'success'}
    except Exception as e:
        print(e)
        return {'status': 'failed'}
# 添加数据
@sc.route('/api/sc_add', methods=['POST'])
def add_data():
    data = request.json
    print(data)
    try:
        sno, cno, sscore = data['params']['sno'], data['params']['cno'], data['params']['sscore']
        print(sno, cno, sscore)
        cursor = connection.cursor()
        
        # 首先判断 sno 是否在 s 表中存在, cno 是否在 c 表中存在
        cmd = 'SELECT sname FROM s WHERE sno = :sno'
        cursor.execute(cmd, sno=sno)
        res = cursor.fetchone()
        if not res:
            return {'status': 'failed', 'msg': '学号不存在'}
        # 获得学生姓名 sname
        sname = res[0]
        print(sname)
        cmd = 'SELECT cname, cscore FROM c WHERE cno = :cno'
        cursor.execute(cmd, cno=cno)
        res = cursor.fetchone()
        if not res:
            return {'status': 'failed', 'msg': '课程号不存在'}
        # 获得课程名 cname, 课程学分 cscore
        cname, cscore = res
        # 如果 sc 表中已经存在该学号和课程号，则返回失败
        cmd = 'SELECT * FROM sc WHERE sno = :sno AND cno = :cno'
        cursor.execute(cmd, sno=sno, cno=cno)
        if cursor.fetchone():
            return {'status': 'failed', 'msg': '学号和课程号已存在'}
        
        cmd = 'INSERT INTO sc VALUES (:sno, :cno, :sname, :cname, :cscore, :sscore)'
        # 打印一下
        print(sno, cno, sname, cname, cscore, sscore)
        cursor.execute(cmd, sno=sno, cno=cno, sname=sname, cname=cname, cscore=cscore, sscore=sscore)
        connection.commit()
        cursor.close()
        return {'status': 'success'}
    except Exception as e:
        print(e)
        return {'status': 'failed'}