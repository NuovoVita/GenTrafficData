# -*- coding: utf-8 -*-
import json
import random
import time

import redis


class GenAttackTrafficData(object):
    queue_key = 'task:attack-traffic:queue'

    @classmethod
    def _con_redis(cls, host='127.0.0.1', port=6379, db=0):
        redis_pool = redis.ConnectionPool(host=host, port=port, db=db)
        return redis.StrictRedis(connection_pool=redis_pool)

    @classmethod
    def producer_traffic(cls, host='127.0.0.1', port=6379, db=0, num=1000):
        redis_client = cls._con_redis(host, port, db)
        traffic = {
            'ifname': 'LAN1',
            'type': 'ICMPFlood',
            'up_b': 0,
            'down_b': 0,
            'up_p': 0,
            'down_p': 0,
            'timestamp': 1662458092,
        }
        ifname_lst = ['LAN1', 'LAN2', 'LAN3', 'LAN4']
        attack_type_lst = ['ICMPFlood', 'Land', 'Smurf', 'SynFlood', 'TCPFlag', 'UDPFlood']
        start = int(time.time()) - 60 * 60 * 8
        while num:
            start += random.randint(0, 10)
            for index in range(10000):
                if index >= num:
                    break

                traffic['ifname'] = random.choice(ifname_lst)
                traffic['type'] = random.choice(attack_type_lst)
                traffic['up_b'] = random.randint(0, 10000)
                traffic['down_b'] = random.randint(0, 10000)
                traffic['up_p'] = random.randint(0, 10000)
                traffic['down_p'] = random.randint(0, 10000)
                traffic['timestamp'] = start
                result = redis_client.rpush(cls.queue_key, json.dumps(traffic))
                if result:
                    num -= 1


if __name__ == '__main__':
    GenAttackTrafficData.producer_traffic(host='192.168.1.70', port=6379, db=0, num=50000)
