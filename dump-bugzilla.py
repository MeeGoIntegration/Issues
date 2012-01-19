#!/usr/bin/python

import sys
from bugz import bugzilla
from xml.etree.ElementTree import tostring
from osc.core import xmlindent

bugid = sys.argv[1]

x = bugzilla.Bugz('url to bugzilla', httpuser='', httppassword='')

response = x.get(bugid)

root = response.getroot()

bugroot = root.getchildren()[0]

xmlindent(bugroot)

bugtext = tostring(bugroot)

cleanbug = []
wanted = ["bug","desc","estimated_time","text","comment","depend","block"]
not_wanted = ["actual_time", "remaining_time", "bug_when"]

for line in bugtext.split("\n"):
    if line.strip().startswith("<"):
        for want in wanted:
            if want in line:
                cleanbug.append(line)
                break
    else:
        cleanbug.append(line)
for line in cleanbug:
    if line.strip().startswith("<"):
        for nwant in not_wanted:
            if nwant in line:
                cleanbug.remove(line)
print "\n".join(cleanbug)
