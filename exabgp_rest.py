#!/usr/bin/env python3

import sys
import web
import requests
import netaddr
import subprocess
import json
from sys import stdout

import pdb

urls = (
    '/announce/(.*)', 'Announce',
    '/withdraw/(.*)', 'Withdraw',
    '/adj-rib/', 'Adj_rib',
    '/neighbor/', 'Neighbor',
    '/status/', 'Status',
)

class MyOutputStream(object):
    def write(self, data):
        # Ignore output
        pass

# web.httpserver.sys.stderr = MyOutputStream()

def verify_ip(ip):
    if not '/' in ip:
        ip = '{0}/32'.format(ip)
    try:
        ip_object = netaddr.IPNetwork(ip)
    except:
        raise web.badrequest('Invalid IP')
    return ip_object 

class BgpPrefix:
    def __init__(self, prefix, action='announce', next_hop='self', attributes={}):
        self.prefix = prefix
        self.action = action
        self.next_hop = next_hop
        self.attributes = attributes

    def get_exabgp_message(self):
        if self.action == 'withdraw':
            exabgp_message = '{0} route {1} next-hop {2}'.format(self.action, self.prefix, self.next_hop)
        else:
            attributes = ''
            for attribute in self.attributes:
                if attribute == 'local-preference':
                    attributes += ' local-preference {0}'.format(self.attributes[attribute])
                elif attribute == 'med':
                    attributes += ' med {0}'.format(self.attributes[attribute])
                elif attribute == 'community':
                    if len(self.attributes[attribute]) > 0:
                        attributes += ' community [ '
                        for community in self.attributes[attribute]:
                            attributes += ' {0}'.format(community)
                        attributes += ' ]'
            exabgp_message = '{0} route {1} next-hop {2}{3}'.format(self.action, self.prefix, self.next_hop, attributes)
        return exabgp_message

class Announce:
    def GET(self, prefix):
        ip = verify_ip(prefix)
        bgp_prefix = BgpPrefix(str(ip), action='announce', attributes=web.input(community=[]))
        p = subprocess.Popen('exabgpcli {0}'.format(bgp_prefix.get_exabgp_message()), shell=True, stdout=subprocess.PIPE)
        return_code = p.wait()
        p.stdout.readlines()
        if return_code == 0:
            return 'OK'
        else:
            raise web.badrequest('Internal Error')

class Withdraw:
    def GET(self, prefix):
        ip = verify_ip(prefix)
        bgp_prefix = BgpPrefix(str(ip), action='withdraw')
        p = subprocess.Popen('exabgpcli {0}'.format(bgp_prefix.get_exabgp_message()), shell=True, stdout=subprocess.PIPE)
        return_code = p.wait()
        p.stdout.readlines()
        if return_code == 0:
            return 'OK'
        else:
            raise web.badrequest('Internal Error')

class Adj_rib:
    def GET(self):
        try:
            p = subprocess.Popen('exabgpcli show adj-rib out extensive', shell=True, stdout=subprocess.PIPE)
            return_code = p.wait()
            if return_code == 0:
                lines = p.stdout.readlines()
                data = []
                count = 0
                for line in lines:
                    line = str(line, 'utf-8').rstrip().split()
                    d = dict()
                    d['id'] = str(count)
                    d['peer'] = line[1]
                    d['peer-as'] = line[7]
                    d['ip'] = line[14]
                    d['next-hop'] = line[16]
                    d['community'] = line[18]
                    data.append(d)
                    count += 1
                web.header('Content-Type', 'application/json')
                return json.dumps({'data':data})
            else:
                raise web.badrequest('Internal Error')
        except Exception as e:
            return web.badrequest('Internal Error')

class Neighbor:
    def GET(self):
        try:
            p = subprocess.Popen('exabgpcli show neighbor summary', shell=True, stdout=subprocess.PIPE)
            return_code = p.wait()
            if return_code == 0:
                lines = p.stdout.readlines()
                if len(lines) > 0: lines.pop(0)
                data = []
                count = 0
                for line in lines:
                    line = str(line, 'utf-8').rstrip().split()
                    d = dict()
                    d['id'] = str(count)
                    d['peer'] = line[0]
                    d['peer-as'] = line[1]
                    d['up_time'] = line[2]
                    d['state'] = line[3]
                    data.append(d)
                    count += 1
                web.header('Content-Type', 'application/json')
                return json.dumps({'data':data})
            else:
                raise web.badrequest('Internal Error')
        except Exception as e:
            return web.badrequest('Internal Error')

class Status:
    def GET(self):
        try:
            p = subprocess.Popen('systemctl is-active exabgp', shell=True, stdout=subprocess.PIPE)
            return_code = p.wait()
            if return_code == 0:
                return 'Running'
            else:
                return 'Failed'
        except Exception as e:
            return web.badrequest('Internal Error')

app = web.application(urls, globals())

if __name__ == '__main__':
    #listen = str(sys.argv[1])
    #port = int(sys.argv[2])
    #web.httpserver.runsimple(app.wsgifunc(), (listen, port))
    web.httpserver.runsimple(app.wsgifunc(), ('0.0.0.0', 8080))
