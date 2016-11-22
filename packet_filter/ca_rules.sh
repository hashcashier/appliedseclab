#iptables rules for CA

# 1. Delete all existing rules
iptables -F

# 2. Set default chain policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# 3. Allow incoming SSH
iptables -A INPUT -i enp0s8 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o enp0s8 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT

# 4. Allow incoming CA connections from the Web Server
iptables -A INPUT -i enp0s8 -p tcp -s 192.168.2.173 --dport 8888 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o enp0s8 -p tcp -d 192.168.2.173 --sport 8888 -m state --state ESTABLISHED -j ACCEPT

# 5. Allow outgoing SSH
iptables -A OUTPUT -o enp0s8 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -i enp0s8 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
