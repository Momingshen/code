# -*- coding: utf-8 -*-
import redis
# from requests.api import get
# from tenacity import retry, stop_after_attempt


PROXIES_CONF = {
    'joinchain2': {
        "http" : "http://%(user)s:%(pwd)s@%(proxy)s/" % {
            "user": "t14480863717233", "pwd": "1rcu6yq6", "proxy": "tps539.kdlapi.com:15818"},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
            "user": "t14480863717233", "pwd": "1rcu6yq6", "proxy": "tps539.kdlapi.com:15818"},
        "limit_list": [9, 10, 1, 1]
    },
    # 'punctuation': {
    #     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
    #         "user": "t19774138550217", "pwd": "8xlahyxl", "proxy": "tps231.kdlapi.com:15818"},
    #     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
    #         "user": "t19774138550217", "pwd": "8xlahyxl", "proxy": "tps231.kdlapi.com:15818"},
    #     "limit_list": [4, 5, 1, 1]
    # },
    # 'joinchain': {
    #     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
    #         "user": "t19584222992636", "pwd": "x2885ina", "proxy": "tps196.kdlapi.com:15818"},
    #     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
    #         "user": "t19584222992636", "pwd": "x2885ina", "proxy": "tps196.kdlapi.com:15818"},
    #     "limit_list": [4, 5, 1, 1]
    # }
}


class ProxyLimit(object):
    def __init__(self):
        # urls 存储的reids
        self.redis_host = '117.48.233.248'
        self.redis_port = 22164
        self.redis_password = 'redis512513'
        # redis 连接
        self.r = self.connect_redis(host=self.redis_host,
                                    port=self.redis_port,
                                    password=self.redis_password)

    def connect_redis(self, host, port, password):
        pool = redis.ConnectionPool(host=host,
                                    port=port,
                                    password=password,
                                    decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        return r

    def req_throttle(self, party):
        res = self.r.execute_command(
            'CL.THROTTLE', f'{party}:proxy', *PROXIES_CONF[party]['limit_list'])
        if res[0] == 0:
            return True
        elif res[0] == 1:
            return False

    # @retry(stop=stop_after_attempt(6))  # 重试6次后不再重试
    # @retry
    def priority_req_throttle(self, party_list):
        for party in party_list:
            res = self.req_throttle(party)
            # 按优先级获取代理，只要获取到一个即可返回
            if res == True:
                return party
            elif res == False:
                pass
        # 全都获取不到返回异常
        return None


ProxyLimit = ProxyLimit()
party_list = PROXIES_CONF.keys()


def get_proxy():
    party = False
    while not party:
        party = ProxyLimit.priority_req_throttle(party_list)
    return PROXIES_CONF[party]

# print(get_proxy())