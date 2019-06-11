# Use this script for visualisation purpose
# and 

import json 
from colorama import init, Fore, Back, Style
init()

path='processed_data\\processed_data.json'

with open(path, encoding='utf') as f:
    a=json.load(f)
for ob in a['Clusters']:
    if (len(ob)>1):
        print(Back.BLACK + Fore.YELLOW +'cluster start')
        for st in ob: 
            print(Style.RESET_ALL)
            for line in st[0].split('\n'):
                print(line)
            print(Back.GREEN + Fore.WHITE +' divider ')    
        print(Back.BLACK + Fore.YELLOW +'cluster end')