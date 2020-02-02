import requests
import warnings
import json
from st2client.client import Client
from st2common.runners.base_action import Action


class InternalCfgEsp(Action):
    def run(self, deviceIP, cmd_path, proposal, espGroup,
            encryption, hashAlg, lifetime):

        cmd_path = cmd_path[:26]
        proposal = str(proposal)
        lifetime = str(lifetime)

        # Fetching device credentials based on keys derived from deviceIP
        #################################################################
        user_key_name = deviceIP + "_user"
        pswd_key_name = deviceIP + "_pswd"
        print("\n")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Looking for credentials in KV store")
        client = Client()
        try:
            user = (client.keys.get_by_name(user_key_name)).value
            pswd = (client.keys.get_by_name(pswd_key_name)).value
            print("     Obtained from KV store: user = " + user)
            print("     Obtained from KV store: pswd = " + pswd)
        except Exception:
            return (False, "No credentials for : " + deviceIP)

        # Preapring the URL request(s)
        #################################################################
        h = {
            "accept": "application/json",
            "content-length": "0"
        }

        url_list = list()

        url_0 = "https://" + deviceIP + "/" + cmd_path
        url_1 = "/set/security/vpn/ipsec/esp-group/" + espGroup
        url_2 = "/proposal/" + proposal

        url = url_0 + url_1 + url_2
        url_list.append(url)

        url = url_0 + url_1 + url_2 + "/encryption/" + encryption
        url_list.append(url)

        url = url_0 + url_1 + url_2 + "/hash/" + hashAlg
        url_list.append(url)

        url = url_0 + url_1 + "/lifetime/" + lifetime
        url_list.append(url)

        # Sending the URL call(s)
        #################################################################
        print("Sending REST call(s):")
        for u in url_list:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                print("     PUT            " + u)
                r = requests.put(u, auth=(user, pswd), headers=h, verify=False)
                r_code = str(r.status_code)
                print("     Response code:   " + r_code)
                cmd_response_code = int(r.status_code)
                if cmd_response_code != 200:
                    return (False, cmd_response_code)
                else:
                    try:
                        data = json.loads(r.text)
                        print("     Response body: ")
                        print(json.dumps(data, sort_keys=True, indent=4))
                    except Exception:
                        print("     Response body: empty")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
