import requests, base64, pyperclip, subprocess, sys, time, socket, datetime, msvcrt

def leetcode_helper(lang="py", prof="Profile 1", sol=""):
    try:
        while not is_online():
            print("\033[33mWaiting for Network...\033[33m", flush=True)
            for i in range(5, 0, -1):
                print(f"{i}", end="\r", flush=True)
                time.sleep(1)
        print("\033[32mInternet Connected...\033[32m")
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        AutoOpen = True
        lc_api = "https://leetcode-api-pied.vercel.app/daily"
        daily_qn = requests.get(lc_api).json()
        go_url = "https://leetcode.com" + daily_qn["link"] + "description/?envType=daily-question&envId=" + today
        qn = str(daily_qn["question"]["questionFrontendId"]).zfill(4)
        print("\033[32mRetrieving Daily Question (API 1)...\033[32m")
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()
    except:
        try:
            print("\033[31mLeetcode API 1 Failed...\033[31m")
            lc_api = "https://alfa-leetcode-api.onrender.com/daily"
            daily_qn = requests.get(lc_api).json()
            go_url = daily_qn["questionLink"] + "description/?envType=daily-question&envId=" + today
            qn = str(daily_qn["questionFrontendId"]).zfill(4)
            print("\033[32mRetrieving Daily Question (API 2)...\033[32m")
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()
        except:
            try:
                AutoOpen = False
                print("\033[31mLeetcode API 2 Failed...\033[31m")
                print("\033[33mOpening in Chrome...\033[33m")
                go_url = "https://leetcode.com"
                subprocess.Popen([
                    chrome_path,
                    f'--profile-directory={prof}',
                    "--new-window",
                    go_url
                ])
                qn = input("Enter Problem Number: ").zfill(4)
            except KeyboardInterrupt:
                print("Exiting...")
                sys.exit()
    finally:
        try:
            repo_url = f"https://api.github.com/repos/doocs/leetcode/contents/solution/{qn[:2]}00-{qn[:2]}99"
            qn_list = requests.get(repo_url).json()
            print("\033[33mFinding for Solution...\033[33m")
            for item in qn_list:
                if item["name"].startswith(qn):
                    qn_url = item["url"].replace("?ref=main","") + "/Solution" + sol + "." + lang + "?ref=main"
                    get_soln = requests.get(qn_url).json()
                    print("\033[32mSolution Found...\033[32m")
                    pyperclip.copy(base64.b64decode(get_soln["content"]).decode('utf-8'))
            print("\033[32mCopied to Clipboard...\033[32m")
            if AutoOpen:
                print("\033[33mOpening in Chrome...\033[33m")
                subprocess.Popen([
                    chrome_path,
                    f'--profile-directory={prof}',
                    "--new-window",
                    go_url
                ])
            print("Exiting...")
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()
        except:
            print("\033[31mFailed to Get Solution...\033[31m")
            print("Exiting...")
            sys.exit()

def is_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()

print("Press any key to continue, or 'x' to exit")
key = msvcrt.getch().decode('utf-8')
if key.lower() == 'x':
    print("\nExiting...")
else:
    leetcode_helper()
