# -*- coding: utf-8 -*-
import copy
import json
import random
import time

import redis


class GenDiagTrafficData(object):
    queue_key = 'task:diag-traffic:queue'

    @classmethod
    def _con_redis(cls, host='127.0.0.1', port=6379, db=0):
        redis_pool = redis.ConnectionPool(host=host, port=port, db=db)
        return redis.StrictRedis(connection_pool=redis_pool)

    @classmethod
    def producer_traffic(cls, host='127.0.0.1', port=6379, db=0, num=1000):
        redis_client = cls._con_redis(host, port, db)

        diag_traffic_mapping = {
            'tcp': {
                'proto': 'tcp',
                'tcp_rst': 0,
                'tcp_resyn': 0,
                'tcp_dupack': 0,
                'tcp_retrans': 0,
                'timestamp': 1662458092,
            },
            'ip': {
                'proto': 'ip',
                'ip_invalidchksum': 0,
                'timestamp': 1662458092,
            },
            'icmp': {
                'proto': 'icmp',
                'icmp_unreach': 0,
                'timestamp': 1662458092,
            }
        }
        start = int(time.time()) - 60 * 60 * 8
        while num:
            start += random.randint(0, 10)
            for index in range(10000):
                if index >= num:
                    break

                proto = random.choice(list(diag_traffic_mapping.keys()))
                traffic = copy.deepcopy(diag_traffic_mapping[proto])
                for name in traffic.keys():
                    if name not in ['proto', 'timestamp']:
                        traffic[name] = random.randint(0, 10000)
                traffic['timestamp'] = start
                result = redis_client.rpush(cls.queue_key, json.dumps(traffic))
                if result:
                    num -= 1


if __name__ == '__main__':
    GenDiagTrafficData.producer_traffic(host='192.168.1.70', port=6379, db=0, num=50000)
