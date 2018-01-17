# changelog-POST-request
Is a small script that creates a slack message from a markup document

## Pre-requisite
Python 3.x

## Install 
```

git clone git@github.com:khirshah/changelog-POST-request.git

```     

## Run
```

python3 slackMsgBuilder.py -ch "#<chanel>" -usr "<usrname>" -em "<emoticon>"

```

### Arguments
```
-ch - chanel on slack
-usr - username to display
-em - emoticon to display as avatar
-lnk - link to changelog file (optional, but either this or -f is required)
-f - file name+location (optional, but either this or -lnk is required)
-ver - version info to display (optional, default: "latest")

```
