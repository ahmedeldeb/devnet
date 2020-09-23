from netmiko import ConnectHandler
cisco = {
   'device_type': 'cisco_ios',
   'host': input("router ip add:"),
   'username': 'admin',
   'password': 'cisco123',
   }
net_connect = ConnectHandler(**cisco)
config_commands = ['crypto isakmp policy 1',
                   ' encr 3des',
                   'hash md5',
                   'authentication pre-share',
                   'group 2',
                   'lifetime 86400']
output = net_connect.send_config_set(config_commands)
print(output)
i= input("whats your preshared key:")
p= input("whats destination ip address:")
config_commands = ['crypto isakmp key ' +i+' addr '+p]
output = net_connect.send_config_set(config_commands)
print(output)
print('CREATING EXTENDED ACL: VPN-TRAFFIC ')
l = input("enter networks with widecard mask :")
config_commands = [
   'ip access-list extended VPN-TRAFFIC',
   'permit ip '+l
]
output = net_connect.send_config_set(config_commands)
print(output)
print('CREATE IPSEC TRANSFORM (ISAKMP PHASE 2 POLICY):TS')
config_commands = ['crypto ipsec transform-set TS esp-3des esp-md5-hmac']
output = net_connect.send_config_set(config_commands)
print(output)
print('STEP 3: CREATE CRYPTO MAP:CMAP')
config_commands = ['crypto map CMAP 10 ipsec-isakmp',
                   ' set peer ' + p,
                   'set transform-set TS',
                   'match address VPN-TRAFFIC',
                   ]
output = net_connect.send_config_set(config_commands)
print(output)
print('APPLY CRYPTO MAP TO THE PUBLIC INTERFACE')
c= input("set ipsec router interface:")
config_commands = [
   'interface '+c,
   'crypto map CMAP'
]
output = net_connect.send_config_set(config_commands)
print(output)
output = net_connect.send_command("show run ")
print(output)
