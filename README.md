# arp-spoofer
Python script that intercept network data using ARP spoofing.

## Prerequisites

- [Python 3 installed](https://www.python.org/downloads/)

## Getting started
To enable IP forwarding on Linux:

```
# echo 1 > /proc/sys/net/ipv4/ip_forward
```

To use this script go to the root project folder and run following command:

```
python3 arp_spoofer.py -t TARGET_IP -g GATEWAY_IP
```

Where `TARGET_IP` is the target machine IP and `GATEWAY_IP` is the router IP address.
