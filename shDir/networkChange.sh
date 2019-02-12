#!/bin/bash

#spark-network remove
sudo docker network rm spark-network

#

sudo ip link add link enp3s0 mactest type macvlan mode bridge
sudo ip address add 10.0.120.5 dev mactest
sudo ip link set dev mactest up

sudo ip route flush dev enp3s0
sudo ip route flush dev mactest

#route
sudo ip route add 10.0.0.0/16 dev mactest metric 0

#gateway
sudo ip route add default via 10.0.0.1

#spark-network create
sudo docker network create -d macvlan -o macvlan_mode=bridge --subnet=10.0.0.0/16 --gateway=10.0.0.1 -o parent=mactest spark-network

