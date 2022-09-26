# -*- coding: utf-8 -*-
import json
import random
import time

import redis


class GenTypeTrafficData(object):
    queue_key = 'task:comm-traffic:queue'

    @classmethod
    def _con_redis(cls, host='127.0.0.1', port=6379, db=0):
        redis_pool = redis.ConnectionPool(host=host, port=port, db=db)
        return redis.StrictRedis(connection_pool=redis_pool)

    @classmethod
    def producer_traffic(cls, host='127.0.0.1', port=6379, db=0, num=1000):
        redis_client = cls._con_redis(host, port, db)
        traffic = {
            'ifname': 'LAN1',
            'timestamp': 1662458092,
            'uni_up_p': 0,
            'multi_up_p': 0,
            'broad_up_p': 0,
            'uni_up_b': 0,
            'multi_up_b': 0,
            'broad_up_b': 0,
            'uni_down_p': 0,
            'multi_down_p': 0,
            'broad_down_p': 0,
            'uni_down_b': 0,
            'multi_down_b': 0,
            'broad_down_b': 0,
        }
        ifname_lst = ['LAN1', 'LAN2', 'LAN3', 'LAN4']
        start = int(time.time()) - 60 * 60 * 8
        while num:
            start += random.randint(0, 10)
            for index in range(10000):
                if index >= num:
                    break

                traffic['ifname'] = random.choice(ifname_lst)
                traffic['uni_up_p'] = random.randint(0, 10000)
                traffic['multi_up_p'] = random.randint(0, 10000)
                traffic['broad_up_p'] = random.randint(0, 10000)
                traffic['uni_up_b'] = random.randint(0, 10000)
                traffic['multi_up_b'] = random.randint(0, 10000)
                traffic['broad_up_b'] = random.randint(0, 10000)
                traffic['uni_down_p'] = random.randint(0, 10000)
                traffic['multi_down_p'] = random.randint(0, 10000)
                traffic['broad_down_p'] = random.randint(0, 10000)
                traffic['uni_down_b'] = random.randint(0, 10000)
                traffic['multi_down_b'] = random.randint(0, 10000)
                traffic['broad_down_b'] = random.randint(0, 10000)
                traffic['timestamp'] = start
                result = redis_client.rpush(cls.queue_key, json.dumps(traffic))
                if result:
                    num -= 1


if __name__ == '__main__':
    GenTypeTrafficData.producer_traffic(host='192.168.1.70', port=6379, db=0, num=50000)
