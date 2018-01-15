from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    #declare variables and containers
    attach=[
        {
            "color": "#36a64f",
            "title": "",
            "title_link": "",
            "fields": []
        }
    ]

    current_tag_list = []

    text_list = []

    h3TagCount = -1

    def handle_starttag(self, tag, attrs):
        #add tag to the current_tag_list
        self.current_tag_list.append(tag)
        #get the first title and link from the text and extract them as attachment title and link
        for attr in attrs:
            if tag=="a":
                if attr[0]=="name" and self.attach[0]["title"]=="":
                    self.attach[0]["title"]=attr[1]
                elif attr[0]=="href"and self.attach[0]["title_link"]=="":
                    self.attach[0]["title_link"]=attr[1]

    def handle_endtag(self, tag):
        #remove tag from current_tag_list
        self.current_tag_list.pop()

    def handle_data(self, data):
        #extract text, remove empty and incomplete strings and (-s from end of strings
        if "a" not in self.current_tag_list and data!=') (' and data.startswith(')')==False and data!=None and len(data)>1 and self.h3TagCount != -1:
            if "h3" not in self.current_tag_list and "h1" not in self.current_tag_list:
                if data.startswith(" "):
                    self.text_list[self.h3TagCount].append(data[1:-2])
                    self.attach[0]["fields"][self.h3TagCount]["value"]=self.attach[0]["fields"][self.h3TagCount]["value"]+"\n- "+data[1:-2]
                elif data.startswith(", "):
                    self.text_list[self.h3TagCount].append(data[2:-2])
                    self.attach[0]["fields"][self.h3TagCount]["value"]=self.attach[0]["fields"][self.h3TagCount]["value"]+"\n- "+data[2:-2]
                else:
                    self.text_list[self.h3TagCount].append(data[0:-2])
                    self.attach[0]["fields"][self.h3TagCount]["value"]=self.attach[0]["fields"][self.h3TagCount]["value"]+"\n- "+data[0:-2]
        #if tag happens to be H3, save text as field name
        if "h3" in self.current_tag_list:
            #first create list element Field and the corresponding Text block
            self.text_list.append([])
            self.attach[0]["fields"].append({"value":""})
            #increase number of items index by 1
            self.h3TagCount+=1
            #extract title text and set field as long (slack syntax)
            self.attach[0]["fields"][self.h3TagCount]["title"]=data
            self.attach[0]["fields"][self.h3TagCount]["short"]= False

