import requests
import warnings
import json

from st2client.client import Client
from st2client.models import KeyValuePair

from st2actions.runners.pythonrunner import Action

class InternalDelBgpPrefix(Action):
    def run(self, deviceIP, cmd_path, localAS, prefix):
        
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

        for subnet in prefix:
            subnet = subnet.replace("/", "%2F")
            url_base = "https://" + deviceIP + "/" + cmd_path
            url = url_base + "/delete/protocols/bgp/" + str(localAS) + "/address-family/ipv4-unicast/network/" + subnet
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