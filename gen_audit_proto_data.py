# -*- coding: utf-8 -*-
import json
import math
import random
import time
import uuid
from datetime import datetime

import faker
import redis


class GenAuditProtoData(object):
    size = 1000
    queue_key = 'task:audit-proto:queue'
    proto = ['http', 'ftp']

    @classmethod
    def _con_redis(cls, host='127.0.0.1', port=6379, db=0):
        redis_pool = redis.ConnectionPool(host=host, port=port, db=db)
        return redis.StrictRedis(connection_pool=redis_pool)

    @classmethod
    def _gen_audit_ftp_record(cls):
        cmd_lst = [
            'HELP', 'USER', 'CHMOD', 'PORT', 'STAT', 'ALLO', 'REST', 'PASS', 'SYST', 'MAIL', 'LIST', 'TYPE', 'PASV',
            'SITE', 'STATUS', 'RESET', 'QUIT', 'PWD', ]

        info_lst = [
            'anonymous',
            'nobody',
            '20560',
            'system',
            'p>Process limits control the number of processes per user.</p>',
            ' under user ids other than the web server user id, this directive',
            'authentication</td></tr>',
            'sername/password <em>and</em> client host address. In this case',
            'asses the address access restriction <em>and</em> enters a valid',
            'sername and password. With the <code>Any</code> option the client will be',
            'ranted access if they either pass the host restriction or enter a',
            'alid username and password. This can be used to password restrict',
            'rompting for a password.</p>',
            'eople outside of your network provide a password, you could use a',
            ' Require valid-user<br />',
            'sys',
            'LALA',
            'nessus@192.168.27.152',
            'qyuqjKXa',
            'dbsnmp',
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
            'assword required for aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'IEUser@',
            'nessus@nessus.org',
            'ogin or password incorrect!',
            'NP0lvVds',
            'assword required for sys',
            'scott',
            'assword required for scott',
            'ntering Passive Mode (192,168,21,101,219,204).',
            'li>Users with the <tt>admin-gui</tt> role should not be granted the',
            'guest',
            'moderator',
            'assword required for anonymous',
            'tiger',
            'assword required for system',
            ' whereas FrontPage',
            'onsiders only those people in the local user file to be',
            'rontPage) - instead of LDAP - when handling authorizing the user.</p>',
            'rontPage users will be able to perform all management',
            ' The user ID is ideal for this.</li>',
            ' <li>When adding users via FrontPage, FrontPage administrators',
            ' should choose usernames that already exist in the LDAP',
            ' directory (for obvious reasons). Also, the password that the',
            ' will actually be authenticating against the password in the',
            ' LDAP database, and not against the password in the local user',
            ' files so that it knows where to look for the valid user list. If',
            ' <dt>Per-user web directories</dt>',
            '   to a URL <code>http://example.com/~username/</code> will get content',
            'mozilla@example.com',
            'pass123',
            '_WYIIIIIIIIIIQZVTX30VX4AP0A3HH0A00ABAABTAAQ2AB2BB0BBXP8ACJJIhiiNc2c0c0aMpUhha7c0c0c0pkpeprpnpeplp3p2dnpdplpla0pGpeptpPprpopcaQpdpdprpepspspLpopapdpLpipbprpaprpyaQaMpdlKeMp0c0c0c0lKaKdLk3hCdLk9hZlKaKc4p9h',
            'assword required for moderator',
            'assword required for lala',
            'assword required for dbsnmp',
            'WYIIIIIIIIIIQZVTX30VX4AP0A3HH0A00ABAABTAAQ2AB2BB0BBXP8ACJJIj0j0j0j0j0j0j0j0j0j0lzc0c0j0c0pfk1hJiodOpBpRpjc2pXhMdnelc5pZpthoh8pcp0p0pllKhzlopuhjlopuhgk1hop2dKc0c0iohgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
            'assword required for wyiiiiiiiiiiqzvtx30vx4ap0a3hh0a00abaabtaaq2ab2bb0bbxp8acjjij0j0j0j0j0j0j0j0j0j0lzc0c0j0c0pfk1hjiodopbprpjc2pxhmdnelc5pzpthoh8pcp0p0pllkhzlopuhjlopuhgk1hop2dkc0c0iohgaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'nessus2809318597432367',
            'rapport',
            'ftp',
            'URjCv2Mh',
            'ZW991AzT',
            '912ETEBKSgUX86NocyRFCreoxnDgCHNarCDqmNWvvPk56lECYhhyjdrAOTSruo1ARucY3qITR0YSp12gvhZeBp9It8f0txEtYBwgRvXkABXvJu00c4CXnzA0wvgQjDlEIvTAldWbh3ciIsvQToubUoNloOm6YTwQ4CqWrx36N5iBKwMcIHMIhY3eCl4wGxZLKa6Sdz1w9Nn6GUmgwAld',
            'assword required for 912etebksgux86nocyrfcreoxndgchnarcdqmnwvvpk56lecyhhyjdraotsruo1arucy3qitr0ysp12gvhzebp9it8f0txetybwgrvxkabxvju00c4cxnza0wvgqjdleivtaldwbh3ciisvqtoubuonloom6ytwq4cqwrx36n5ibkwmcihmihy3ecl4wgxz',
            'newuser',
            'ER   PASS   QUIT   CWD    PWD    PORT   PASV   TYPE',
            'ntering Passive Mode (192,168,21,101,163,245).',
            'admin',
            'password',
            'nessus nessus nessus nessus',
            'd</code></dt>',
            '   <dt><code>--with-suexec-userdir</code></dt>',
            ',[<3MdC3h?!goMZ>[{`GsSC@gsdn>^d7b(T1tcB{Fclo8|U-H>l(P>Sa]?@#u,Tj|TE$Z4T-M}BDmROjgjP{X[euNdwNLYYc*v$B@^Si9!!69i@sJ#i|E!C#phNVGC3G_y;NAaLX>Ucj#7uYYN[2b;[2^CWba5?Y$;;{zJdtFH`B?O_K<#}3[?1zVgq1;IO!W-OX,>bAr1)#GN2?Amuw',
            'whatever',
            'Administrator',
            'monitor',
            'NULL',
            'lease log in with USER and PASS first.',
            'nessus@example.com',
            'OQ8tAOry',
            'yRGnSEEn',
            'assword required for yrgnseen',
            'nopvyIRi',
            'bogusbogus',
            'nonymous user logged in.',
            'ntering Passive Mode (192,168,21,103,192,28)',
            '1913008068',
            'd along to lower modules if the UserID is not known to this module</i></tt></dd>',
            'ord',
            'manage',
            'assword required for np0lvvds',
            'p>A bind password to use in conjunction with the bind DN. Note',
            'hat the bind password is probably sensitive data, and should be',
            'ther than the user that starts Apache has write access to the',
            'cjadksrt',
            '   <li>encourages user feedback through new ideas, bug reports and',
            ' It has been tested thoroughly by both developers and users. The Apache',
            ' <dd><p>Apache has an active community of users who are willing to share',
            'assword required for ftp',
            'assword required for nessus2809318597432367',
            'arning: Router with P@SW bug detected. Entering Passive Mode (192,168,28,103,192,12)',
            'assword required for urjcv2mh',
            ' user support issues.</p>',
            ' <p>With millions of users and fewer than sixty volunteer developers,',
            ' SELECT (Host, Db, User, Table_name, Table_priv, Column_priv)',
            'li>Then each of the <i>true</i> users should be granted a set of privileges',
            '   privileges to an ordinary user, unless you understand the impact of those',
            '   privileges (for example, you are creating a superuser).<br />',
            '   For example, to grant the user <i>real_user</i> with all privileges on',
            '   the database <i>user_base</i>:<br />',
            '   What the user may now do is controlled entirely by the MySQL user',
            'li>Obviously, the user must enable cookies in the browser, but this is',
            '   with the same username.</li>',
            'erver under your control. Otherwise users may not be able to contact you in',
            'p>as users do not always mention that they are talking about the',
            'napier',
            'assword required for Administrator.',
            'ser Administrator logged in.',
            'ntering Passive Mode (192,168,47,134,4,54).',
            'ntering Passive Mode (192,168,47,134,4,55).',
            'ntering Passive Mode (192,168,47,134,4,57).',
        ]
        return {
            'command': random.choice(cmd_lst),
            'info': random.choice(info_lst)
        }

    @classmethod
    def _gen_audit_http_record(cls):
        fake = faker.Faker()
        return {
            'url': '{}://{}/blog/{}'.format(
                random.choice(['http', 'https']), fake.ipv4(), fake.name().replace(' ', '-')),
        }

    @classmethod
    def gen_proto_info(cls, proto):
        proto_info_mapping = {
            'ftp': cls._gen_audit_ftp_record(),
            'http': cls._gen_audit_http_record(),
        }
        return proto_info_mapping[proto]

    @classmethod
    def producer_traffic(cls, host='127.0.0.1', port=6379, db=0, num=1000):
        redis_client = cls._con_redis(host, port, db)
        traffic = {
            'proto': 'http',
            'flow_id': str(uuid.uuid4()).replace('-', ''),
            'flow_timestamp': str(int(time.time())),
            'direction': 0,
            'proto_detail': '',
            'packet_length': 0,
            'packet_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        timestamp = int(time.time()) - math.ceil(num / cls.size * 1.0)
        while num > 0:
            timestamp += random.randint(0, 3)
            fake = faker.Faker()
            for _ in range(cls.size):
                _proto_traffic = {}
                _proto_traffic.update(traffic)
                _proto_traffic['flow_timestamp'] = timestamp
                _proto_traffic['proto'] = random.choice(cls.proto)
                if _proto_traffic['flow_id'][-1] != '2':
                    _proto_traffic['flow_id'] = str(uuid.uuid4()).replace('-', '')
                    _proto_traffic['direction'] = random.randint(0, 1)
                _proto_traffic.update(cls.gen_proto_info(_proto_traffic['proto']))
                _proto_traffic['proto_detail'] = fake.name() if random.randint(0, 1) % 2 else fake.address()
                _proto_traffic['packet_length'] = random.randint(1, 1500)
                _proto_traffic['packet_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                redis_client.rpush(cls.queue_key, json.dumps(_proto_traffic))
            else:
                num -= cls.size


if __name__ == '__main__':
    _start = time.time()
    gen_num = 50000
    GenAuditProtoData.producer_traffic(host='192.168.1.189', port=6379, db=0, num=gen_num)
    _end = time.time()
    print('It took {} seconds to generate {} pieces of data'.format(_end - _start, gen_num))
