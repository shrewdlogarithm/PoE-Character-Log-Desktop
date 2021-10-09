# PoE-Character-Log-Desktop #
## Path of Exile Character Log - track your own PoE characters as you play ##

This is VERY much work-in-progress - sharing for feedback/ideas!

### What it Does ###
It lives in your task tray monitoring your PoE client.txt
When it detects an active character 'zoning', it logs XP, passives and gear for that character

This then...
Creates a 'Build Log' showing changes to the character over-time (txt and HTML)
Creates a Path-of-Building file using the  same data

It's a 'desktop' version of the server-based https://github.com/shrewdlogarithm/PoE-Character-Log-Python - there's video here explaining that

[PoEClog in less than 60s (YouTube Link)](https://www.youtube.com/watch?v=Mje0pl9L8sY)

## How to Use ##
You can either run this as Python source or download a release version for your platform.
At this point only a Windows release is available - if MacOS/Linux users would like to build/test a release for those (pyinstaller) please get-in-touch!

Once run, there's an icon in your task-tray - this tracks your characters in the background - you can view the log ad exit from the task-tray menu...  

The first time you run it creates "settings.json" - edit that (or use the Settings option in the tray menu) to  set
Your account name (login name for PoE NOT a character name)
The  path to your PoE/logs/client.txt file (e.c. c:\\program files\\path of exile\\logs/client.txt) << Note use either \\ or / as separators

## What it creates ##
In the 'data' directory 
JSON files which are a complete dump of API data for Tree, Skills and Items - 1 entry per scan

In the "logs" directory 
LOG files - textfiles detailing changes made to a character over-time
HTML files - the same content as the LOG but hyperlinked/colourized 

In the "pob/builds" directory 
XML - a Path-of-Building-compatible savefile 

## Known Issues ##
Probably LOADS of these - this is the first release - do let me know what you find!