from datetime import datetime
from flask import render_template, request
import requests
import config
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters, User
from wxcloudrun import db
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route('/api/login', methods=['POST'])
def login():
    """
    :return: 登录结果
    """
    # 获取请求体参数
    params = request.get_json()

    # 检查参数
    if 'name' not in params or 'student_id' not in params or 'code' not in params:
        return make_err_response('缺少必要参数')

    name = params['name']
    student_id = params['student_id']
    code = params['code']

    # 调用微信API获取openid
    appid = config.APPID
    secret = config.APPSECRET
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code"
    response = requests.get(url)
    data = response.json()

    if 'errcode' in data:
        return make_err_response(data['errmsg'])

    openid = data['openid']

    # 检查用户是否已存在
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


@app.route('/api/user/<student_id>', methods=['GET'])
def get_user(student_id):
    """
    :return: 用户信息
    """
    user = User.query.filter(User.student_id == student_id).first()
    if not user:
        return make_err_response('用户不存在')
    user_data = {
        'id': user.id,
        'name': user.name,
        'student_id': user.student_id,
        'openid': user.openid
    }
    return make_succ_response(user_data)
