#!/usr/bin/python

import sys
import string
import re

print 'This python script transforms html-formatted google docs to standard wikicode'
def getAttribute(parent_match):
  str = parent_match.group()
  attr_regex = re.compile('</{0,1}[a-zA-Z0-9]*[> ]')
  attr = attr_regex.search(str).group()
  attr = string.strip(attr,'</ >')
  return attr

def getClass(line, match_object):
  fulltag = line[match_object.start():match_object.end()]
  attr_regex = re.compile('class="([\w]*)"')
  attr_match = attr_regex.search(fulltag)
  return attr_match.group(1)

def wikicode(line, stack, start, end):
  parent_match = stack[-1] # currently the last opening tag
  parent = getAttribute(parent_match)
  wikiline = ''  
  
  wikidict = {
             'title':['=', '='],
             'ol':['*', ''],
             'h4':['====', '===='],
             'h3':['===', '==='],
             'h2':['==', '=='],
             'h1':['=','='],
             'p': ['','']
            # pretty short I know..
             }
  oldict = {
           'c2':1,
           'c9':1,
           'c8':2,
           'c10':3,
           'c4':2,
           'c20':3,  
           }

  i = -1;

  while parent not in wikidict.keys():
    i = i - 1;
    if -i >= len(stack):
      break
    parent_match = stack[i]
    parent = getAttribute(parent_match)
  
  left = ""
  right = ""
  if parent in wikidict:
    format = wikidict[parent]
    if parent == 'ol':
       degree = oldict[getClass(line, parent_match)]
       left = format[0] * degree
    else:
       left = format[0]
       right = format[1]
       
  return (left + line[start:end] + right)

def isClosingTag(tag):
  ct = re.compile('^</')
  if ct.match(tag) is None:
    return False
  else:
    return True

def getOutput(line):
  # Define tags
  tagRegex = re.compile('<.*?>') # ('<[a-zA-Z"=/ ]*>')
  iterator = tagRegex.finditer(line)
  stack = [] # stack of match objects
  output = [] # list of wikicode lines
  content = True # The content must be between an opening and a closing tag. This boolean keeps track of this.

  prev = "" # Keeps track of the previous tag
  for match in iterator:
     cur = getAttribute(match)
 
     if isClosingTag(match.group()) == False:
       stack.append(match)
       start = match.end()  # The start of the content is the end of the opening tag
       prev = getAttribute(match)
     else:
       end = match.start()  #The end of the content is the beginning of the closing tag 
       if prev == cur:
         print line[start:end]
         output.append(wikicode(line, stack, start, end))
       else:
         print '%(prev)s and %(cur)s do not match' %vars()
       stack.pop()
  return output

# Get .html file
#html = raw_input('Enter .html file:')
#txt = raw_input('Enter output file:')
#print 'Starting parsing of %(html)s\n' % vars()

html = 'SimpleDoc.html'
file = open(html, 'rt')
line = file.readline() # LOL Google Docs output html as a single line
file.close()
output = getOutput(line)

for wikiline in output:
  print wikiline

print 'Done\n'
