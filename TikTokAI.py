import random
import threading
import time
from uuid import uuid4
from colorama import Fore, init
import requests
import json
import sys
import os

init()

MAX_THREADS = 100
REQUEST_DELAY = 1
MAX_RETRIES = 3
TIMEOUT = 15

APIS = {
    'tiktok_check': {
        'url': 'http://37.221.93.104:8080/dudegeorgetrial',
        'headers': {'Content-Type': 'application/json'}
    },
    'gmail_check': {
        'url': 'http://37.221.93.104:9999/checkgmail',
        'headers': {'Content-Type': 'application/json'}
    }
}

os.system('clear')
LOGO = print (""" \x1b[1;35m
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║                                                            ║
║   █████╗ ██╗  ██╗████████╗ ██████╗ ███╗   ███╗██╗██╗  ██╗  ║
║  ██╔══██╗██║  ██║╚══██╔══╝██╔═══██╗████╗ ████║██║╚██╗██╔╝  ║
║  ███████║███████║   ██║   ██║   ██║██╔████╔██║██║ ╚███╔╝   ║
║  ██╔══██║██╔══██║   ██║   ██║   ██║██║╚██╔╝██║██║ ██╔██╗   ║
║  ██║  ██║██║  ██║   ██║   ╚██████╔╝██║ ╚═╝ ██║██║██╔╝ ██╗  ║
║  ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝  ║
║                                                            ║
║  ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗            ║
║  ╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝            ║
║     ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝             ║
║     ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗             ║
║     ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗            ║
║     ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝            ║
║                                                            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""")

def get_min_followers():
    while True:
        try:
            return int(input(f'{Fore.YELLOW}[?] Enter number Followers: {Fore.WHITE}'))
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Fore.RESET}")

min_followers = get_min_followers()

def make_api_request(url, headers=None, params=None, method='get', retries=MAX_RETRIES):
    for attempt in range(retries):
        try:
            if method.lower() == 'get':
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=TIMEOUT
                )
            else:
                response = requests.post(
                    url,
                    headers=headers,
                    json=params,
                    timeout=TIMEOUT
                )
            
            response.raise_for_status()
            return response.json() if response.content else None
            
        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:
                print(f"{Fore.RED}Request failed: {e}{Fore.RESET}")
                return None
            time.sleep(1 * (attempt + 1))

def check_tiktok(email):
    api = APIS['tiktok_check']
    response = make_api_request(
        f"{api['url']}?email={email}",
        headers=api['headers']
    )
    
    if response and response.get('status') == 'registered':
        print(f'{Fore.GREEN}[+] TikTok Registered: {email}{Fore.RESET}')
        return True
    print(f'{Fore.RED}[-] TikTok Not Registered: {email}{Fore.RESET}')
    return False


def check_gmail(email):
    api = APIS['gmail_check']
    response = make_api_request(
        f"{api['url']}?email={email}",
        headers=api['headers']
    )
    
    if response and response.get('status') == 'available':
        print(f'{Fore.GREEN}[+] Gmail Available: {email}{Fore.RESET}')
        return True
    print(f'{Fore.RED}[-] Gmail Taken: {email}{Fore.RESET}')
    return False


import re
import requests
import pycountry
import datetime
from colorama import Fore, Style, init

# Initialize colorama
init()

def extract(pattern, text, default=None, yesno=False):
    match = re.search(pattern, text)
    if match:
        value = match.group(1)
        if yesno:
            return value.lower() == "true"
        return value
    return default if not yesno else False

def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

