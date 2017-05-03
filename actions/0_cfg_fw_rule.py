import requests
import warnings
import json

from st2client.client import Client
from st2client.models import KeyValuePair

from st2actions.runners.pythonrunner import Action

class InternalCfgFwRule(Action):
    def run(self, deviceIP, cmd_path, fw_instance_name, rule_number, rule_content):
        
        # Fetching device credentials based on keys derived from deviceIP 
        #################################################################
        user_key_name = deviceIP + "_user"
        pswd_key_name = deviceIP + "_pswd"
        print("\n")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Looking for credentials: Fetching values for keys " + user_key_name + " and " + pswd_key_name)
        client = Client()
        keys = client.keys.get_all()
        try:
            user = (client.keys.get_by_name(user_key_name)).value
            pswd = (client.keys.get_by_name(pswd_key_name)).value
            print("     Obtained from KV store: user = " + user)
            print("     Obtained from KV store: pswd = " + pswd)
        except:
            return (False, "No credentials for : " + deviceIP)

        # Preapring the URL request(s) 
        #################################################################
        headers = {
            "accept": "application/json",
            "content-length": "0"
        }
        cmd_path = cmd_path[:26]

        url_list = list()

        url_base = "https://" + deviceIP + "/" + cmd_path + "/set/security/firewall/name/" + fw_instance_name + "/rule/" + str(rule_number)

        # Fetching content of JSON object rule_filter and build a list of URL calls
        #################################################################
        if 'action' in rule_content:
            action = rule_content['action']
            url = url_base + "/action/" + action
            url_list.append(url)

        if 'state' in rule_content:
            state = rule_content['state']
            url = url_base  + "/state/" + state
            url_list.append(url)

        if 'src_addr' in rule_content:
            src_addr = rule_content['src_addr'].replace("/", "%2F")
            url = url_base + "/source/address/" + src_addr
            url_list.append(url)

        if 'src_port' in rule_content:
            try:
                protocol = rule_content['protocol']
            except:
                print ("protocol required in filter_list parameter")
            
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
                print ("protocol required in filter_list parameter")
            
            url = url_base + "/protocol/" + protocol
            url_list.append(url)
            dst_port = rule_content['dst_port']
            url = url_base + "/destination/port/" + dst_port
            url_list.append(url)

        # Sending the URL(s) 
        #################################################################
        print("Sending REST call(s):")
        for url_item in url_list:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                print("     PUT            " + url_item)
                cmd_response = requests.put(url_item, auth=(user, pswd), headers=headers, verify=False)
                cmd_response_code = str(cmd_response.status_code)
                print("     Response code:   " + cmd_response_code)
                cmd_response_code = int(cmd_response.status_code)
                if cmd_response_code != 200:
                    return (False, cmd_response_code)
                else:
                    try:
                        data = json.loads(cmd_response.text)
                        print("     Response body: ")
                        print json.dumps(data, sort_keys=True, indent=4)
                    except:
                        print ("     Response body: empty")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")