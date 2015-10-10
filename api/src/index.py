#-*- encoding: utf-8 -*-

from flask import Flask, request
app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('FLASKY_API_CONFIG')

from flasky.lib.http.response import ApiError, make_api_resp, api_error_handler
from flasky.lib.http.request import on_json_loading_failed, get_or_400, get_arg_or_400, get_int_arg_or_400
from flasky.lib.http.session import set_user_session, get_user_id_or_401, need_session


"""初始化日志"""
from flasky.lib.log.logger import Logger, logger
Logger.init_logger(app.config['LOG_LEVEL'], app.config['LOG_FILE'])


"""导入Model"""
from flasky.model import db
db.init_app(app)
from flasky.model.flasky import User, Article, Label


"""设置错误处理
处理所有的HTTPException，输出对应的Json数据。因此，应用中则不能
    raise 400
    raise BadRequest
必须
    raise ApiError
    return make_api_resp()
"""
@app.errorhandler(ApiError)
def error_handler(error):
    return api_error_handler(error)

from werkzeug.exceptions import HTTPException, MethodNotAllowed
from werkzeug.http import HTTP_STATUS_CODES

def default_error_handler(error):
    return make_api_resp(status_code=error.code, msg=error.name)

for status_code in HTTP_STATUS_CODES.keys():
    app.error_handler_spec[None][status_code] = default_error_handler


"""设置前处理和后处理"""
@app.before_request
def before_request():
    """如果HTTP Body为Json数据，需要设置Header
        Content-Type: application/json
    """
    logger.info(Logger.dumps(t='req'))
    request.on_json_loading_failed = on_json_loading_failed

@app.after_request
def after_request(resp):
    return resp

@app.teardown_request
def teardown_request(e):
    if e is not None:
        logger.error(Logger.dumps(t='exception', e=str(e)))


"""视图"""
import uuid
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register():
    name = get_or_400(request.get_json(), 'name')
    user = db.session.query(User).filter(User.name==name).first()
    if user is not None:
        return make_api_resp(status_code=400, msg='user exists')
    password = get_or_400(request.get_json(), 'password')
    password_hash = bcrypt.generate_password_hash(password)
    user = User(name=name, password=password_hash)
    db.session.add(user)
    db.session.commit()
    return make_api_resp({'user_id':user.id})

@app.route('/login', methods=['POST'])
def login():
    name = get_or_400(request.get_json(), 'name')
    user = db.session.query(User).filter(User.name==name).first()
    if user is None:
        raise ApiError(status_code=404, msg='user does not exist')
    password = get_or_400(request.get_json(), 'password')
    if not bcrypt.check_password_hash(user.password, password):
        raise ApiError(status_code=401, msg='password is not correct')

    return set_user_session(user.id)

@app.route('/get_user')
def get_user():
    user_id = get_user_id_or_401()
    user = db.session.query(User).get(user_id)
    return make_api_resp(
        {'user':{'id':user_id, 'name':user.name}}
    )


@app.route('/')
@need_session
def index():
    i = get_int_arg_or_400('i')
    s = get_arg_or_400('s')
    d = request.args.get('d', 'ddd')
    return make_api_resp({'i':i, 's':s, 'd':d})

@app.route('/error')
def error():
    raise ApiError(500, {'info':'hello'})


if __name__ == '__main__':
    app.run()
