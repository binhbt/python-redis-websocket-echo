from flask import Flask
from redis import Redis
from flask_sse import sse
from flask import request, abort
from pub.config import APP_AUTH
from pub.err.errs import *
from pub.util.token_utils import decode_auth_token, encode_auth_token
from flask import jsonify
import traceback
from flask_uwsgi_websocket import GeventWebSocket

app = Flask(__name__)
# app.wsgi_app = AuthMiddleWare(app.wsgi_app)
websocket = GeventWebSocket(app)


redis = Redis(host='redis', port=6379)
app.config["REDIS_URL"] = "redis://redis:6379"


# def on_success(http_code, data=None):
#     meta = OrderedDict()
#     meta['code'] = int(http_code.split(" ")[0])
#     meta['message'] = http_code.split(" ")[1]

#     obj = OrderedDict()
#     obj['meta'] = meta
#     obj['data'] = data
#     return jsonify(obj)
# @app.before_request
# def check_auth_token():
#     path = request.path

#     if not APP_AUTH['TOKEN_ON']:
#         return
#     if "/send" in path:
#         return
#     if "/stream" in path:
#         return
#     if "/api/v1/devices/validate" in path:
#         return

#     print("Authorization---req.headers: %s", request.headers)
#     if "X-API-KEY" in request.headers:
#         request_api_key = request.headers["X-API-KEY"]
#         if request_api_key is not None:
#             isok, resp = decode_auth_token(request_api_key)
#             if not isok:
#                 return jsonify(UnauthorizedError(resp).__dict__)
#             else:
#                 return
#         else:
#             return
#     else:
#         return jsonify(MissingApiKey('Your request did not include an x-api-key').__dict__)

# @app.route('/')
# def hello():
#     print('api  .............')
#     redis.incr('hits')
#     return 'Hello World! I have been seen %s times.' % redis.get('hits')

# app.register_blueprint(sse, url_prefix='/stream')

# @app.route('/send')
# def send_message():
#     sse.publish({"message": "Hello!"}, type='greeting')
#     return "Message sent!"

# @app.route('/api/v1/devices/validate', methods=['POST'])
# def validate_device():
#     try:
#         req = request
#         try:
#             raw_json = req.stream.read()
#             user_req = json.loads(raw_json.decode('utf-8'))
#         except Exception:
#             return jsonify(ServerUnknowError('Read data error. Have error on server').__dict__)
#         print('abc')
#         print(req)
#         # user_req = req.context['data']
#         x_key = user_req['x_param']
#         device_id = user_req['device_id']
#         device_model = user_req['device_model']
#         device_os = user_req['device_os']
#         if x_key == APP_AUTH['PUBLIC_KEY']:
#             if device_id == None:
#                 device_id = 'device_id'
#             if device_model == None:
#                 device_model = 'device_model'
#             if device_os == None:
#                 device_os = 'device_os'
#             device_info = device_id + '|' + device_model + '|' + device_os
#             auth_token = encode_auth_token(device_info)
#             return on_success('200 OK', auth_token.decode('utf-8'))
#         else:
#             return jsonify(TokenInvalidError('Invalite token error').__dict__)
#     except:
#         traceback.print_exc()
#         return jsonify(ServerUnknowError('Have error on server').__dict__)

# @app.route('/api/v1/notifications', methods=['POST', 'PUT', 'DELETE'])
# def send_notifications():
#     try:
#         raw_json = request.stream.read()
#         user_req = json.loads(raw_json.decode('utf-8'))
#         sse.publish(user_req, type='greeting')

#         return on_success('200 OK', 'Message sent')
#     except:
#         traceback.print_exc()
#         return jsonify(ServerUnknowError('Have error on server').__dict__)
CHANNEL='notifications_channel'
pub = redis.pubsub()

@websocket.route('/echo/<client_id>')
def echo(ws, client_id):

    pub.subscribe(CHANNEL)
    while True:
        # msg = ws.receive()
        # ws.send(msg)
        #Receive message
        msg = get_socket_message_and_send(ws)
        #Send message
        msg = get_redis_message()
        if msg:
            str_mess = str(msg)+'-'+client_id
            ws.send(str_mess.encode('utf-8'))

def get_socket_message_and_send(ws):
    msg = ws.receive()
    # ws.send(msg)
    if msg:
        redis.publish(
            channel=CHANNEL,
            message=msg
        ) 
    return msg   
def get_redis_message():
    data = pub.get_message()
    if data:
        message = data['data']
        if message and message != 1:
            return message
    return None


@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