def capture(email):
    username = email.split('@')[0]
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(f'https://www.tiktok.com/@{username}', headers=headers)
        tikinfo = response.text

        getting = str(tikinfo.split('webapp.user-detail"')[1]).split('"RecommendUserList"')[0]

        user_info = {
            "user_id": extract(r'"id":"(.*?)"', getting, ""),
            "nickname": extract(r'"nickname":"(.*?)"', getting, ""),
            "signature": extract(r'"signature":"(.*?)"', getting, ""),
            "region": extract(r'"region":"(.*?)"', getting, ""),
            "following": extract(r'"followingCount":(\d+)', getting, "0"),
            "followers": extract(r'"followerCount":(\d+)', getting, "0"),
            "likes": extract(r'"heart":(\d+)', getting, "0"),
            "videos": extract(r'"videoCount":(\d+)', getting, "0"),
            "private": extract(r'"privateAccount":(true|false)', getting, yesno=True),
            "verified": extract(r'"verified":(true|false)', getting, yesno=True),
            "secuid": extract(r'"secUid":"(.*?)"', getting, "")
        }

        try:
            country_obj = pycountry.countries.get(alpha_2=user_info["region"])
            country_name = country_obj.name
            country_flag = country_obj.flag
        except:
            country_name = user_info["region"]
            country_flag = ""

        binary = "{0:b}".format(int(user_info["user_id"])) if user_info["user_id"].isdigit() else ""
        timestamp = int(binary[:31], 2) if len(binary) >= 31 else 0
        try:
            created_date = datetime.datetime.fromtimestamp(timestamp)
        except:
            created_date = ""

        # Beautiful formatted output
        print(f"\n{Fore.CYAN}⎯" * 50)
        print(f"{Fore.YELLOW}📱 TikTok Account Information{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⎯" * 50)
        print(f"{Fore.GREEN}✉️ Email: {Fore.WHITE}{email}")
        print(f"{Fore.GREEN}👤 Username: {Fore.WHITE}@{username}")
        print(f"{Fore.GREEN}🏷️ Name: {Fore.WHITE}{user_info['nickname']}")
        print(f"{Fore.GREEN}🆔 User ID: {Fore.WHITE}{user_info['user_id']}")
        print(f"{Fore.GREEN}🔒 Private: {Fore.WHITE}{'Yes' if user_info['private'] else 'No'}")
        print(f"{Fore.GREEN}✅ Verified: {Fore.WHITE}{'Yes' if user_info['verified'] else 'No'}")
        print(f"{Fore.GREEN}🌍 Country: {Fore.WHITE}{country_name} {country_flag}")
        print(f"{Fore.CYAN}⎯" * 50)
        print(f"{Fore.YELLOW}📊 Account Stats{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⎯" * 50)
        print(f"{Fore.GREEN}👥 Followers: {Fore.WHITE}{format_number(int(user_info['followers']))}")
        print(f"{Fore.GREEN}🤝 Following: {Fore.WHITE}{format_number(int(user_info['following']))}")
        print(f"{Fore.GREEN}❤️ Likes: {Fore.WHITE}{format_number(int(user_info['likes']))}")
        print(f"{Fore.GREEN}🎥 Videos: {Fore.WHITE}{format_number(int(user_info['videos']))}")
        print(f"{Fore.CYAN}⎯" * 50)
        print(f"{Fore.YELLOW}📝 Bio{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⎯" * 50)
        print(f"{Fore.WHITE}{user_info['signature'] or 'No bio available'}")
        print(f"{Fore.CYAN}⎯" * 50 + Style.RESET_ALL)

        # Save to file
        with open('hits.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Username: @{username}\n")
            f.write(f"Name: {user_info['nickname']}\n")
            f.write(f"User ID: {user_info['user_id']}\n")
            f.write(f"Private: {'Yes' if user_info['private'] else 'No'}\n")
            f.write(f"Verified: {'Yes' if user_info['verified'] else 'No'}\n")
            f.write(f"Country: {country_name} {country_flag}\n")
            f.write(f"Followers: {format_number(int(user_info['followers']))}\n")
            f.write(f"Following: {format_number(int(user_info['following']))}\n")
            f.write(f"Likes: {format_number(int(user_info['likes']))}\n")
            f.write(f"Videos: {format_number(int(user_info['videos']))}\n")
            f.write(f"Bio: {user_info['signature'] or 'No bio available'}\n")
            f.write(f"{'='*50}\n")

        return True

    except Exception as e:
        print(f"{Fore.RED}❌ Error fetching TikTok info for {email}: {e}{Style.RESET_ALL}")
        return False

def generate_random_username():
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(chars) for _ in range(random.randint(6, 12)))

