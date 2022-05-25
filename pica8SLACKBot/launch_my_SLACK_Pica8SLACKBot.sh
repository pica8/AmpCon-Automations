#!/bin/bash
source mysecrets.profile
echo "#########################################################################"
echo "DON'T FORGET TO UPDATE mysecrets.profile with your SLACK API TOKENS :) "
echo "#########################################################################"
#streamlit run ./Pica8SLACKBot.py -- -i <IP address or FQDN of AmpCon>
#streamlit run ./Pica8SLACKBot.py -- -i 1.2.3.4
#streamlit run ./Pica8SLACKBot.py -- -i myampcon.myorg.com
# -- is needed for streamlit to run properly and not be "greedy" and let's pica8SLACKBot use 
# the "-i" switch for "itself" :)

#Launch CLI Only Bot
#streamlit run ./Pica8SLACKBot_NO_UI.py -- -i 192.168.42.161

#Launch Bot with Browser UI to capture AmpCon Credential Login
streamlit run ./Pica8SLACKBot.py -- -i 192.168.42.161