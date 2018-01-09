#-------------------------------- import ----------------------------------------
import urllib.request, urllib.parse
import argparse
import markdown
import json
import html5lib

#--------------------------------- init -----------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('-ch', '--channel',
                        help='channel to POST to',
                        required='True')
parser.add_argument('-usr', '--username',
                        help='name of the user',
                        required='True')
parser.add_argument('-em', '--emoji',
                        help='icon to show',
                        required='True')
args = parser.parse_args()


with open('changelog.txt') as f:
    data = f.read()

#------------------------------ functions --------------------------------------
def str_part(text,d1,d2):
  string=text.partition(d1)[2]
  return string.partition(d2)[0]

#------------------------------dictionaries -------------------------------------
attach=[
  {
            "title": "",
            "title_link": "",
  }
]

dictionary={
"attachments": attach,
"channel":args.channel,
"username":args.username,
"icon_emoji":args.emoji

}


#---------------------------- HTML parsing ---------------------------------
#-- cut text then markdown--
htmltxt=markdown.markdown("<a name"+str_part(data,"<a name","<a name"))
#-- parse html --
d = html5lib.parse(htmltxt)
#-- find all elements in the etree
s = d.findall('.//')
#-- iterate over the element and select the first name and href tags
#-- save values to attach dict
for i in s:
    if i.attrib != {}:
        if 'name' in i.attrib and attach[0]['title']=="":
            attach[0]['title']="Change log - " + i.attrib['name']
        if 'href' in i.attrib and attach[0]['title_link']=="":
            attach[0]['title_link'] = i.attrib['href']
    print(i.text)

print(attach)

#-------------------------- dict conversion to JSON ------------------------------
JSONobj=json.dumps(dictionary)
print(type(JSONobj),"\n",JSONobj)

#-------------------------- POST request ------------------------------------------
req = urllib.request.Request('https://hooks.slack.com/services/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')
req.add_header('Content-Type', 'application/json')
d=JSONobj.encode('ascii')
r = urllib.request.urlopen(req, d)
