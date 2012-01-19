#!/usr/bin/python

import sys, time
from github2 import client
from xml.etree.ElementTree import fromstring

xmltext = sys.stdin.read()

xmlroot = fromstring(xmltext)

title = xmlroot.find("short_desc").text


body = xmlroot.findall("long_desc")[0].find("thetext").text

comment_text = ""

for comment in xmlroot.findall("long_desc")[1:]:
    ct = comment.find("thetext").text
    if ct.strip() == "The feature's description has been updated.":
        continue
    else:
        comment_text = "%s%s\n" % (comment_text, ct.strip())

print "creating %s" % title

#gc = client.Github(username="",api_token="",proxy_host="", proxy_port=8080)
gc = client.Github(username="",api_token="",requests_per_second=1)

new_issue = gc.issues.open("MeeGoIntegration/Issues", title=title, body=body)

print "created %s" % str(new_issue.number)

time.sleep(1)

if comment_text:
    gc.issues.comment("MeeGoIntegration/Issues", new_issue.number, comment_text)

    print "commented %s" % str(new_issue.number)

    time.sleep(1)
