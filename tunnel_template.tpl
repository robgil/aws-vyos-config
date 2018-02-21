# Define virtual tunnel interface
set interfaces vti {{ tun.vti }} address '{{ tun.local_neighbor_ip }}'
set interfaces vti {{ tun.vti }} description 'VPN to {{ tun.vpnid }}'
set interfaces vti {{ tun.vti }} mtu '{{ tun.mtu }}'

# Define site to site peer
set vpn ipsec site-to-site peer {{ tun.remote_ip }} authentication mode 'pre-shared-secret'
set vpn ipsec site-to-site peer {{ tun.remote_ip }} authentication pre-shared-secret '{{ tun.psk }}'
set vpn ipsec site-to-site peer {{ tun.remote_ip }} authentication id {{ tun.local_public_ip }}
set vpn ipsec site-to-site peer {{ tun.remote_ip }} authentication remote-id {{ tun.remote_ip }}
set vpn ipsec site-to-site peer {{ tun.remote_ip }} description 'Tunnel to {{ tun.vpnid }}'
set vpn ipsec site-to-site peer {{ tun.remote_ip }} connection-type initiate
set vpn ipsec site-to-site peer {{ tun.remote_ip }} ike-group 'AWS'
set vpn ipsec site-to-site peer {{ tun.remote_ip }} ikev2-reauth inherit
set vpn ipsec site-to-site peer {{ tun.remote_ip }} local-address '{{ tun.local_ip }}'
set vpn ipsec site-to-site peer {{ tun.remote_ip }} vti bind '{{ tun.vti }}'
set vpn ipsec site-to-site peer {{ tun.remote_ip }} vti esp-group 'AWS'

# Configure BGP neighbors
set protocols bgp 65000 neighbor {{ tun.remote_neighbor_ip }} remote-as '{{ tun.remote_asn }}'
set protocols bgp 65000 neighbor {{ tun.remote_neighbor_ip }} soft-reconfiguration 'inbound'
set protocols bgp 65000 neighbor {{ tun.remote_neighbor_ip }} timers holdtime '{{ tun.hold_time }}'
set protocols bgp 65000 neighbor {{ tun.remote_neighbor_ip }} timers keepalive '10'

