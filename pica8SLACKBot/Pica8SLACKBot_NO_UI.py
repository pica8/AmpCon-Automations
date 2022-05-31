### Pica8 SLACKBOT Example
### Neal Trieber, Pica8, Inc.
#####################################################
# * PRELIMINARY STEPS / PREP * ######################
#####################################################
# STEP 1) Create a SLACK account and SLACK Workspace: https://slack.com/help/articles/206845317-Create-a-Slack-workspace
# Great Guide from TWILIO: https://www.twilio.com/blog/how-to-build-a-slackbot-in-socket-mode-with-python
# STEP 2) Create a SLACK "APP/Channel": https://api.slack.com/start/building/bolt-python
# (Also in Found in Guide from TWILIO above)
### DON'T FORGET TO BASH / SHELL EXPORT the variables below with YOUR keys from SLACK in same shell session where running this "Streamlit" APP:
# These are available once you create a slack app and generate tokens for it
# bash~$: export SLACK_BOT_TOKEN=xoxb-*******************************************************
# bash~$: export SLACK_APP_TOKEN=xapp-*******************************************************
##########***********************************************
# NOTES: * THIS SLACKBOT: 
#               - USES "SOCKET MODE" (WebSocket Mode) so it DOES NOT REQUIRE 'NGROK' :)
#               - USES ANSIBLE (via BASH SHELL calls) to interact with Pica8/PicOS CLI
#               - USES Pica8's AmpCon REST APIs to interact with AmpCon: https://docs.pica8.com/display/ampcon/AmpCon+API+document
#               - SAMPLE Bash script provided to start your SLACKBOT and "bash source" your newly created SLACK Keys into SHELL variables
#               - Requirements.txt to help you auto-install all of the needed Python modules: pip install -r requirements.txt
##########***********************************************
# command-line example: streamlit run pica8SLACKBot_NO_UI.py -- -i 1.2.3.4
##########***********************************************

from __future__ import (absolute_import, division, print_function)
from queue import Full
__metaclass__ = type
import re
import requests
import sys
import os, shutil, getopt
import glob
import io
from pathlib import Path
import types
import urllib
import subprocess
import json
import simplejson
from urllib.parse import urlparse
from subprocess import Popen, PIPE, STDOUT
import datetime
from datetime import datetime as date
import hashlib
import collections
import functools
import inspect
import textwrap
import time
import random
import string
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import getpass

inputfile= ''
pica8apikey = ''
pica8instance = ''
bearerstr = ''
if sys.version[0] == '2':
    sys.reload(sys)
    sys.setdefaultencoding("utf-8")

picosrequests = []

def setargs(bearerstr, pica8apikey, pica8instance, argv):
    try:
        opts, remainder = getopt.gnu_getopt(sys.argv[1:], 'i:k:h:', ['help=','pica8apikey=','pica8instance='])
    except getopt.GetoptError as err:
        print ('USAGE: pica8SLACKBot_NO_UI.py <flag> option: \n -i <FQDN or IP address of AmpCon - I.e. www.ampcon.com or 10.10.10.1)\n -k <Token/APIKey provided by AmpCon for authentication>\n',  err)
        sys.exit(2)
    if len(sys.argv) <= 1:
        # printbanner()
        print ('USAGE: pica8SLACKBot_NO_UI.py <flag> option: \n -i <FQDN or IP address of AmpCon - I.e. www.ampcon.com or 10.10.10.1)\n -k <Token/APIKey provided by AmpCon for authentication>\n')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h'):
            # printbanner()
            print ('USAGE: pica8SLACKBot_NO_UI.py <flag> option: \n -i <FQDN or IP address of AmpCon - I.e. www.ampcon.com or 10.10.10.1)\n -k <Token/APIKey provided by AmpCon for authentication>\n')
            sys.exit()
        if opt in ('-k'):
            pica8apikey = (arg)
            print ("The ApiKey/Token is: " + str(pica8apikey))
            bearerstr = 'Bearer ' + str(pica8apikey)
            #return inputfile
        if opt in ('-i'):
            pica8instance = (arg)
            print ("The AmpCon Instance being used is: " + str(pica8instance))
            #return inputfile
    return bearerstr, pica8apikey, pica8instance, argv

