# -*- coding: utf-8 -*-
import json
import math
import random
import time

import faker
import redis


class GenIPProtoTrafficData(object):
    size = 1000
    video_proto_lst = ['sip', 'rtsp', 'onvif', 'rtp']
    queue_key = 'task:ip-proto-traffic:queue'

    @classmethod
    def _con_redis(cls, host='127.0.0.1', port=6379, db=0):
        redis_pool = redis.ConnectionPool(host=host, port=port, db=db)
        return redis.StrictRedis(connection_pool=redis_pool)

    @classmethod
    def producer_traffic(cls, host='127.0.0.1', port=6379, db=0, num=1000):
        redis_client = cls._con_redis(host, port, db)
        traffic = {
            'timestamp': 1662458092,
            'proto': 'sip',
            'up_b': 0,
            'down_b': 0,
            'up_p': 0,
            'down_p': 0,
            'ip': '127.0.0.1'
        }

        fake = faker.Faker()
        ip_res = [(fake.ipv4() if random.randint(0, 1000) % 1000 else fake.ipv6()) for _ in range(1000)]
        start = int(time.time()) - math.ceil(num / cls.size * 1.0)
        while num:
            start += random.randint(0, 5)
            for _ in range(cls.size):
                traffic['ip'] = random.choice(ip_res)
                traffic['proto'] = random.choice(cls.video_proto_lst)
                traffic['up_b'] = random.randint(0, 10000)
                traffic['down_b'] = random.randint(0, 10000)
                traffic['up_p'] = random.randint(0, 10000)
                traffic['down_p'] = random.randint(0, 10000)
                traffic['timestamp'] = start
                result = redis_client.rpush(cls.queue_key, json.dumps(traffic))
                if result:
                    num -= 1
                if num <= 0:
                    break


if __name__ == '__main__':
    GenIPProtoTrafficData.producer_traffic(host='192.168.1.70', port=6379, db=0, num=50000)
