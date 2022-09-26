# -*- coding: utf-8 -*-
import json
import random
import time

import redis


class GenProtoTrafficData(object):
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
        start = int(time.time()) - 60 * 60 * 8
        while num:
            start += random.randint(0, 10)
            for index in range(10000):
                if index >= num:
                    break

                traffic['proto'] = random.choice(proto_lst)
                traffic['up_b'] = random.randint(0, 10000)
                traffic['down_b'] = random.randint(0, 10000)
                traffic['up_p'] = random.randint(0, 10000)
                traffic['down_p'] = random.randint(0, 10000)
                traffic['timestamp'] = start
                result = redis_client.rpush(cls.queue_key, json.dumps(traffic))
                if result:
                    num -= 1


if __name__ == '__main__':
    GenProtoTrafficData.producer_traffic(host='192.168.1.70', port=6379, db=0, num=50000)
