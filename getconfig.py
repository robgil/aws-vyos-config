#!/usr/bin/env python3
import os
import boto3
import argparse
import traceback
import pprint
#import xml.etree.ElementTree as xml
import untangle
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser()
parser.add_argument("-p",
                    help="AWS Profile",
                    dest="profile",
                    required=True,
                    action="store",
                    default=[])
parser.add_argument("--id",
                    help="VPN ID",
                    dest="vpnid",
                    required=True,
                    action="store",
                    default=[])
parser.add_argument("--vti",
                    help="Virtual Tunnel Interface",
                    dest="vti",
                    required=True,
                    action="store",
                    default=[])
parser.add_argument("--localip",
                    help="Local IP used for the tunnel. Use the RFC1918 address if doing NAT Traversal",
                    dest="localip",
                    required=True,
                    action="store",
                    default=[])
parser.add_argument("--ipsec",
                    help="Additionally dump the ipsec configuration",
                    dest="ipsec",
                    required=False,
                    action="store_true")


args = parser.parse_args()


try:
    session = boto3.Session(profile_name=args.profile)
    ec2 = session.client('ec2')
    vpns = ec2.describe_vpn_connections(VpnConnectionIds=[args.vpnid])
    config_xml = vpns['VpnConnections'][0]['CustomerGatewayConfiguration']
    #pprint.pprint(config_xml)
    obj = untangle.parse(config_xml)
    vpnid = obj.vpn_connection['id']

    tun1 = obj.vpn_connection.ipsec_tunnel[0]
    tun2 = obj.vpn_connection.ipsec_tunnel[1]

    tun1 = {
        'vpnid': vpnid,
        'vti': args.vti,
        'local_ip': args.localip,
        'mtu': 1436,
        'psk': tun1.ike.pre_shared_key.cdata,
        'remote_ip': tun1.vpn_gateway.tunnel_outside_address.ip_address.cdata,
        'local_public_ip': tun1.customer_gateway.tunnel_outside_address.ip_address.cdata,
        'local_neighbor_ip': tun1.customer_gateway.tunnel_inside_address.ip_address.cdata + '/' + \
                tun1.customer_gateway.tunnel_inside_address.network_cidr.cdata,
        'remote_neighbor_ip': tun1.vpn_gateway.tunnel_inside_address.ip_address.cdata + '/' + \
                tun1.vpn_gateway.tunnel_inside_address.network_cidr.cdata,
        'remote_asn': tun1.vpn_gateway.bgp.asn.cdata,
        'hold_time': tun1.vpn_gateway.bgp.hold_time.cdata,
        }
    tun2 = {
        'vpnid': vpnid,
        'vti': args.vti,
        'local_ip': args.localip,
        'mtu': 1436,
        'psk': tun2.ike.pre_shared_key.cdata,
        'remote_ip': tun2.vpn_gateway.tunnel_outside_address.ip_address.cdata,
        'local_public_ip': tun2.customer_gateway.tunnel_outside_address.ip_address.cdata,
        'local_neighbor_ip': tun2.customer_gateway.tunnel_inside_address.ip_address.cdata + '/' + \
                tun2.customer_gateway.tunnel_inside_address.network_cidr.cdata,
        'remote_neighbor_ip': tun2.vpn_gateway.tunnel_inside_address.ip_address.cdata + '/' + \
                tun2.vpn_gateway.tunnel_inside_address.network_cidr.cdata,
        'remote_asn': tun2.vpn_gateway.bgp.asn.cdata,
        'hold_time': tun2.vpn_gateway.bgp.hold_time.cdata,
        }


    template_path = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_path), trim_blocks=True)
    print(env.get_template('tunnel_template.tpl').render(tun=tun1))
    print(env.get_template('tunnel_template.tpl').render(tun=tun2))
    if args.ipsec == True:
        print(env.get_template('ipsec_template.tpl').render())

except Exception as e:
    print(e, traceback.print_exc())
