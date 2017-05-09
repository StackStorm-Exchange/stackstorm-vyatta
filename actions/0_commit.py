import requests
import warnings
import json
from st2client.client import Client
from st2actions.runners.pythonrunner import Action


class commit(Action):
    def run(self, deviceIP, cmd_path):

        cmd_path = cmd_path[:26]

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
        url = url_base + "/commit"

        # Sending the URL call(s)
        #################################################################
        print "Sending REST call(s):"
        print "     POST            " + url
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = requests.post(url, auth=(user, pswd), headers=h, verify=False)
            r_code = str(r.status_code)
            print "     Response code:   " + r_code

            if r.status_code == 200:
                try:
                    data = json.loads(r.text)
                    print "     Response body: "
                    print json.dumps(data, sort_keys=True, indent=4)
                    return True, data
                    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                except:
                    print "     Response body is empty"
                    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            else:
                return (False, "Failed!")
