import requests
import warnings
import json

from st2client.client import Client
from st2client.models import KeyValuePair

from st2actions.runners.pythonrunner import Action

class sstartCfg(Action):
    def run(self, deviceIP):
        
        # Fetching device credentials based on keys derived from deviceIP 
        #################################################################
        user_key_name = deviceIP + "_user"
        pswd_key_name = deviceIP + "_pswd"
        client = Client()
        keys = client.keys.get_all()
        
        try:
            user = (client.keys.get_by_name(user_key_name)).value
            pswd = (client.keys.get_by_name(pswd_key_name)).value
        except:
            return (False, "No credentials for : " + deviceIP)

        # Preapring the URL request 
        #################################################################
        headers = {
            "accept": "application/json",
            "content-length": "0"
        }

        url_base = "https://" + deviceIP
        url = url_base + "/rest/conf/"

        # Sending the URL call(s)
        #################################################################        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cmd_response = requests.post(url, auth=(user, pswd), headers=headers, verify=False)
            cmd_response_code = str(cmd_response.status_code)
       
            if cmd_response.status_code == 201:
                cmd_path = cmd_response.headers["Location"]
                cmd_path = cmd_path[0:26]
                cmd_path = str(cmd_path)
                print cmd_path[0:26]
            else:
                return (False, "Failed!")
                
