import httplib2
from bs4 import BeautifulSoup,SoupStrainer
import requests
import requests.exceptions
from urllib.parse import urlparse
# import urllib.parse
import re
from collections import deque
from validate_email import validate_email
import dns.resolver
import socket
import smtplib

# Get local server hostname

# SMTP lib setup (use debug level for full output)

# http = httplib2.Http()
new_urls = deque(['http://www.acs.uwinnipeg.ca'])
# status, new_urls = http.request('http://www.acs.uwinnipeg.ca/chenry/index.html')
#
# for link in BeautifulSoup(new_urls, parseOnlyThese=SoupStrainer('a')):
#     if link.has_attr('href'):

processed_urls = set()

emails = set()


while len(new_urls):

    # move next url from the queue to the set of processed urls
       url = new_urls.popleft()
       processed_urls.add(url)

    # extract base url to resolve relative links
       parts = urlparse(url)
       base_url = "{0.scheme}://{0.netloc}".format(parts)
       path = url[:url.rfind('/')+1] if '/' in parts.path else url

    # get url's content
       print("Processing %s" % url)
       try:
            response = requests.get(url)
       except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors
              continue

    # extract all email addresses and add them into the resulting set
       new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
       resolver = dns.resolver.Resolver()
       resolver.timeout = 1
       resolver.lifetime = 1
       for email in new_emails:
            for n in range(len(email)):
                if email[n]=='@':
                   servers = ''
                   for x in range(n+1, len(email)):
                        servers = servers+str(email[x])
                   try:
                       records = dns.resolver.query(servers, 'MX')
                       mxRecord = records[0].exchange
                       mxRecord = str(mxRecord)
                       emails.update(email)
                   except:
                       break









    # create a beutiful soup for the html document
    # soup = BeautifulSoup(response.text)
    #
    # # find and process all the anchors in the document
    # for anchor in soup.find_all("a"):
    #     # extract link url from the anchor
    #     link = anchor.attrs["href"] if "href" in anchor.attrs else ''
    #     # resolve relative links
    #     if link.startswith('/'):
    #         link = base_url + link
    #     elif not link.startswith('http'):
    #         link = path + link
    #     # add the new url to the queue if it was not enqueued nor processed yet
    #     if not link in new_urls and not link in processed_urls:
    #         new_urls.append(link)


# http = httplib2.Http()
# status, response = http.request('https://www.yelp.com/winnipeg')
#
# for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
#     if link.has_attr('href'):
#         print (link['href'])
