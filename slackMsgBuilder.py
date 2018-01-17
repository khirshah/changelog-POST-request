#-------------------------- import -------------------------------
import urllib.request, urllib.parse
import argparse
import markdown
import json
import os.path
from HTMLParsExt import MyHTMLParser

#------------------------ functions -----------------------------

def str_part(text,d1,d2):
    string=text.partition(d1)[2]
    return string.partition(d2)[0]

def add_args():
  argparser.add_argument('-ch', '--channel',
                        help='channel to POST to',
                        required=True)
  argparser.add_argument('-usr', '--username',
                        help='name of the user',
                        required=True)
  argparser.add_argument('-em', '--emoji',
                        help='icon to show',
                        required=True)
  argparser.add_argument('-lnk', '--link',
                        help='file source URL',
                        required=False,
                        default='')
  argparser.add_argument('-f', '--file',
                        help='filename+path',
                        required=False,
                        default='')
  argparser.add_argument('-ver', '--version',
                        help='version to display',
                        required=False,
                        default='latest')

#-------------------------- init --------------------------------
#get variables from sh command
argparser = argparse.ArgumentParser()
add_args()
args = argparser.parse_args()

ChLogTxt=""

#open file
if  args.file!='' and args.link=='':
  with open(args.file) as f:
    ChLogTxt = f.read()
elif args.link!='' and args.file=='':
  c=urllib.request.urlopen(args.link)
  content=c.read()
  ChLogTxt=content.decode('utf-8')
else:
  print("Error: supply either link or filename but not both")
  exit(0)

#------------------------- commands ------------------------------------

#extract the text part we need and convert it from markup to html
if args.version=='latest':
  html=markdown.markdown("<a name"+str_part(ChLogTxt,"<a name","<a name"))
else:
  html=markdown.markdown('<a name="'+args.version+'">'+str_part(ChLogTxt,'<a name="'+args.version+'">','<a name'))

#call the parser
parser = MyHTMLParser()
parser.feed(html)

#populate our message parameter list with the data extracted with tha parser
msg_params={
          "attachments": parser.attach,
          "channel":args.channel,
          "username":args.username,
          "icon_emoji":args.emoji,
            }


#create a JSON file from our dictionary
JSONobj=json.dumps(msg_params)
#performing the POST request
req = urllib.request.Request('https://hooks.slack.com/services/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')
req.add_header('Content-Type', 'application/json')
d=JSONobj.encode('ascii')
r = urllib.request.urlopen(req, d)
