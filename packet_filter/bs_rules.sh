#iptables rules for BS

# 1. Delete all existing rules
iptables -F

# 2. Set default chain policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# 3. Allow incoming SSH
iptables -A INPUT -i enp0s8 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o enp0s8 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
