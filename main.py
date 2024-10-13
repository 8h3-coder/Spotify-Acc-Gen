import requests, string, random, argparse, sys
import time
import os

black="\033[0;30m"
red="\033[0;31m"
bred="\033[1;31m"
green="\033[0;32m"
bgreen="\033[1;32m"
yellow="\033[0;33m"
byellow="\033[1;33m"
blue="\033[0;34m"
bblue="\033[1;34m"
purple="\033[0;35m"
bpurple="\033[1;35m"
cyan="\033[0;36m"
bcyan="\033[1;36m"
white="\033[0;37m"
nc="\033[00m"

def getRandomString(length): 
    pool = string.ascii_lowercase + string.digits
    return "".join(random.choice(pool) for i in range(length))

def getRandomText(length): 
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))

def generate():
    nick = getRandomText(8)
    passw = getRandomString(12)
    email = nick + "@" + getRandomText(5) + ".com"

    headers = {
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US",
        "App-Platform": "Android",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "spclient.wg.spotify.com",
        "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
        "Spotify-App-Version": "8.6.72",
        "X-Client-Id": getRandomString(32)
    }
    
    payload = {
        "creation_point": "client_mobile",
        "gender": "male" if random.randint(0, 1) else "female",
        "birth_year": random.randint(1990, 2000),
        "displayname": nick,
        "iagree": "true",
        "birth_month": random.randint(1, 11),
        "password_repeat": passw,
        "password": passw,
        "key": "142b583129b2df829de3656f9eb484e6",
        "platform": "Android-ARM",
        "email": email,
        "birth_day": random.randint(1, 20)
    }
    
    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload)

    if r.status_code == 200:
        if r.json()['status'] == 1:
            return True, f"{nick}:{r.json()['username']}:{email}:{passw}"
        else:
            return False, f"Could not create the account, error: {r.json()['errors']}"
    else:
        return False, f"Failed to load the page. Response code: {r.status_code}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help="Number of accounts to generate, default is 1", type=int)
    parser.add_argument("-o", "--output", help="Output file, default is working.txt")
    args = parser.parse_args()

    if not args.number:
        try:
            N = int(input(f"{bcyan}How many accounts would you like to generate? {nc}"))
            if N < 1:
                sys.exit(f"{bred}Invalid number: minimum amount is 1{nc}")
        except ValueError:
            sys.exit(f"{bred}Invalid input: please enter a valid number{nc}")
    else:
        N = args.number

    output_file = args.output if args.output else "working.txt"

    with open(output_file, "a") as file:
        successful = 0
        failed = 0
        time.sleep(1)
        input(f"{bcyan}Welcome to SPOTIFY ACCOUNT GENERATOR. Press Enter to continue...{nc}")
        time.sleep(1)
        print(f"{byellow}\nSPOTIFY ACCOUNT GENERATOR [v2.0]\nMade by Volpino Modified By 8H3\n\nGenerating Accounts...\n{nc}")
        time.sleep(2)

        for i in range(N):
            result = generate()
            if result[0]:
                successful += 1
                print(f"{green}[SUCCESS] Account Successfully Generated: {successful}/{N}{nc}")
                credentials = f"{result[1].split(':')[2]}:{result[1].split(':')[3]}"
                file.write(f"{credentials}\n")
                print(f"{bblue}Credentials saved to {output_file}: {credentials}{nc}")
            else:
                failed += 1
                print(f"{red}[ERROR] {result[1]}{nc}")

        print(f"\n{bgreen}Generation Complete!{nc}")
        print(f"{byellow}Summary:{nc}")
        print(f"{bgreen}Working Accounts: {successful}{nc}")
        print(f"{bred}Errors: {failed}{nc}")
