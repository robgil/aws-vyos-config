# aws-vyos-config
Script to help generate the tunnel configurations on [VyOS](https://vyos.io/). The script also uses jinja
templates to make it easy to update for your specific needs and environments.

```
$ ./getconfig.py -h
usage: getconfig.py [-h] -p PROFILE --id VPNID --vti VTI --localip LOCALIP
                    [--ipsec]

optional arguments:
  -h, --help         show this help message and exit
  -p PROFILE         AWS Profile
  --id VPNID         VPN ID
  --vti VTI          Virtual Tunnel Interface
  --localip LOCALIP  Local IP used for the tunnel. Use the RFC1918 address if
                     doing NAT Traversal
  --ipsec            Additionally dump the ipsec configuration
```

# Requirements
Written in Python 3.6 but could probably be adapted for earlier versions.

# Install
Basic virtualenv install
```
virtualenv -p python3 aws-vyos-config
cd aws-vyos-config/
. bin/activate
pip install -r requirements.txt
```

# Example
```
./getconfig.py -p <my aws profile> --id vpn-123abc456> --vti vti0 --localip 10.255.0.4
```

*Sample Output*
```
set interfaces vti vti0 address '169.254.47.22/30'
set interfaces vti vti0 description 'VPN to vpn-123abc456'
set interfaces vti vti0 mtu '1436'

set vpn ipsec site-to-site peer 35.168.100.100 authentication mode 'pre-shared-secret'
set vpn ipsec site-to-site peer 35.168.100.100 authentication pre-shared-secret
'my super secure psk provided by aws'
set vpn ipsec site-to-site peer 35.168.100.100 description 'Tunnel to vpn-123abc456'
set vpn ipsec site-to-site peer 35.168.100.100 ike-group 'AWS'
set vpn ipsec site-to-site peer 35.168.100.100 local-address '10.255.0.4'
set vpn ipsec site-to-site peer 35.168.100.100 vti bind 'vti0'
set vpn ipsec site-to-site peer 35.168.100.100 vti esp-group 'AWS'

set protocols bgp 65000 neighbor 169.254.47.21/30 remote-as '64600'
set protocols bgp 65000 neighbor 169.254.47.21/30 soft-reconfiguration 'inbound'
set protocols bgp 65000 neighbor 169.254.47.21/30 timers holdtime '30'
set protocols bgp 65000 neighbor 169.254.47.21/30 timers keepalive '10'

set interfaces vti vti0 address '169.254.47.86/30'
set interfaces vti vti0 description 'VPN to vpn-123abc456'
set interfaces vti vti0 mtu '1436'

set vpn ipsec site-to-site peer 34.235.100.100 authentication mode 'pre-shared-secret'
set vpn ipsec site-to-site peer 34.235.100.100 authentication pre-shared-secret
'my super secret psk provided by aws'
set vpn ipsec site-to-site peer 34.235.100.100 description 'Tunnel to vpn-123abc456'
set vpn ipsec site-to-site peer 34.235.100.100 ike-group 'AWS'
set vpn ipsec site-to-site peer 34.235.100.100 local-address '10.255.0.4'
set vpn ipsec site-to-site peer 34.235.100.100 vti bind 'vti0'
set vpn ipsec site-to-site peer 34.235.100.100 vti esp-group 'AWS'

set protocols bgp 65000 neighbor 169.254.47.85/30 remote-as '64600'
set protocols bgp 65000 neighbor 169.254.47.85/30 soft-reconfiguration 'inbound'
set protocols bgp 65000 neighbor 169.254.47.85/30 timers holdtime '30'
set protocols bgp 65000 neighbor 169.254.47.85/30 timers keepalive '10'
```

# Testing
Will accept PRs!

# Development
If you'd like to contribute, the following may help.

```
aws --profile <your ~/.aws/credentials profile> ec2 describe-vpn-connections
```
_the important part in here is `CustomerGatewayConfiguration` which is the configuration in XML format_