bearerstr, pica8apikey, pica8instance, sys.argv = setargs(bearerstr, pica8apikey, pica8instance, sys.argv)

print ("Please Enter your AmpCon Username:")
username = input()
password = getpass.getpass(prompt='Please Enter your AmpCon Password: ', stream=None)

payload = json.dumps({
  "username": username,
  "password": password
})


tokenurl = "https://" + pica8instance + "/token"
tokenheaders = {
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(pica8apikey), 
    'Content-Type': 'application/json',
}

response = requests.request("POST", tokenurl, headers=tokenheaders, data=payload, verify=False)
pica8apikey = response.text

pica8apiurl =  "https://" + pica8instance + "/api"

tokenurl = "https://" + pica8instance + "/token"
tokenheaders = {
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(pica8apikey), 
    'Content-Type': 'application/json',
}
print ("API KEY Retrieved: " + pica8apikey)            
    
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(pica8apikey), 
    'Content-Type': 'application/json',
}

    #print ("Sending these headers: " + headers)


#context.picosARGS = ImmutableDict(connection='smart', module_path=['/to/mymodules /usr/share/ansible'], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False, verbosity=0)

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
#@app.message(re.compile("(hi|hello|hey)", re.IGNORECASE))
#def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
#    say(f"Hey there <@{message['user']}>!")


@app.message(":wave:")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")


@app.message(re.compile("hi", re.IGNORECASE))
@app.message(re.compile("hello", re.IGNORECASE))
@app.message(re.compile("hullo", re.IGNORECASE))
@app.message(re.compile("howdy", re.IGNORECASE))
@app.message(re.compile("hey", re.IGNORECASE))
@app.message(re.compile("good day", re.IGNORECASE))
@app.message(re.compile("cheerio", re.IGNORECASE))
@app.message(re.compile("greetings", re.IGNORECASE))
def hi(message, say):
    say(f"Hey there <@{message['user']}>!")
    say('How can I help you with your Pica8 Infrastructure Today?')
    say('Simply ask me a question about that network that AmpCon can answer or possibly do for you, or you can enter a picos command you want to send to your Pica8 Devices using the PicOS picos command or Ask me a question. You can also tell me to do things with AmpCon, like deploy conifguration changes, launch playbooks, or just retrieve info.\n Like this: \'picos show vlans\' if entering multiple commands simply put a \';\' bewteen the commands like this: \' picos conf; run show running-config\'')

@app.message(re.compile("thank.*", re.IGNORECASE))
def thanks_response(message, say):
    say("You're Welcome! May I be of further assistance? \n. Simply enter another command or ask me a question and I will show you the result if I am able to compete the task.")

@app.message(re.compile("yes", re.IGNORECASE))
@app.message(re.compile("correct", re.IGNORECASE))
@app.message(re.compile("affirmative", re.IGNORECASE))
@app.message(re.compile("confirmed", re.IGNORECASE))
def yes_response(message, say, picosrequest):
    say('Simply ask me a question about that network that AmpCon can answer or possibly do for you, or you can enter a picos command you want to send to your Pica8 Devices using the PicOS picos command or Ask me a question. You can also tell me to do things with AmpCon, like deploy conifguration changes, launch playbooks, or just retrieve info.\n Like this: picos show vlans')

