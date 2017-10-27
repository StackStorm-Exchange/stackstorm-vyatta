import requests
import warnings
import json
from st2client.client import Client
from st2common.runners.base_action import Action


class InternalCfgFwRule(Action):
    def run(self, deviceIP, cmd_path, fw_instance_name,
            rule_number, rule_content):

        cmd_path = cmd_path[:26]
        rule_number = str(rule_number)

        # Fetching device credentials based on keys derived from deviceIP
        #################################################################
        user_key_name = deviceIP + "_user"
        pswd_key_name = deviceIP + "_pswd"
        print "\n"
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print "Looking for credentials in KV store"
        client = Client()
        try:
            user = (client.keys.get_by_name(user_key_name)).value
            pswd = (client.keys.get_by_name(pswd_key_name)).value
            print "     Obtained from KV store: user = " + user
            print "     Obtained from KV store: pswd = " + pswd
        except:
            return (False, "No credentials for : " + deviceIP)

        # Preapring the URL request(s)
        #################################################################
        h = {
            "accept": "application/json",
            "content-length": "0"
        }

        url_0 = "https://" + deviceIP + "/" + cmd_path
        url_1 = "/set/security/firewall/name/" + fw_instance_name
        url_2 = "/rule/" + rule_number
        url_base = url_0 + url_1 + url_2

        url_list = list()

        # Fetching content of 'rule_filter' object and build URL calls list
        #################################################################
        if 'action' in rule_content:
            action = rule_content['action']
            url = url_base + "/action/" + action
            url_list.append(url)

        if 'state' in rule_content:
            state = rule_content['state']
            url = url_base + "/state/" + state
            url_list.append(url)

        if 'src_addr' in rule_content:
            src_addr = rule_content['src_addr'].replace("/", "%2F")
            url = url_base + "/source/address/" + src_addr
            url_list.append(url)

        if 'src_port' in rule_content:
            try:
                protocol = rule_content['protocol']
            except:
                print "protocol required in filter_list parameter"

            url = url_base + "/protocol/" + protocol
            url_list.append(url)
            src_port = rule_content['src_port']
            url = url_base + "/source/port/" + src_port
            url_list.append(url)

        if 'dst_addr' in rule_content:
            dst_addr = rule_content['dst_addr'].replace("/", "%2F")
            url = url_base + "/destination/address/" + dst_addr
            url_list.append(url)

        if 'dst_port' in rule_content:
            try:
                protocol = rule_content['protocol']
            except:
                print "protocol required in filter_list parameter"

            url = url_base + "/protocol/" + protocol
            url_list.append(url)
            dst_port = rule_content['dst_port']
            url = url_base + "/destination/port/" + dst_port
            url_list.append(url)

        # Sending the URL call(s)
        #################################################################
        print "Sending REST call(s):"
        for u in url_list:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                print "     PUT            " + u
                r = requests.put(u, auth=(user, pswd), headers=h, verify=False)
                r_code = str(r.status_code)
                print "     Response code:   " + r_code
                cmd_response_code = int(r.status_code)
                if cmd_response_code != 200:
                    return (False, cmd_response_code)
                else:
                    try:
                        data = json.loads(r.text)
                        print "     Response body: "
                        print json.dumps(data, sort_keys=True, indent=4)
                    except:
                        print "     Response body: empty"
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
