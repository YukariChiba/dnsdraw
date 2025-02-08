import sys
from netfilterqueue import NetfilterQueue
from scapy.all import IPv6, ICMPv6TimeExceeded, send
from scapy.sendrecv import __gen_send  # `send` is fucking slow!
from scapy.config import conf
from ipaddress import IPv6Address

socket = conf.L3socket()
ifaceout="gri-sol1"

conf.route6.add("::/0", dev=ifaceout)

baseaddr = IPv6Address('2a0e:b107:b7f::')
MAX_LEN = 256

def handle(inpkt):
    pkt = IPv6(inpkt.get_payload())
    dstaddr = IPv6Address(pkt.dst)
    group = (int(dstaddr)-int(baseaddr))>>8
    set_len = (int(dstaddr) & 0xff)
    max_len = max(set_len, MAX_LEN)
    hlim = pkt.hlim
    if hlim < max_len:
        inpkt.drop()
        sendsrc = baseaddr + (group<<8) + hlim - 1
        tosend = IPv6(src=str(sendsrc), dst=pkt.src) / ICMPv6TimeExceeded() / pkt
        __gen_send(socket, tosend)
    else:
        inpkt.drop()
        sendsrc = dstaddr
        tosend = IPv6(src=str(sendsrc), dst=pkt.src) / ICMPv6TimeExceeded() / pkt
        __gen_send(socket, tosend)


if __name__ == '__main__':
    queue = 1
    if len(sys.argv) > 1:
        queue = int(sys.argv[1])

    print('Binding queue', queue)

    nfqueue = NetfilterQueue()
    nfqueue.bind(queue, handle)
    try:
        print('Listening...')
        nfqueue.run()
    except KeyboardInterrupt:
        pass

