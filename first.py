#Simplest example of making a GET request 

import urllib.request
body = urllib.request.urlopen("https://www.bugatti.com")
print(body.read())

#*****************************************************

#creating the same GET request using the Request class and defining a
#custom User-Agent HTTP header:

import urllib.request
url = "https://www.bugatti.com"

headers = {}
headers['User-Agent'] = 'Googlebot'

request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)

print(response.read())
resonse.close()


#To create custom headers, you define a headers dictionary ,
#which allows you to then set the header key and value that you want to
#use. In this case, we’re going to make our Python script appear to be the
#Googlebot. We then create our Request object and pass in the url and the
#headers dictionary , and then pass the Request object to the urlopen function
#call . This returns a normal file-like object that we can use to read
#in the data from the remote website.