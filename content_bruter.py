import urllib.request
import threading
import queue
import urllib

threads = 50
target_url = "http://testphp.vulnweb.com"
wordlist_file = "/tmp/all.txt"  # from SVNDigger
resume = None
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101Firefox/19.0"


def build_wordlist(wordlist_file):
    # read in the word list
    fd = open(wordlist_file, "rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = queue.Queue()

    # We have some built-in functionality that allows us to resume a brute-forcing session if our
    # network connectivity is interrupted or the target site goes down. This can
    # be achieved by simply setting the resume variable to the last path that the
    # brute forcer tried.

    for word in raw_words:
        word = word.rstrip()

        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming worlist from: %s" % resume)

        else:
            words.put(word)

    return words


def dir_bruter(word_queue, extensions=None):
    while not word_queue.empty():
        attempt = word.queue.get()
        attempt_list = []

        # check to see if there is a file extension; if not, it's a directory path we're bruting
        if '.' not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s/" % attempt)

        # if we ant to bruteforce extensions
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt, extension))

        # iterate over our list of attempts
        for brute in attempt_list:
            url = "%s%s" % (target_url, urllib.quote(brute))

            try:
                headers = {}
                headers["User-Agent"] = user_agent
                r = urllib.request.Request(url, headers=headers)

                response = urllib.request.urlopen(r)

                if len(response.read()):
                    print("[%d] => %s" % (response.code, url))

            except urllib.request.URLError:
                if hasattr(e, 'code') and e.code != 404:
                    print("!!! %d => %s" % (e.code, url))

                pass


word_queue = build_wordlist(wordlist_file)
extensions = [".php", ".bak", ".orig", ".inc"]

for i in range(threads):
    t = threading.Thread(target=dur_bruter, args=(word_queue, extensions,))
    t.start()
