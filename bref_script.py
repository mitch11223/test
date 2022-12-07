#!/usr/bin/python
import json
import time
import requests
import os

print('Importing {rosters script} please wait')
import rosters_script
print('Importing {gamelog_script} please wait')
import gamelog_script

print('Executing gamelog_script')
gamelog_script.execute()
print('gamelog_script.execute: Status: Success!')


print('Executing rosters_script')
rosters_script.execute()
print('rosters_script.execute: Status: Success!')


