#!/usr/bin/python

import sys
import string
import re

print 'This python script transforms html-formatted google docs to standard wikicode'

def getClass(line, match_object):
  fulltag = line[match_object.start():match_object.end()]
  attr_regex = re.compile('class="([\w]*)"')
  attr_match = attr_regex.search(fulltag)
  return attr_match.group(1)

def wikicode(line, stack, start, end):
  cur_match = stack[-1] # cur is the last opening tag
  cur = cur_match.group()
  wikiline = ''  
  
  wikidict = {
             '<title>':'=',
             '<ol>':'*',
             '<h4>':'====',
             '<h3>':'===',
             '<h2>':'==',
             '<h1>':'=',
             # pretty short I know..
             }
  oldict = {
           'c2':1,
           'c4':2,
           'c20':3,  
           }

  i = -1;
  parent = cur # Parent is the html tag that contains one of the tags in wikicode
  parent_match = cur_match

  while parent not in wikidict:
    i = i - 1;
    if -i >= len(stack):
      break
    parent_match = stack[i]
    parent = parent_match.group()
  
  format = ""
  if parent in wikidict:  
    if parent == '<ol>':
       degree = oldict[getClass(line, parent_match)]
       format = wikidict[parent] * degree
    else:
       format = wikidict[parent]
       
  wikiline = format
  wikiline = wikiline + line[start:end]
  wikiline = wikiline + format
  return wikiline

def isClosingTag(tag):
  ct = re.compile('^</')
  if ct.match(tag) is None:
    return False
  else:
    return True

def getOutput(line):
  # Define tags
  tagRegex = re.compile('<[a-zA-Z"=/]*>')
  iterator = tagRegex.finditer(line)
  stack = [] # stack of match objects
  output = [] # list of wikicode lines
  content = True # The content must be between an opening and a closing tag. This boolean keeps track of this.

  for match in iterator:
     tag = match.group()
     
     if isClosingTag(tag) == False:
       print '%(tag)s is an opening tag' %vars()
       stack.append(match)
       start = match.end()  # The start of the content is the end of the opening tag
       content = True
     else:
       if content == True:
         end = match.start()  #The end of the content is the beginning of the opening tag 
         output.append(wikicode(line, stack, start, end))
       if len(stack) > 0:
         stack.pop()
       content = False 
  return output

# Get .html file
#html = raw_input('Enter .html file:')
#txt = raw_input('Enter output file:')
#print 'Starting parsing of %(html)s\n' % vars()

html = 'BIOL201LN21.html'
file = open(html, 'rt')
line = file.readline() # LOL Google Docs output html as a single line
file.close()
output = getOutput(line)

for wikiline in output:
  print wikiline

print 'Done\n'
