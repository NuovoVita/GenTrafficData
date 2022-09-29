# -*- coding: utf-8 -*-
import json
import math
import random
import time

import redis


class GenProtoTrafficData(object):
    size = 1000
    proto_lst = [
        'osu-nms', 'domain', 'efs', 'oob-ws-https', 'teedtap', 'opcda', 'kpasswd', 'pcanywherestat', 'echo',
        'gprs-data', 'BACnet', 'ENIP-UDP', 'ibm-db2', 'sunrpc', 'ntalk', 'netiq-ncap', 'xdmcp', 'ingreslock',
        'sip', 'pkix-3-ca-ra', 'epmap', 'svrloc', 'pnrt', 'pcp', 'scol', 'snmp', 'daytime', 'cmip-agent',
        'netbios-dgm', 'ms-sql-m', 'compressnet', 'netop-school', 'fins', 'rfile', 'cadlock2', 'vrtl-vmf-sa',
        'mobileip-agent', 'pcmail-srv', 'retrospect', 'UNKNOW', 'smux', 'ntp', 'cisco-sccp', 'oob-ws-http',
        'dbase', 'dhcp', 'tftp', 'qotd', 'goose', 'ws-discovery', 'dhcpv6-server', 'netbios-ns', 'tacacs',
        'bootps', 'dns', 'timbuktu', 'dcerpcudp', 'chargen', 'http-rpc-epmap', 'ssdp', 'nameserver', 'puprouter',
        'talk', 'ftp-data',
    ]
    queue_key = 'task:proto-traffic:queue'

    @classmethod
    def _con_redis(cls, host='127.0.0.1', port=6379, db=0):
        redis_pool = redis.ConnectionPool(host=host, port=port, db=db)
        return redis.StrictRedis(connection_pool=redis_pool)

    @classmethod
    def producer_traffic(cls, host='127.0.0.1', port=6379, db=0, num=1000):
        redis_client = cls._con_redis(host, port, db)
        traffic = {
            'timestamp': 1662458092,
            'proto': 'domain',
            'up_b': 0,
            'down_b': 0,
            'up_p': 0,
            'down_p': 0,
        }

        start = int(time.time()) - math.ceil(num / cls.size * 1.0)
        while num:
            start += random.randint(0, 5)
            for _ in range(cls.size):
                traffic['proto'] = random.choice(cls.proto_lst)
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
    GenProtoTrafficData.producer_traffic(host='192.168.1.70', port=6379, db=0, num=50000)
