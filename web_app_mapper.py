import queue
import threading
import os
import urllib.request

threads = 10

target = "https://www.blackhatpython.org"
directory = "/Users/justin/"
filters = [".jpg", ".gif", "png", ".css"]

os.chdir(directory)

web_paths = queue.Queue()

for r, d, f, in os.walk("."):
    for files in f:
        remote_path = "%s%s" % (r, files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

        request = urllib.request.Request(url)

        try:
            response = urllib.request.urlopen(request)
            content = response.read()

            print("[%d] => %s" % (response.code, path))
            response.close()

        except urllib.request.HTTPError as error:
            print("Failed %s" % error.code)
            pass


for i in range(threads):
    print("Spawning thread: %d" % i)
    t = threading.Thread(target=test_remote)
    t.start()


# The web_paths  variable is our Queue object where we will store the files that we’ll attempt to locate on the remote server
# We then use the os.walk function to walk through all of the files and directories in the local web application directory. As we walk through the files and directories, we’re building the full path to the target files and testing them against our filter list to make sure we are only looking for the file types we want
# For each valid file we find locally, we add it to our web_paths Queue.

# The test_remote function operates in a loop that will keep executing
# until the web_paths Queue is empty. On each iteration of the loop, we grab
# a path from the Queue x, add it to the target website’s base path, and then
# attempt to retrieve it. If we’re successful in retrieving the file, we output the
# HTTP status code and the full path to the file . If the file is not found or
# is protected by an .htaccess file, this will cause urllib2 to throw an error,
# which we handle  so the loop can continue executing.
