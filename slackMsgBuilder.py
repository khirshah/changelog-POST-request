#-------------------------- import -------------------------------
import urllib.request, urllib.parse
import argparse
import markdown
import json
from HTMLParsExt import MyHTMLParser

#-------------------------- init --------------------------------
def str_part(text,d1,d2):
  string=text.partition(d1)[2]
  return string.partition(d2)[0]



argparser = argparse.ArgumentParser()
argparser.add_argument('-ch', '--channel',
                        help='channel to POST to',
                        required='True')
argparser.add_argument('-usr', '--username',
                        help='name of the user',
                        required='True')
argparser.add_argument('-em', '--emoji',
                        help='icon to show',
                        required='True')
args = argparser.parse_args()


with open('changelog.txt') as f:
    ChLogTxt = f.read()

#------------------------- commands ------------------------------------

#extract the text part we need and convert it from markup to html
html=markdown.markdown("<a name"+str_part(ChLogTxt,"<a name","<a name"))

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