@app.message(re.compile(".*list.* global configs.*", re.IGNORECASE))
@app.message(re.compile(".*list.*global config.*", re.IGNORECASE))
def hi(message, say):
    say(f"Hey there <@{message['user']}>!")
    say('Let me check AmpCon one moment please...')
    globalconfigurl = pica8apiurl + "/global_config"
    response = requests.request("GET", globalconfigurl, headers=headers, verify=False)
    globalconfigsresponse = response.text
    print (globalconfigsresponse)
    globalconfigs = json.loads (globalconfigsresponse)
    say('Here\'s a list of the Global Configurations I found:')
    for GlobalConfig in globalconfigs:
    #print ('*********************************\n')
        configname = str(GlobalConfig['name'])
        say(configname)
        say('-------------------------------------------------')
        config = GlobalConfig['config']
        #print (configname)
        say('And Here\'s ' + configname + ' Global Config:')
        say('-------------------------------------------------')
        say(config)
    say('Was that helpful?')
    
@app.message(re.compile(".*show.* switch.*", re.IGNORECASE))
@app.message(re.compile(".*show.* site.*", re.IGNORECASE))
@app.message(re.compile(".*site.* config.*", re.IGNORECASE))
@app.message(re.compile(".*switch.* config.*", re.IGNORECASE))
def hi(message, say):
    say(f"Hey there <@{message['user']}>!")
    say('Let me check AmpCon one moment please...')
    switchconfigurl = pica8apiurl + "/switch_config"
    response = requests.request("GET", switchconfigurl, headers=headers, verify=False)
    switchconfigsresponse = response.text
    print (switchconfigsresponse)
    switchconfigs = json.loads (switchconfigsresponse)
    say('Here\'s a list of the Switch/Site-Level Configurations I found:')
    for SwitchConfig in switchconfigs:
    #print ('*********************************\n')
        configname = str(SwitchConfig['name'])
        say(configname)
        config = SwitchConfig['config']
        #print (configname)
        say('And here\'s the ' + configname + ' config:')
        say('-------------------------------------------------')
        say(config)
    fullconfigsurl = pica8apiurl + "/config_files"
    response = requests.request("GET", fullconfigsurl, headers=headers, verify=False)
    fullconfigslistresponse = response.text
    print (fullconfigslistresponse)
    fullconfigslist = json.loads (fullconfigslistresponse)
    say('Here\'s a list of Full Switch Configurations I found:')
    for FullConfig in fullconfigslist:
        #for individualconfiguration in FullConfig:
        #print (individualconfiguration)
        say('*********************************\n')
        myconfigname = str(FullConfig['name'])
        say(myconfigname)
        say('*********************************\n')
        myconfig = str(FullConfig['content'])
        #print (configname)
        say('And here\'s the ' + myconfigname + ' config:')
        say('-------------------------------------------------')
        say(myconfig)
    say('Was that helpful? To see a list of available switches to configure, ask me to list them for you :)')

@app.message(re.compile(".*show.* switches", re.IGNORECASE))
@app.message(re.compile(".*list.* switch.*", re.IGNORECASE))
@app.message(re.compile(".*switch.* list.*", re.IGNORECASE))
@app.message(re.compile(".*show.* list.* .*switch.*", re.IGNORECASE))
@app.message(re.compile(".*show.* list.* .*switch.*", re.IGNORECASE))
@app.message(re.compile(".*available.* switches", re.IGNORECASE))
@app.message(re.compile(".*available.* .*device.*", re.IGNORECASE))
def hi(message, say):
    say(f"Hey there <@{message['user']}>!")
    #say(message['text'])
    say('Let me check AmpCon one moment please...')
    switchlisturl = pica8apiurl + "/switch/all_switch_list"
    print ('sending to : ' + switchlisturl)
    response = requests.request("GET", switchlisturl, headers=headers, verify=False)
    switchlistresponse = response.text
    print (switchlistresponse)
    switches = json.loads (switchlistresponse)
    say('Here\'s a list of the Switch/Site-Level Configurations I found:')
    for switch in switches:
    #print ('*********************************\n')
        switchname = str(switch['host_name'])
        say(switchname)
        serialnumber = switch['sn']
        #print (configname)
        say('Switch: ' + switchname)
        say('Serial: ' + serialnumber)
        say('-------------------------------------------------')
        
