# coding: UTF-8

import redis
import requests
from flask import Flask, request as flask_req

requests.packages.urllib3.disable_warnings()
cache = redis.StrictRedis(host="localhost", port=6379, db=0)
app = Flask(__name__)
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def unvalid_url(path):
    return '400 Bad Request'

@app.route('/from_cache') 
def valid_url():
        
    key = check_params(flask_req)
    if key:
        _hash = cache.get(key)
        if _hash:
            return _hash
        try:
            response = requests.get('https://vast-eyrie-4711.herokuapp.com/?key=%s' % key, verify=False, timeout=1)
        except requests.exceptions.ReadTimeout:
            return '408 Request Timeout'
        if response.text != 'error': 
            cache.set(key, response.text, ex=86400)             
        return response.text
    return '400 Bad Request'
      
def check_params(request):
    """
    GET /from_cache?key="some key"
    """
    if len(request.args)==1 and request.args.get('key'):
        return request.args.get('key')
    return None
    
if __name__ == '__main__':
    app.run(threaded=True)
    #app.run(processes=3)

