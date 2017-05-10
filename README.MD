[![Build Status](https://travis-ci.org/mab27/st2_vyatta.svg?branch=master)](https://travis-ci.org/mab27/st2_vyatta)

# StackStorm automation pack for Brocade vyatta vRouter

## Content of the pack:
- This pack contains simple actions and workflows to interact with the Brocade 5600 vRouter including: interfaces mgmt, routing, Firewalling (ACLs) and IPSec.
- Action runner for the different actions is ```python-script``` which generates REST calls to the device.
- This pack has been written based on the Brocade Vyatta Network OS configuration manuals: 
	- [Brocade Vyatta Network OS Remote Access API Reference Guide, 5.1R1](http://www.brocade.com/content/html/en/vyatta-network-os/51r1/vyatta-network-os-5.1r1-remote-access-api/GUID-430E8A44-1953-4C40-8E2D-AB65F0B24561-homepage.html)
	- [Brocade Vyatta Network OS LAN Interfaces Configuration Guide, 5.1R1](http://www.brocade.com/content/html/en/vyatta-network-os/51r1/vyatta-network-os-5.1r1-laninterface/GUID-DFF91D76-3A69-4E8A-935C-F63C60A766F9-homepage.html)
	- [Brocade Vyatta Network OS Basic Routing Configuration Guide, 5.1R1](http://www.brocade.com/content/html/en/vyatta-network-os/51r1/vyatta-network-os-5.1r1-basic-routing/GUID-3414F714-E8F9-4646-903C-11D66E078C2A-homepage.html)
	- [Brocade Vyatta Network OS BGP Configuration Guide, 5.2R1](http://www.brocade.com/content/html/en/vyatta-network-os/5.2r1/vyatta-network-os-5.2r1-bgp/GUID-3CD25159-4EF0-41D5-93F8-89D01B2CF3C3.html)
	- [Brocade Vyatta Network OS Firewall Configuration Guide, 5.2R1](http://www.brocade.com/content/html/en/vyatta-network-os/5.2r1/vyatta-network-os-5.2r1-firewall/GUID-9F0DAD54-7F7E-472B-A62F-8BCF4254707C-homepage.html)
- For information on StackStorm:
	- [Documentation](https://docs.stackstorm.com/overview.html) 
	- [Video-StackStorm-101](https://www.youtube.com/watch?v=CwEzO_f-q3s&t=907s)

## Before using the pack:
- Save the vyatta router credentials in the K/V store. You can do that via the cli command ```st2 key set``` or using the action from the ```st2``` pack.
- Below an example for two vyatta devices, with ip addresses 192.168.0.10 and 192.168.0.20.
```
st2 run st2.kv.set key=192.168.0.10_user value=vyatta 
st2 run st2.kv.set key=192.168.0.20_user value=vyatta 
st2 run st2.kv.set key=192.168.0.10_pswd value=vyatta 
st2 run st2.kv.set key=192.168.0.20_pswd value=vyatta
```
- Check the K/V Store
```
st2 key list
```

## Actions & Workflows:

- Configuration:
	- cfg_interface 	/ 	del_interface
	- cfg_ip_route 		/ 	del_ip_route
	- cfg_ebgp 			/ 	del_ebgp
	- cfg_bgp_adv_prefix / 	del_bgp_adv_prefix
	- cfg_ipsec 		/ 	del_ipsec
	- cfg_fw_rule 		/ 	del_fw_rule
	- cfg_fw_instance 	/ 	del_fw_instance

- Validation:
	- show_interfaces
	- show_ip_route
	- show_bgp_sum
	- show_bgp_neighbors
	- show_fw
	- show_vpn_ipsec_status
	- show_vpn_ipsec_sa
	- ping

- Device's information:
	- show_version
	- show_history
	- show_system_commit
	- show_system_memory

### Examples:
- Interface management:
```
st2 run vyatta.show_interfaces deviceIP=192.168.0.10

st2 run vyatta.cfg_interface deviceIP=192.168.0.10 intfType=loopback intfNum=lo5 address=192.168.75.5/32

st2 run vyatta.del_interface deviceIP=192.168.0.10 intfType=loopback intfNum=lo5
```
- Static routing:
```
st2 run vyatta.show_ip_route deviceIP=192.168.0.10

st2 run vyatta.cfg_ip_route deviceIP=192.168.0.10 subnet=10.10.10.0/24 nextHop=172.16.0.20

st2 run vyatta.del_ip_route deviceIP=192.168.0.10 subnet=10.10.10.0/24
```
- BGP Routing:
```
st2 run vyatta.cfg_ebgp eastDeviceIP=192.168.0.10 eastASN=65010 eastPeeringIP=172.16.0.10 westDeviceIP=192.168.0.20 westASN=65020 westPeeringIP=172.16.0.20

st2 run vyatta.show_ip_bgp_sum deviceIP=192.168.0.10

st2 run vyatta.show_ip_bgp_neighbors deviceIP=192.168.0.10

st2 run vyatta.cfg_bgp_adv_prefix deviceIP=192.168.0.10 localAS=65010 prefix="10.10.10.0/24","20.20.20.0/24","30.30.30.0/24"

st2 run vyatta.del_bgp_adv_prefix deviceIP=192.168.0.10 localAS=65010 prefix="10.10.10.0/24","30.30.30.0/24"

st2 run vyatta.del_bgp deviceIP=192.168.0.10
```
- Firewall:
```
st2 run vyatta.cfg_fw_rule deviceIP=192.168.0.10 fw_instance_name=fw-1 rule_number=1 rule_content='{"action": "accept", "state": "enable","protocol": "tcp", "dst_addr": "172.60.10.0/24","dst_port": "80", "src_addr": "10.10.10.0/8"}'

st2 run vyatta.cfg_fw_rule deviceIP=192.168.0.10 fw_instance_name=fw-1 rule_number=2 rule_content='{"action": "accept", "state": "enable","protocol": "tcp", "dst_addr": "172.60.10.0/24","dst_port": "80", "src_addr": "20.20.20.0/8"}'

st2 run vyatta.del_fw_rule deviceIP=192.168.0.10 fw_instance_name=fw-1 rule_number=2

st2 run vyatta.cfg_fw_instance deviceIP=192.168.0.10 intfNum=dp0p38p1 fw_instance_name=fw-1 direction=in

st2 run vyatta.show_fw deviceIP=192.168.0.10

st2 run vyatta.del_fw_instance deviceIP=192.168.0.10 intfNum=dp0p38p1 fw_instance_name=fw-1 direction=in
```
- IPSec (Site-to-site only, pre-shared-key only):
```
st2 run vyatta.cfg_ipsec eastDeviceIP=192.168.0.10 eastTunnelIP=172.16.0.10 eastPrefix=10.10.10.10/32 westDeviceIP=192.168.0.20 westTunnelIP=172.16.0.20 westPrefix=20.20.20.20/32

st2 run vyatta.show_vpn_ipsec_status deviceIP=192.168.0.10

st2 run vyatta.show_vpn_ipsec_sa deviceIP=192.168.0.10

st2 run vyatta.del_vpn_ipsec deviceIP=192.168.0.10
```
- Validation:
```
st2 run vyatta.ping deviceIP=192.168.0.10 targetIP=172.16.0.20
```
- Device's information:
```
st2 run vyatta.show_version deviceIP=192.168.0.10

st2 run vyatta.show_system_commit deviceIP=192.168.0.10

st2 run vyatta.show_system_memory deviceIP=192.168.0.10

st2 run vyatta.show_history deviceIP=192.168.0.10
```

## Rules:

### Webhooks: 
- **webhook_cfg_interface**: From Webhook payload, fire the action to configure an interface.
- **webhook_del_interface**: From Webhook payload, fire the action to delete an  interface.

- **webhook_cfg_ip_route**: From Webhook payload, fire the action to configure an ip route.
- **webhook_del_ip_route**: From Webhook payload, fire the action to delete an ip route.

- **webhook_cfg_ebgp**: From Webhook payload, fire the action to configure an ebgp peering.
- **webhook_del_ebgp**: From Webhook payload, fire the action to delete an ebgp peering.
- **webhook_cfg_bgp_adv_prefix**: From Webhook payload, fire the action to configure an bgp prefix advertisement.
- **webhook_del_bgp_adv_prefix**: From Webhook payload, fire the action to delete an bgp prefix advertisement.

- **webhook_cfg_fw_rule**: From Webhook payload, fire the action to configure a FW rule.
- **webhook_del_fw_rule**: From Webhook payload, fire the action to delete a FW rule.
- **webhook_cfg_fw_instance**: From Webhook payload, fire the action to apply a FW instance.
- **webhook_del_fw_instance**: From Webhook payload, fire the action to remove a FW instance.

- **webhook_cfg_ipsec**: From Webhook payload, fire the action to configure an ipsec tunnel.
- **webhook_del_ipsec**: From Webhook payload, fire the action to delete an ipsec tunnel.

### What are Webhooks: 
- Systems that push data to the ST2 API when an event you are interested in occurs.
- Webhooks come handy is when you want to consume events from a 3rd party service which already offer webhooks integration - e.g. GitHub
- Webhooks aren't directly created --> they're created via rules.

The rules in this pack are written using one of the default triggers: ```core.st2.webhook``` --> This means that the rule will be watching for incoming events that are in the form of a custom webhook.

POST-ing data to a custom webhook will cause a trigger with the following attributes to be dispatched:
- **trigger** - Trigger name.
- **trigger.headers** - Dictionary containing the request headers.
- **trigger.body** - Dictionary containing the request body.

These allows the rule to check if the event matches any of its criteria, if yes, then the corresponding action/workflow will be fired.

### Pre-requisistes (Before trying rules):
- Make sure the rules are registered and available by list the available rules for the pack:
```
st2 rule list -p vyatta
```
- If needed, restart the rules service:
```
sudo st2ctl restart --register-rules
```
- Obtain an authentication token. You'll need it to replace **$TOKEN** in the cURL commands below:
```
st2 auth login -p password
```

### Usefull commands to verify rules enforcement and actions/workflows executions:
- Check the latest rules enforced:
```
st2 rule-enforcement list -n 5
```
- Check the details of the emitted trigger  (obtain **trigger_id** from previous command):
```
st2 trigger-instance get **trigger_id**
```
- Check the latest actions/workflows executed:
```
st2 execution list -n 5
```

### Examples:

- Trigger the **cfg_ip_route** rule:
send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d '{"task":"cfg_ip_route","deviceIP":"192.168.0.10","subnet":"70.70.70.0/24","nextHop":"172.16.0.20"}' http://localhost:9101/v1/webhooks/vrouter
```

- Trigger the **del_ip_route** rule:
send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d '{"task":"del_ip_route","deviceIP":"192.168.0.10","subnet":"70.70.70.0/24"}' http://localhost:9101/v1/webhooks/vrouter
```

- Trigger the **cfg_ebgp** rule:
send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d '{"task":"cfg_ebgp","eastDeviceIP":"192.168.0.10","eastASN":"65010","eastPeeringIP":"172.16.0.10", "westDeviceIP":"192.168.0.20","westASN":"65020","westPeeringIP":"172.16.0.20"}' http://localhost:9101/v1/webhooks/vrouter
```

- Trigger the **del_bgp** rule:
send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d '{"task":"del_bgp","deviceIP":"192.168.0.10"}' http://localhost:9101/v1/webhooks/vrouter
```

- Trigger the **cfg_fw_rule** rule:

First create a file ```body_cfg_fw_rule_1_1.json```:
```
{
    "task": "cfg_fw_rule",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw-1",
    "rule_number": "1",
    "rule_filter": {
    	"action": "accept",
    	"state": "enable",
    	"protocol": "tcp",
    	"dst_addr": "172.60.10.0/24",
    	"dst_port": "80", 
    	"src_addr": "10.10.10.0/8"
    }
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_cfg_fw_rule_1_1.json http://localhost:9101/v1/webhooks/vrouter
```

- Trigger again the **cfg_fw_rule** rule:

First create a file ```body_cfg_fw_rule_1_2.json```:
```
{
    "task": "cfg_fw_rule",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw-1",
    "rule_number": "2",
    "rule_filter": {
        "action": "accept",
        "state": "enable",
        "protocol": "tcp",
        "dst_addr": "172.60.10.0/24",
        "dst_port": "80", 
        "src_addr": "10.10.10.0/8"
    }
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_cfg_fw_rule_1_2.json http://localhost:9101/v1/webhooks/vrouter
```

- Trigger the **del_fw_rule** rule:

First create a file ```body_del_fw_rule_1_2.json```:
```
{
    "task": "cfg_fw_rule",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw_1",
    "rule_number": "1"
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_del_fw_rule_1_2.json http://localhost:9101/v1/webhooks/vrouter
```

- Trigger the **apply_fw_instance** rule:

First create a file ```body_cfg_fw_instance_1.json```:
```
{
    "task": "apply_fw_instance",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw-1",
    "intfNum": "dp0p38p1",
    "direction": "out"
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_cfg_fw_instance_1.json http://localhost:9101/v1/webhooks/vrouter
```
- Trigger the **remove_fw_instance** rule:

First create a file ```body_del_fw_instance_1.json```:
```
{
    "task": "remove_fw_instance",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw-1",
    "intfNum": "dp0p38p1",
    "direction": "out"
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_del_fw_instance_1.json http://localhost:9101/v1/webhooks/vrouter
```

## ChatOps:
### What is Chatops:
- It is about humans talking to ChatBots (and the other way around).
- A more formal definition would be the concept of delegating responsibility of tasks/actions to an internal robot that also sits inline with your existing company.
- Simply put, ChatOps let you take operational and development workflows and expose them as commands that can be executed in a company chat room.
- The benefits are numerous: Shared CLI to help for incident management, enable team scaling by allowing automation consumable in a easy way by every team member (Makes everyone more powerfull) etc ...

### ChatOps in this pack:
- StackStorm facilitates the introduction of ChatOps in your organisation by diffeent integrations with pupular chat tools and bots.
- Any action/workflow you want to expose in a chatroom will have an action-alias, in the ```aliases``` folder.
- The demo in this pack has been realised using Slack as a chat tool and Hu-Bot as a bot. 

### Examples:
Before trying any conversation with your bot, check its online presence in the chatroom, the bot must appear on-line to be able to communicate with ST2.
And also type in the two following commands to restart the ChatOps service, this is often required every time you reconnect to you chatroom:
```
st2ctl reload --register-aliases
sudo service st2chatops restart
```
- Show the firewall config on a device, type this in the chatroom:
```
!show fw on 192.168.0.10  
```