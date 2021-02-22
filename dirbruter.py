import queue
import getopt
import sys
import threading
import requests


url = ""
wordlist_path = ""
extentions_list = []
thread_numer = 5


class Colors:
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def usage():
    usage = """
Usage : ./dirbuster -u <http://target_url> -w </wordlist_path> [-e extetions sperated by comma]

Options:
    -h, --help      :    Display this help page
    -w, --wordlist  :    specify path for wordlist
    -u, --url       :    specify target url
    -e, --extention :    apply search with the extentions
"""
    print(Colors.INFO, usage, Colors.RESET)
    sys.exit()


def bruter(words, extentions=[]):
    while not words.empty():
        attemp_list = []
        word = words.get()

        if "." in word:
            attemp_list.append(word)
        else:
            attemp_list.append(f"{word}/")

        if len(extentions):
            for ext in extentions:
                if "." in word:
                    term = word.split('.')[0]
                    term_ext = word.split('.')[1]
                    if term_ext != ext:
                        attemp_list.append(f"{term}.{ext}")
                else:
                    attemp_list.append(f"{word}.{ext}")

        for dir in attemp_list:
            brute_url = f"{url}/{dir}"
            
            try:
                headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"}
                response = requests.get(brute_url, headers=headers, timeout=3)
                if len(response.text):
                    if not (response.ok):
                        raise Exception
                    print(f"[{response.status_code}] ==> {brute_url}")
            except Exception as e:
                pass
        

def read_wordlist(wordlist):
    try:
        with open(wordlist, "r") as wdlist:
            lines = wdlist.readlines()
    except:
        print(Colors.FAIL, "[FAIL]: Error while reading wordlist make sure your specified path", Colors.RESET)

    word_queue = queue.Queue()
    for word in lines:
        word = word.strip()
        word_queue.put(word)

    return word_queue


def main():
    global url
    global wordlist_path
    global extentions_list

    argument_list = sys.argv[1:]
    if len(argument_list) < 4 or len(argument_list) > 6:
        usage()

    try:
        options, arguments = getopt.getopt(sys.argv[1:], "u:w:e:h", ["url=", "wordlist=", "extention=", "help"])
    except getopt.GetoptError as e:
        print(Colors.FAIL, "\n[FAILED]: " + str(e), Colors.RESET)
        usage()

    for opt, arg in options:
        if opt in ['-u', '--url']:
            url = arg
        elif opt in ['-w', '--wordlist']:
            wordlist_path = arg
        elif opt in ['-e', '--extention']:
            extentions = arg.split(',')
            for ext in extentions:
                extentions_list.append(ext)
        elif opt in ['-h', '--help']:
            usage()
        else:
            print(Colors.FAIL, "Unhandled options", Colors.RESET)
            usage()
    
    if not url or not wordlist_path: 
        print(Colors.WARNING, "\n[WARNING]: URL and Wordlist parameteres must be specified by the user!!!", Colors.RESET)
        usage()

    words = read_wordlist(wordlist_path)
    for _ in range(thread_numer):
        bruter_thread = threading.Thread(target=bruter, args=(words, extentions_list))
        bruter_thread.start()

    
if __name__ == "__main__":
    main()