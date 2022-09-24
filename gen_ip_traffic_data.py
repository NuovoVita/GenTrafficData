# -*- coding: utf-8 -*-
import json
import random
import time

import faker
import redis

redis_pool = redis.ConnectionPool(host='192.168.1.70', port=6379, db=0)
redis_client = redis.StrictRedis(connection_pool=redis_pool)


class GenTrafficData(object):
    queue_key = 'task:ip-traffic:queue'

    @classmethod
    def producer_ip_traffic(cls, num=1000):
        ip_traffic = {
            'ip': '127.0.0.1',
            'up_b': 34820,
            'down_b': 34820,
            'up_p': 344,
            'down_p': 344,
            'timestamp': 1662458092,
        }
        fake = faker.Faker()
        start = int(time.time()) - 60 * 60 * 8
        while num:
            start += random.randint(0, 10)
            for index in range(10000):
                if index >= num:
                    break
                ip_traffic['ip'] = fake.ipv4() if random.randint(0, 100) % 10 else fake.ipv6()
                ip_traffic['up_b'] = random.randint(0, 10000)
                ip_traffic['down_b'] = random.randint(0, 10000)
                ip_traffic['up_p'] = random.randint(0, 10000)
                ip_traffic['down_p'] = random.randint(0, 10000)
                ip_traffic['timestamp'] = start
                result = redis_client.rpush(cls.queue_key, json.dumps(ip_traffic))
                if result:
                    num -= 1


if __name__ == '__main__':
    GenTrafficData.producer_ip_traffic(1000000)
