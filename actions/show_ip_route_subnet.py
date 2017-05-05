import requests
import warnings
from st2client.client import Client
from st2actions.runners.pythonrunner import Action


class showIpRouteSubnet(Action):
    def run(self, deviceIP, subnet):

        # Fetching device credentials based on keys derived from deviceIP
        #################################################################
        user_key_name = deviceIP + "_user"
        pswd_key_name = deviceIP + "_pswd"
        print "\n"
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
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

        subnet = subnet.replace("/", "%2F")
        url_base = "https://" + deviceIP + "/rest/op/"
        url = url_base + "show/ip/route/" + subnet

        # Sending the URL call(s)
        #################################################################
        print "Sending REST call(s):"
        print "     POST            " + url
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = requests.post(url, auth=(user, pswd), headers=h, verify=False)
            r_code = str(r.status_code)
            print "     Response code:   " + r_code
            r_code = int(r.status_code)
            if r_code != 201:
                return (False, r_code)
            else:
                cmd_path = r.headers["Location"]
                url = "https://" + deviceIP + "/" + cmd_path
                print "     GET             " + url
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    r2 = requests.get(url, auth=(user, pswd), headers=h, verify=False)
                    r2_code = str(r2.status_code)
                    print "     Response code:   " + r2_code
                    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                    r2_code = int(r2.status_code)
                    if r2_code != 200:
                        return (False, r2_code)
                    else:
                        try:
                            print "\n"
                            print r2.text
                        except:
                            print "     Response body: empty"
