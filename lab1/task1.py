import subprocess

import csv

import chardet



def ping(host):
  
    return subprocess.run(['ping', '-n', '1', host], stdout=subprocess.PIPE)