def scraper():
    while True:
        try:
            g = random.choice([
                'ğüişöçñäüğüişöçñäüğüişöçñäüqw.ertyuiopasdfghjklzxcvbnm',
                'abcdefghijklmnopqrstuvwxyzéèêëàâäôùûüîïçÿæœ',
                'αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ',
                'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
                'áéíóúýàèìòùâêîôûãñõäëïöüÿçšž',
                'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
            ])

            keyword = ''.join((random.choice(g) for _ in range(random.randrange(4, 9))))
            idd6 = "".join(random.choice('1234567890') for _ in range(19))
            
            he3 = {
                "User-Agent": f'com.zhiliaoapp.musically/{keyword} (Linux; U; Android {random.randrange(7,13)}; ar_IQ_#u-nu-latn; ANY-LX2; Build/{keyword}; Cronet/58.0.{random.randrange(3,9)}.0)'
            }
            
            try:
                ttwid = requests.get('https://www.tiktok.com/', headers=he3, timeout=10).cookies.get_dict().get('ttwid', '')
                shelby = requests.get(
                    'https://www.tiktok.com/api/search/user/full/'
                    '?aid=1988&app_language=ar&app_name=tiktok_web&battery_info=0.84'
                    '&browser_language=ar-IQ&browser_name=Mozilla&browser_online=true'
                    '&browser_platform=Linux%20aarch64&browser_version=5.0%20%28X11%3B%20Linux%20x86_64%29'
                    '%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F106.0.0.0'
                    '%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&cursor=0'
                    '&device_id=7136188745632548358&device_platform=web_pc&focus_state=true'
                    '&from_page=search&history_len=40&is_fullscreen=false&is_page_visible=true'
                    '&keyword=dude&os=linux&priority_region=&referer=&region=IQ'
                    '&screen_height=796&screen_width=360&tz_name=Asia%2FBaghdad'
                    '&verifyFp=verify_l9zrjkcx_XSZCv5U7_xzys_4UEP_8m1a_TibJS3izVTHL'
                    '&webcast_language=ar&msToken=qfFKcpRIe_b543Hfa7buaE31PLWDv6-_TQYqevIaTVOPrUNjuwuHR2z0_cEadFELKqD9p6fLuWk8tgAO9lDmVCUX4vqnit3V4rX9zvJfLCbhs9U2apBgYHmKpXPp6DLl2wZy35z0xD6g6TSu_NIh'
                    '&X-Bogus=DFSzswVLk-tANxW1S02v8OxPBxgg'
                    '&_signature=_02B4Z6wo00001IuO8aAAAIDBSFHuFzoQUMCLjvUAAEGFfa',
                    headers=he3,
                    timeout=10
                )
                msToken = shelby.cookies.get_dict().get('msToken', '')
                
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=1, i',
                    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': he3["User-Agent"],
                }

                params = {
                    'WebIdLastTime': '1715883147',
                    'aid': '1988',
                    'app_language': 'en',
                    'app_name': 'tiktok_web',
                    'browser_language': 'en-US',
                    'browser_name': 'Mozilla',
                    'browser_online': 'true',
                    'browser_platform': 'Win32',
                    'browser_version': he3["User-Agent"],
                    'channel': 'tiktok_web',
                    'cookie_enabled': 'true',
                    'cursor': '220',
                    'data_collection_enabled': 'false',
                    'device_id': idd6,
                    'device_platform': 'web_pc',
                    'focus_state': 'true',
                    'from_page': 'search',
                    'history_len': '5',
                    'is_fullscreen': 'false',
                    'is_page_visible': 'true',
                    'keyword': keyword,
                    'odinId': '7369661640164000774',
                    'os': 'windows',
                    'priority_region': '',
                    'referer': '',
                    'region': 'PE',
                    'screen_height': '864',
                    'screen_width': '1536',
                    'search_id': '20240801154310BA7846F9CDEDD312B464',
                    'tz_name': 'Asia/Baghdad',
                    'user_is_login': 'false',
                    'web_search_code': '{"tiktok":{"client_params_x":{"search_engine":{"ies_mt_user_live_video_card_use_libra":1,"mt_search_general_user_live_card":1}},"search_server":{}}}',
                    'webcast_language': 'en',
                    'msToken': msToken,
                    'X-Bogus': 'DFSzswVLRekANHWvtvtx-ShPmkfD',
                    '_signature': '_02B4Z6wo00001nO.kIwAAIDCAGLSLe4xtvJzv5QAAPpT70',
                }

                ses = str(uuid4()).replace('-', '')
                cookies = {
                    'cookie': f'passport_csrf_token=446c23e1b656077bd01b1f379ff01c64; passport_csrf_token_default=446c23e1b656077bd01b1f379ff01c64; tiktok_webapp_theme=dark; cookie-consent="ga":true,"af":true,"fbp":true,"lip":true,"bing":true,"ttads":true,"reddit":true,"version":"v8"; _ttp=2HZr0KnJ2pqKwJRyQ8myJ28Lpa8; __tea_cache_tokens_1988="user_unique_id":"7160599742786815489","timestamp":1667850947815,"_type_":"default"; passport_auth_status=c8fe9febc06f8f7a271309fa9e4f80e9,; passport_auth_status_ss=c8fe9febc06f8f7a271309fa9e4f80e9,; tt_csrf_token=CSVYu9wW-NbmqJ_cgNMHwEIItUNZGwDPM-hU; tt_chain_token=K01fXiH8q/IKwxFnx8jzcA==; _abck=951F354EE38142028A7429E8C92DB598~0~YAAQVvvOF6YBsxSFAQAAMc+wPgl24s0qz4P3iMup3WLL4PWyu/iF6+jb4qL2RfvMEKOGTv6dPfAH9AA2Hm+t/Z/Qn1TlkKHzKXk+KmuWj5d1dmCzqXD0BWgAUcMFCLRinQHou0lzh0ImXOw3B98dRIVnofWMwN8L8JxOErAxrQfi2JIEgTjNECxiZFYaqhpfLqyAUXBESaQxfCYfbNwLNwAAZvjpAfc1viGc/I9vlRIeVc2jYPA5/YUVwAytWPIOb2RuvdrXc2bfybwD3ffG0godURyE+r0QSJapjZK7kfVwbPGnVLal0dzAQM6MK2iDC5YhXugMYw9ZXB2CIaYRg4Cqy/t6BabKM9i+ZJgdvwWQQ6ljnk0pa1bKBsAYL79BxNMrQWccpQxQhUm9n09604O82PBKq8E=~-1~-1~-1; bm_sz=304AE404FA2929B0E90042E8314D20CA~YAAQVvvOF6kBsxSFAQAAMc+wPhIfC1eYkaU2YudlghSK8pNrkVcLYapeM/xrzvQbQkT9quFNwKNHsG4xkv6anwuDXn+BSd+gzoBWSdRZJscGEzPghGpbTStjyG61DtaJIqpkgjW7q6BEP37XgXgrWfHRdmoN5zraADDH7wpkIQ3UlBq5rj88cFl1IY4CUg2DSRugvtjKk+vcNV5AUjQ++v859Tv3vYF3Ga6m5lifIf0u50u/dC1xeVz0p4ew+7U21dwrDdNrai63bM7T9ArdMNk1q+2YK55FJU7tdQwtKtdLtnI=~4407620~4277556; ak_bmsc=EE17F7D340A941EB628DF68B5981EA8D~000000000000000000000000000000~YAAQVvvOF/8BsxSFAQAAS/SwPhJbeUd2XpuVnfaiGo9WDUNsMw3AUn4T4r4BtvFH6pwejSxQJ/K4aoQUK/hGU8InWjW8iSyWgKZxkNIl6lgAAvUdX8CiKcyfyQKJYfQcPDyxW6dnF6+VF2/BABsRcYTw9LUX6MjuhvgtLs1uh3AbWeHxdZFDhp/YYwjrPxoOEXgItQjGUSsxRhgRubItrsXwhW20gW9y+I7Eq22TORlAZOn+jyrl2bYH6C4yxD8yld+5OcSAQ3zKJfQLUjNj03BMgtlIyYT74OIh6GwUzgtjpGLUCzpqdeiOFZdfZApTnRoTK9J01CpUY+YxrThJKz4dScjK1V78LSd2CkfUakgFa7TXfZ1fgfPX/RW2nkWTe9SZtvDH3f62qd9b5oNojffOAM0fpnNeX06hNWSNDRRuiHOmv3m49PN2cJhknh753LdNdt81kj8LJ3SEe1y3sfHb0nPwafPExOaSSrXviHwj4+yLWrZw+dXy3Q==; sid_guard=5d52768f6a4a876314ea37244edfd0d0|1671794088|21600|Fri,+23-Dec-2022+17:14:48+GMT; uid_tt={ses[:16]}; uid_tt_ss={ses[:16]}; sid_tt={ses}; sessionid={ses}; sessionid_ss={ses}; sid_ucp_v1=1.0.0-KDM1ZGU2ODk4YzcyNDJkMzUxNWRiMTVlMzc3OTMyZTNlY2JlYWYwYWMKCRCom5adBhizCxADGgZtYWxpdmEiIDVkNTI3NjhmNmE0YTg3NjMxNGVhMzcyNDRlZGZkMGQw; ssid_ucp_v1=1.0.0-KDM1ZGU2ODk4YzcyNDJkMzUxNWRiMTVlMzc3OTMyZTNlY2JlYWYwYWMKCRCom5adBhizCxADGgZtYWxpdmEiIDVkNTI3NjhmNmE0YTg3NjMxNGVhMzcyNDRlZGZkMGQw; bm_sv=F556D2E15739C190D1B417337724D81E~YAAQVvvOF8ACsxSFAQAAaICxPhJ1QOpVK0jJSh0nuEay3Iz+L/0up1OoP09MVnndgBSzTjunJoYxBBQH4BTuDkQIQY+zt9kedbGoP5/7AUt2jVEq7DfEwQYdr31ZvZiHlhdU2Q5jwNvbZvNzQSokkwHoGbPqes9c4kV0ZGJuEuWc3pLurp0dkRkEBTY0UrcljYpQayw5/w7+4BlpmrMR5UAHElAGf2njGNpz3vRls+WGkTy9l8jRTCEseWkwnA9X~1; ttwid='+ttwid+'; odin_tt=70015f10b12827e4d2b9cce32ead78da9bd1f5af11487a83ba408d86d9a4fb55ec780a14ad91b601d9fe256fcb8160786311c12ef294e6bf285fbbf7eed8dff8080f26ed1bcedbdfca7244743dcbc60e; msToken='+msToken+'; msToken='+msToken+'; s_v_web_id=verify_lc0f2h1w_v9MWasYr_Uw4b_4j2o_8gdZ_QkWrSxI57MTt',
                    'pragma': 'no-cache',
                }

                try:
                    response = requests.get(
                        'https://www.tiktok.com/api/search/user/full/',
                        params=params,
                        headers=headers,
                        cookies=cookies,
                        timeout=10
                    ).json()
                    
                    for user in response.get('user_list', []):
                        user_info = user.get('user_info', {})
                        ud = user_info.get('uid', '')
                        username = user_info.get('unique_id', '')
                        followers = user_info.get('follower_count', 0)
                        
                        if followers >= min_followers and username and '_' not in username:
                            email = f"{username}@gmail.com"
                            if check_tiktok(email) and check_gmail(email):
                                capture(email)
                            
                except (requests.exceptions.RequestException, ValueError, KeyError):
                    continue
                    
            except requests.exceptions.RequestException:
                continue
                
        except Exception:
            continue

if __name__ == "__main__":
    print(f"{Fore.CYAN}[⚡] TikTok Starting threads... {Fore.RESET}")
    
    threads = []
    for _ in range(MAX_THREADS):
        t = threading.Thread(target=scraper, daemon=True)
        t.start()
        threads.append(t)
    
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[❕] Stopping threads...{Fore.RESET}")