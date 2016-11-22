#iptables rules for WS

# 1. Delete all existing rules
iptables -F

# 2. Set default chain policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# 3. Allow incoming SSH
iptables -A INPUT -i enp0s9 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o enp0s9 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT

# 4. Allow incoming HTTP connections
iptables -A INPUT -i enp0s9 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o enp0s9 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT

# 5. Allow incoming HTTPS connections
iptables -A INPUT -i enp0s9 -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o enp0s9 -p tcp --sport 443 -m state --state ESTABLISHED -j ACCEPT

# 6. Allow outgoing SSH
iptables -A OUTPUT -o enp0s9 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -i enp0s9 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
