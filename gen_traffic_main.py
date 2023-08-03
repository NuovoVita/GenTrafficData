import multiprocessing as mp

from gen_attack_traffic_data import GenAttackTrafficData
from gen_audit_proto_data import GenAuditProtoData
from gen_diag_traffic_data import GenDiagTrafficData
from gen_ip_proto_traffic_data import GenIPProtoTrafficData
from gen_ip_traffic_data import GenIPTrafficData
from gen_package_length_data import GenPkgLengthData
from gen_port_traffic_data import GenPortTrafficData
from gen_proto_traffic_data import GenProtoTrafficData
from gen_realtime_traffic_data import GenRealtimeTrafficData
from gen_type_traffic_data import GenTypeTrafficData


def gen_traffic_process(host='127.0.0.1', port=6379, db=0, num=50000):
    processes = [
        mp.Process(target=GenAttackTrafficData.producer_traffic, args=(host, port, db, num)),
        mp.Process(target=GenAuditProtoData.producer_traffic, args=(host, port, db, num)),
        mp.Process(target=GenDiagTrafficData.producer_traffic, args=(host, port, db, num)),
        mp.Process(target=GenIPProtoTrafficData.producer_traffic, args=(host, port, db, num)),
        mp.Process(target=GenIPTrafficData.producer_traffic, args=(host, port, db, num)),
        mp.Process(target=GenPkgLengthData.producer_traffic, args=(host, port, db, num)),
        mp.Process(target=GenPortTrafficData.producer_traffic, args=(host, port, db, num)),
        mp.Process(target=GenProtoTrafficData.producer_traffic, args=(host, port, db, num)),
        mp.Process(target=GenRealtimeTrafficData.producer_traffic, args=(host, port, db, num)),
        mp.Process(target=GenTypeTrafficData.producer_traffic, args=(host, port, db, num)),
    ]

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()


if __name__ == '__main__':
    gen_traffic_process('192.168.1.70', 6379, 0, 50000)
