import requests
import warnings
import json
from st2client.client import Client
from st2actions.runners.pythonrunner import Action


class InternalCfgIpRoute(Action):
    def run(self, deviceIP, cmd_path, subnet):

        cmd_path = cmd_path[:26]
        subnet = subnet.replace("/", "%2F")

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

        url_base = "https://" + deviceIP + "/" + cmd_path
        url = url_base + "/delete/protocols/static/route/" + subnet

        # Sending the URL call(s)
        #################################################################
        print "Sending REST call(s):"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            print "     PUT            " + url
            r = requests.put(url, auth=(user, pswd), headers=h, verify=False)
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
