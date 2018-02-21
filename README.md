# aws-vyos-config
Script to help generate the tunnel configurations on [VyOS](https://vyos.io/). The script also uses jinja
templates to make it easy to update for your specific needs and environments.

```
$ ./getconfig.py -h
usage: getconfig.py [-h] -p PROFILE --id VPNID --vti VTI [VTI ...] --localip
                    LOCALIP [--ipsec]

optional arguments:
  -h, --help           show this help message and exit
  -p PROFILE           AWS Profile
  --id VPNID           VPN ID
  --vti VTI [VTI ...]  Virtual Tunnel Interface (list separated by space)
  --localip LOCALIP    Local IP used for the tunnel. Use the RFC1918 address
                       if doing NAT Traversal
  --ipsec              Additionally dump the ipsec configuration
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
./getconfig.py -p <my aws profile> --id vpn-123abc456> --vti vti0 vti1 --localip 10.255.0.4
```
_Note the two vti devices are required. One for each tunnel._

# Testing
Will accept PRs!

# Development
If you'd like to contribute, the following may help.

```
aws --profile <your ~/.aws/credentials profile> ec2 describe-vpn-connections
```
_the important part in here is `CustomerGatewayConfiguration` which is the configuration in XML format_
