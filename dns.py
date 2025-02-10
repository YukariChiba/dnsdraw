#!/usr/bin/env python

import argparse
import datetime
import sys
import time
import threading
import traceback
import socketserver
import struct
import hashlib
import os.path
import ipaddress
import json
import idna
import string

try:
    from dnslib import *
except ImportError:
    print("Missing dependency dnslib: <https://pypi.python.org/pypi/dnslib>. Please install it with `pip`.")
    sys.exit(2)


class DomainName(str):
    def __getattr__(self, item):
        return DomainName(item + '.' + self)

data_dir = "data/"
data_json = "data.json"
data_meta = {}
try:
    with open(data_json) as f:
        data_meta = json.load(f)
except:
    print("Missing metadata, run process.py to generate it.")
    sys.exit(2)

MAXTTL = 255

D = DomainName("draw.strexp.net.")
NSNAME = "draw.ns.strexp.net"
INFOPAGE = "yukarichiba.github.io"
RD = DomainName("f.7.b.0.7.0.1.b.e.0.a.2.ip6.arpa.")
TTL = 60 * 5
IP = ipaddress.IPv6Address("2a0e:b107:b7f::")

soa_record = SOA(
    mname=D,
    rname=D.admin,
    times=(
        1145141919,  # serial number
        60 * 60 * 1,  # refresh
        60 * 60 * 3,  # retry
        60 * 60 * 24,  # expire
        60 * 60 * 1,  # minimum
    )
)
ns_record = NS(NSNAME)

def dns_response(data):
    request = DNSRecord.parse(data)

    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=0), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    qtype = request.q.qtype
    qt = QTYPE[qtype]

    if qn == D and qt in ["CNAME", "AAAA", "A"]:
        reply.add_answer(RR(rname=qname, rtype=QTYPE.CNAME, rclass=1, ttl=TTL, rdata=CNAME(INFOPAGE)))

    if qn in [RD, D] and qt in ["NS"]:
        reply.add_answer(RR(rname=qn, rtype=QTYPE.NS, rclass=1, ttl=TTL, rdata=ns_record))

    if qn in [RD, D] and qt in ["SOA"]:
        reply.add_answer(RR(rname=qn, rtype=QTYPE.SOA, rclass=1, ttl=TTL, rdata=soa_record))
        return reply.pack()

    if qn.endswith('.' + D) and qt in ["AAAA"]:
        if qn.endswith('.' + D.hash):
            query = qn.removesuffix('.' + D.hash)
            if not all(c in string.hexdigits for c in query) or len(query) != 18:
                return reply.pack()
            hashedid = query
        else:
            query = qn.removesuffix('.' + D)
            hashedid = hashlib.shake_256(query.encode('UTF-8')).hexdigest(9)
        if hashedid in data_meta:
            resolvedIP = IP + (int(hashedid, 16)<<8) + data_meta[hashedid]["lines"] + 1
            reply.add_answer(RR(rname=qname, rtype=QTYPE.AAAA, rclass=1, ttl=TTL, rdata=AAAA(str(resolvedIP))))
        return reply.pack()

    if qn.endswith('.' + RD) and qt in ["PTR"]:
        eachbit = qn.removesuffix('.ip6.arpa.').split('.')
        if len(eachbit) != 32:
            return reply.pack()
        eachbit = list(reversed(eachbit))
        query = ':'.join([ ''.join(eachbit[i:i+4]) for i in range(len(eachbit)) if i%4 == 0 ])
        try:
            queryaddress = ipaddress.IPv6Address(query)
        except:
            return reply.pack()
        hashedid = (int(queryaddress) - int(IP))>>8
        hashhex = format(hashedid, 'x').zfill(18)
        rownum = int(queryaddress) & 0xff
        if hashhex in data_meta:
            ptrdata = None
            if rownum == 0 or rownum == data_meta[hashhex]["lines"] + 1:
                ptrdata = data_meta[hashhex]["title"]
            else:
                try:
                    with open('data/' + hashhex + ".txt") as f:
                        for i, line in enumerate(f):
                            if i == rownum - 1:
                                ptrdata = line.removesuffix('\n')
                except:
                    pass
            if ptrdata:
                reply.add_answer(RR(rname=qname, rtype=QTYPE.PTR, rclass=1, ttl=TTL, rdata=PTR(idna.encode(ptrdata))))
        return reply.pack()

    return reply.pack()


class BaseRequestHandler(socketserver.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("\n\n%s request %s (%s %s):" % (self.__class__.__name__[:3], now, self.client_address[0],
                                               self.client_address[1]))
        try:
            data = self.get_data()
            respdata = dns_response(data)
            self.send_data(respdata)
        except Exception:
            traceback.print_exc(file=sys.stderr)


class UDPRequestHandler(BaseRequestHandler):

    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)

class ThreadingUDPServer6(socketserver.ThreadingUDPServer):
    address_family = socket.AF_INET6


def main():
    s = ThreadingUDPServer6((str(IP), 53), UDPRequestHandler)
    thread = threading.Thread(target=s.serve_forever)  # that thread will start one more thread for each request
    thread.daemon = True  # exit the server thread when the main thread terminates
    thread.start()

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        s.shutdown()

if __name__ == '__main__':
    main()
