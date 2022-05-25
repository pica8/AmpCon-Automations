## pica8SLACKBot :sparkles:
# Pica8 SLACKBOT Example
## Neal Trieber, Pica8, Inc. :wave:
## * PRELIMINARY STEPS / PREP * ######################
- MUST....(Kidding) :stuck_out_tongue_winking_eye: *SHOULD* Read [Blog Post](link) for full instructions
- MUST HAVE [PYTHON 3] (https://www.python.org/downloads/) pre-installed :smile:
-- Easy enough to install on Debian/UBUNTU:
```bash
sudo apt install python3
```
-- Red Hat/CENTOS:
```bash
sudo yum install python3
```
-- MacOS:
```bash
brew install python3
```

- HAVE ANSIBLE pre-installed and configured with a test host IF making ANSIBLE calls
-- Excellent Guide [Here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
-- Easy enough to install on Debian/UBUNTU:
```bash
sudo apt install ansible
```
-- Red Hat/CENTOS:
```bash
sudo yum install ansible
```
-- MacOS:
```bash
brew install ansible
```

- MUST INSTALL [Pica8 Ansible Module](https://github.com/pica8/Ansible/tree/main/ansible_module/v3) if making ANSIBLE calls..
## ********************************************************************
- STEP 1) [Create a SLACK account and SLACK Workspace](https://slack.com/help/articles/206845317-Create-a-Slack-workspace)
-- Additional Reference: [Great Guide from TWILIO ON How to create a SLACK Account + SLACKBOT in 'Socket Mode'](https://www.twilio.com/blog/how-to-build-a-slackbot-in-socket-mode-with-python)
- STEP 2) [Create a SLACK "APP/Channel"](https://api.slack.com/start/building/bolt-python)
-- (Also in Found in Guide from TWILIO above)
## DON'T FORGET TO BASH / SHELL EXPORT the variables below with YOUR keys from SLACK in same shell session where running this "Streamlit" APP:
# These are available once you create a slack app and generate tokens for it
```bash
export SLACK_BOT_TOKEN=xoxb-*******************************************************
export SLACK_APP_TOKEN=xapp-*******************************************************
```
## NOTES AND FILES USED IN THIS SLACKBOT: 
- USES "SOCKET MODE" (WebSocket Mode) so it DOES NOT REQUIRE 'NGROK' :smile:
- USES STREAMLIT as a UI for Pica8/AmpCon Credential Entry ONLY (**pica8SLACKBot.py**)
- USES CLI (instead of STREAMLIT) for secure Pica8/AmpCon Credential Entry (**pica8SLACKBot_NO_UI.py**)
- USES ANSIBLE (via BASH SHELL calls) to interact with Pica8/PicOS CLI
- USES Pica8's AmpCon REST APIs to interact with AmpCon - [API Docs](https://docs.pica8.com/display/ampcon/AmpCon+API+document)
- SAMPLE Bash script provided (**launch_my_SLACK_Pica8SLACKBot.sh**) to start your SLACKBOT and "bash source" the included bash profile (DON'T FORGET TO EDIT IT: **mysecrets.profile**) to auto-import your newly created SLACK Keys into SHELL variables that the BOT REQUIRES
- requirements.txt included to help you auto-install all of the needed Python modules :smile:
#
```bash
pip install -r requirements.txt
```
# ########***********************************************
## HAPPY CHATOps-ing! from Pica8
# ########***********************************************
