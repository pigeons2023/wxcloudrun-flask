from datetime import datetime
from flask import request
import requests
import config
from run import app
from wxcloudrun.model import User
from wxcloudrun import db
from wxcloudrun.response import make_succ_response, make_err_response


@app.route('/api/login', methods=['POST'])
def login():
    """
    用户登录接口
    接收姓名+学号，同时绑定微信openid
    """
    # 获取请求体参数
    params = request.get_json()

    # 检查参数
    if 'name' not in params or 'student_id' not in params or 'code' not in params:
        return make_err_response('缺少必要参数，需要提供name、student_id和code')

    name = params['name']
    student_id = params['student_id']
    code = params['code']

    # 调用微信API获取openid
    appid = config.APPID
    secret = config.APPSECRET
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        return make_err_response(f'微信接口调用失败: {str(e)}')

    if 'errcode' in data:
        return make_err_response(f'微信接口错误: {data.get("errmsg", "未知错误")}')

    openid = data.get('openid')
    if not openid:
        return make_err_response('无法获取用户openid')

    # 检查用户是否已存在（根据学号）
    existing_user = User.query.filter(User.student_id == student_id).first()
    
    if existing_user:
        # 更新用户信息
        existing_user.name = name
        existing_user.openid = openid
        existing_user.updated_at = datetime.now()
        db.session.commit()
        user_data = {
            'id': existing_user.id,
            'name': existing_user.name,
            'student_id': existing_user.student_id,
            'openid': existing_user.openid
        }
        return make_succ_response(user_data)


@app.route('/api/seed', methods=['POST'])
def seed_test_data():
    """
    插入测试数据接口
    插入姓名:test, 学号:123
    """
    try:
        # 检查是否已存在
        existing_user = User.query.filter(User.student_id == '123').first()
        if existing_user:
            return make_succ_response({
                'message': '测试数据已存在',
                'user': {
                    'id': existing_user.id,
                    'name': existing_user.name,
                    'student_id': existing_user.student_id,
                    'openid': existing_user.openid
                }
            })
        
        # 创建测试用户
        test_user = User(
            name='test',
            student_id='123',
            openid='test_openid_' + str(datetime.now().timestamp())
        )
        db.session.add(test_user)
        db.session.commit()
        
        return make_succ_response({
            'message': '测试数据插入成功',
            'user': {
                'id': test_user.id,
                'name': test_user.name,
                'student_id': test_user.student_id,
                'openid': test_user.openid
            }
        })
    except Exception as e:
        db.session.rollback()
        return make_err_response(f'插入测试数据失败: {str(e)}')
    else:
        # 创建新用户
        new_user = User(
            name=name,
            student_id=student_id,
            openid=openid
        )
        db.session.add(new_user)
        db.session.commit()
        user_data = {
            'id': new_user.id,
            'name': new_user.name,
            'student_id': new_user.student_id,
            'openid': new_user.openid
        }
        return make_succ_response(user_data)
