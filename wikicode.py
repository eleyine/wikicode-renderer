#!/usr/bin/python

import sys
import string
import re

def getAttribute(parent_match):
  tag = parent_match.group()
  attr_regex = re.compile('</{0,1}([a-zA-Z0-9]*)[> ]')
  return attr_regex.match(tag).group(1)

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
             'p': ['',''],
             'a': ['','']
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
      return ""
      break
    parent_match = stack[i]
    parent = getAttribute(parent_match)
  
  left = ""
  right = ""
  if parent in wikidict:
    format = wikidict[parent]
    if parent == 'ol':
       classCode = getClass(line, parent_match)
       if classCode in oldict:
          degree = oldict[classCode]
       else:
          degree = 0
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
         output.append(wikicode(line, stack, start, end))
       stack.pop() # this could be useful for debugging later
  return output

# File I/O
html = raw_input('Enter .html file: ')
txt = raw_input('Enter output file: ')

input_file = open(html, 'r')
line = input_file.readline() # LOL Google Docs output html as a single line
input_file.close()
output = getOutput(line)

output_file = open(txt, 'w')
output_file.write('\n'.join(output))
output_file.write('\n')
output_file.close()
