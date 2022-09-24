# -*- coding: utf-8 -*-
import json
import random
import time

import redis

redis_pool = redis.ConnectionPool(host='192.168.1.70', port=6379, db=0)
redis_client = redis.StrictRedis(connection_pool=redis_pool)


class GenTrafficData(object):
    queue_key = 'task:attack-traffic:queue'

    @classmethod
    def producer_attack_traffic(cls, num=1000):
        ip_traffic = {
            'ifname': 'LAN1',
            'type': 'ICMPFlood',
            'up_b': 34820,
            'down_b': 34820,
            'up_p': 344,
            'down_p': 344,
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

                ip_traffic['ifname'] = random.choice(ifname_lst)
                ip_traffic['type'] = random.choice(attack_type_lst)
                ip_traffic['up_b'] = random.randint(0, 10000)
                ip_traffic['down_b'] = random.randint(0, 10000)
                ip_traffic['up_p'] = random.randint(0, 10000)
                ip_traffic['down_p'] = random.randint(0, 10000)
                ip_traffic['timestamp'] = start
                result = redis_client.rpush(cls.queue_key, json.dumps(ip_traffic))
                if result:
                    num -= 1


if __name__ == '__main__':
    GenTrafficData.producer_attack_traffic(50000)