@app.message(re.compile(".*deploy", re.IGNORECASE))
@app.message(re.compile(".*push", re.IGNORECASE))
def hi(message, say):
    deploymentrequest = (message['text'])
    say(f"Understood <@{message['user']}>!")
    say('Let me check AmpCon and ready the switch for deployment, one moment please...')
    switchListing = {}
    configListing = {}
    switchconfigurl = pica8apiurl + "/config_files"
    response = requests.request("GET", switchconfigurl, headers=headers, verify=False)
    switchconfigsresponse = response.text
    print (switchconfigsresponse)
    switchconfigs = json.loads (switchconfigsresponse)
    say('Gathering Configs and Switches...')
    for SwitchConfig in switchconfigs:
    #print ('*********************************\n')
        configname = str(SwitchConfig['name'])
        #say(configname)
        config = SwitchConfig['content']
        print (configname)
        confignameregex = re.compile (configname, re.IGNORECASE)
        confignamefound = re.findall(confignameregex, str(deploymentrequest))
        if (confignamefound):
            configtodeploy = configname
        #configListing.update( {configname : config} )
        #say('And here\'s the ' + configname + ' config:')
        #say('-------------------------------------------------')
        #say(config)
    switchlisturl = pica8apiurl + "/switch/all_switch_list"
    print ('sending to : ' + switchlisturl)
    response = requests.request("GET", switchlisturl, headers=headers, verify=False)
    switchlistresponse = response.text
    print (switchlistresponse)
    switches = json.loads (switchlistresponse)
    for switch in switches:
    #print ('*********************************\n')
        switchname = str(switch['host_name'])
        #print (switchname)
        #say(switchname)
        serialnumber = switch['sn']
        switch_regex = re.compile (switchname, re.IGNORECASE)
        #print (str(switch_regex))
        switchnamefound = re.findall(switch_regex, str(deploymentrequest))
        #print ("Request: " + deploymentrequest)
        #print ("found: " + (switchnamefound))
        if (switchnamefound):
                switchtodeploy = switchname
                switchtodeployserial = serialnumber
        #print (configname)
        #say('Switch: ' + switchname)
        #say('Serial: ' + serialnumber)
        #switchListing.update( {switchname : serialnumber} )
        #say('-------------------------------------------------')    
    say("Deploying " + configtodeploy + " to switch " + switchtodeploy + "....Please Stand By....")
    deploymenturl = pica8apiurl + "/config_files/push"
    payload = json.dumps({
        "config_name": configtodeploy,
        "switch_checked": {
            "checkall": False,
            "checkedNodes": [
            {
                "sn": switchtodeployserial
            }
            ],
            "uncheckedNodes": []
        },
        "group_checked": {
            "checkall": False,
            "checkedNodes": [],
            "uncheckedNodes": []
        }
        })
    response = requests.request("POST", deploymenturl, headers=headers, data=payload, verify=False)
    print(response.text)
    deploymentresponse = response.text
    #print (switchlistresponse)
    #deploymentresults = json.loads (deploymentresponse)
    #say('Here\'s a list of the Switch/Site-Level Configurations I found:')
    #print ('*********************************\n')
    say('Deployment Successful!')
    say('Was that helpful?')



@app.message(re.compile("no", re.IGNORECASE))
def no_response(message, say):
    say('Would you like to ask me something about the network? Or make a change to it?')
    say('Simply ask me a question about that network that AmpCon can answer or possibly do for you, or you can enter a picos command you want to send to your Pica8 Devices using the PicOS picos command or Ask me a question. You can also tell me to do things with AmpCon, like deploy conifguration changes, launch playbooks, or just retrieve info.\n Like this: \'picos show vlans\' if entering multiple commands simply put a \';\' bewteen the commands like this: \' picos conf; run show running-config\'')

    #def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{message['user']}>!",
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


