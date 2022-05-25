import threading, itertools
from time import sleep
from colorama import Fore, init; init()
from requests import Request, Session

threads = 20 #set threads
retries = 5 # Depending on how good your proxies are set how many times to retry before switching to another proxy, Recomended are 3 or more for public proxies and 2 or 1 for private paid proxies

# for the proxies you can use proxyscrape.com tho they are very bad and you will instantly get proxy error: "too many requests"
# for the namelist i recommend just searching for a word gen (this site fancytext.net/random-word-generator/ worked pretty fine just remove empty lines after copying everything) and genning 50K lines or smth also i recommend removing 3char words from your lists bc most of them if not all are taken

#------------------------------------- DONT EDIT UNLESS YOU KNOW WHAT YOU ARE DOING -------------------------------------

proxies = itertools.cycle(open('./proxies.txt', 'r+').read().splitlines())

print(f"Checking {len(list(open('./namelist.txt', 'r+').read().splitlines()))} usernames")

class cprint:
    def green(textt):
        print(Fore.GREEN+'[+] '+textt)

    def red(textt):
        print(Fore.RED+'[-] '+textt)

    def yellow(textt):
        print(Fore.YELLOW+'[/] '+textt)

class Check(threading.Thread):
    def __init__(self, username):
        self.username = username
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                request = Request('POST','https://github.com/signup_check/username?suggest_usernames=true',
                headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': 'https://github.com',
                    'referer': 'https://github.com/join',
                    'cookie': '_gh_sess=Yvn8FydJgmtu6mQoduS0l%2B8EMAsC%2B%2FtDTgmUtDyQHhfjz2zXsn3byLej2VaESgKhANjCaDo9HJUQ5U9ZHHl6MDS8Fglynlxy%2FNQNYaBmvDnjwZzcQ28bH8XHaPYrNqSutF14Y2umBMJs3PjNz918Nacn61XaU4dShC3lrWvAD2pjYDS586jKMXrGdloO0x0N%2FJvUtFD01huYgZgAU8tDoZuK6cdEpY4yF9FF%2FlB0l6wFSGOnFG1L1bk1pGN42fb4VOlN4uVWkeEX8c9gUd7MoA%3D%3D--vsCRyrp7Kk8R%2Bc2M--op2kFsWlG3yncWKyHTKtxw%3D%3D; _octo=GH1.1.693835820.1653342574; logged_in=no; tz=Europe%2FBratislava',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
                },
                files = {
                    'authenticity_token': (None, 'pI29lHcvV4BsqLLulKFZVEa0h21sIwAGx7+Yf81DWVCWBSxTyQsZOpmEb49qini+QkM91XK8kIhZLhp+wNaHSA=='),
                    'value': (None, self.username),
                }
                ).prepare()

                re = Session().send(request, proxies=f'http://{next(proxies)}')
                #print(re.status_code)

                if re.status_code == 200:
                    cprint.green(f'{self.username} is available')
                    with open('./available.txt', 'a+') as f:
                        f.write(self.username+'\n')
                elif re.status_code == 422:
                    cprint.red(f'{self.username} is already taken')
                elif re.status_code == 429:
                    cprint.red('Proxy Error: Too many requests')
                break
            except Exception as execpon:
                count = 1
                if count >= retries:
                    cprint.red("Bad proxy")
                    cprint.red("exception: "+str(execpon))
                    break
                else:
                    cprint.red("exception: "+str(execpon))
                    count = count+1
                    print('trying again')
                    continue

for name in list(set(open('./namelist.txt', 'r+').read().splitlines())):
    while threading.active_count() >= threads:
        sleep(0.2)
    Check(name).start()