#!/bin/bash
ETH=$1
while [ -z "$(ifconfig -a | grep $ETH)" ]; do sleep 3s; done;
cat /etc/network/interfaces.d/eth0.cfg | sed s/eth0/$ETH/g > /etc/network/interfaces.d/$ETH.cfg
ifup $ETH
echo "200 out" >> /etc/iproute2/rt_tables
GATEWAY=$(route -n | awk 'FNR == 3 {print $2}')
PRIVATE_IP=$(ifconfig -a | grep -A 1 $ETH | awk 'FNR == 2 { print $2 }' | sed 's/.*://')
ip route add default via $GATEWAY dev $ETH table out
ip rule add from $PRIVATE_IP/32 table out
ip rule add to $PRIVATE_IP/32 table out
ip route flush cache