#@app.message(re.compile("(What.*)", re.IGNORECASE))
#@app.message(re.compile("(When.*)", re.IGNORECASE))
#@app.message(re.compile("(Why.*)", re.IGNORECASE))
#@app.message(re.compile("(Which.*)", re.IGNORECASE))
#@app.message(re.compile("(Who.*)", re.IGNORECASE))
#@app.message(re.compile("(How.*)", re.IGNORECASE))
#@app.message(re.compile("(Whose.*)", re.IGNORECASE))
#pattern = re.compile(r"\d+[^?]*you|(\d+[^?]*\?)")
#@app.message(re.compile("I\s", re.IGNORECASE))
# @app.message(re.compile("want", re.IGNORECASE))
# @app.message(re.compile("need", re.IGNORECASE))
# @app.message(re.compile("change", re.IGNORECASE))
# @app.message(re.compile("update", re.IGNORECASE))
# @app.message(re.compile("upgrade", re.IGNORECASE))
# @app.message(re.compile("modify", re.IGNORECASE))
#@app.message(re.compile("conf.*", re.IGNORECASE))

@app.message(re.compile("picos .*", re.IGNORECASE))
def assist_response(message, say):
    say ("I'm going to analyze the task you would like performed and let you know if I have any limitations. One moment please... ")
    print (message)
    for item in message:
        print ("Item: " + item)
    for key, value in message.items():
        print("Key: " + key)
        if (key=="text"):
            picosrequest = value
            picoscommand = picosrequest.split("picos ",1)[1]
            print ("PicOS COMMAND: " + picoscommand)           
            #print (str(picoscommand[1]))
            #print (str(picoscommand[2]))
            print ("PicOS Request entered is " + str(picoscommand))
    print (picosrequest)
    vlan_regex = re.compile ('vlan', re.IGNORECASE)
    vlans = re.findall(vlan_regex, str(picosrequest))
    add_regex = re.compile ('add', re.IGNORECASE)
    delete_regex = re.compile ('delete', re.IGNORECASE)
    vlanid =  r"\d*"
    vlanid_regex = re.compile(vlanid)
    addvlan = re.findall(add_regex, str(picosrequest))
    deletevlan = re.findall(delete_regex, str(picosrequest))
    vlanidmatch = re.findall(vlanid_regex, str(picosrequest))
    result = vlanid_regex.findall(picosrequest)
    regex = '\d+'      
    "(x|(w-))?[^-]...-\\d{6,6}-\\w\\w-.{0,}"
    ""
    
    print (result)
    for item in result:
        match = re.findall(regex, item)
        if (match):
            print (str(match))
        #if (match):
        #print ("MATCHED VLAN: " + match) 
            print ("Result item: " + item)
            vlannum = item
            print ("VLAN: " + vlannum)
            #vlannum = item 
            print (vlannum)
    
    #real ansible command --> ansible pica8switch -m picos_config -a "mode='cli_show' cmd='sh int br'" -t ansible_output -o
    #ansiblecommand1 = 'ansible labswitches -m picos_config -a "mode=\'cli_show\' cmd=\'' + picosrequest + '\'" -t ansible_output -o'
    ansiblecommand = 'ansible pica8vms -m picos_config -a "mode=\'cli_show\' cmd=\'' + picoscommand + '\'" -t ansible_output -o'
    os.system(ansiblecommand)
    
    fileinputvm = open("./ansible_output/picosv", "r")
    
    responsevm = json.load(fileinputvm)
    stdouttextvm = str(responsevm['stdout'])
    stdoutlinesvm = str(responsevm['stdout_lines'])
    say ("Sure, I can assist you with that " + picosrequest)
    say ("Here's the result from PicOS-V:\n" + stdouttextvm + "\n" )

    
# Start your app
#if __name__ == "__main__":
#    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

if __name__ == "__main__":
    # export SLACK_APP_TOKEN=xapp-***
    # export SLACK_BOT_TOKEN=xoxb-***
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()