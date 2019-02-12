#!/bin/bash

#spark-network remove
sudo docker network rm spark-network

#

sudo ip link add link wlp4s0 mactest2 type macvlan mode bridge
sudo ip address add 172.30.24.28 dev mactest2
sudo ip link set dev mactest2 up

sudo ip route flush dev wlp4s0
sudo ip route flush dev mactest2

#route
sudo ip route add 172.0.0.0/12 dev mactest2 metric 0

#gateway
sudo ip route add default via 172.30.1.254

#spark-network create
sudo docker network create -d macvlan -o macvlan_mode=bridge --subnet=172.0.0.0/12 --gateway=172.30.1.254 -o parent=mactest2 spark-network

