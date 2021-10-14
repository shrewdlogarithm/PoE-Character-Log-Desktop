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
You can either run this as Python source or download a binary release version for your platform (if available - see below)

This should create an icon in your task-tray - this tracks your characters in the background - you can use it's menu to view the log, character details, change settings and close the program (this takes upto 5secs to close everything gracefully)

The first time you run it creates "settings.json" - edit that (or use the Settings option in the tray menu) to  set
Your account name (login name for PoE NOT a character name)
The  path to your PoE/logs/client.txt file (e.c. c:\\program files\\path of exile\\logs/client.txt) << Note use either \\ or / as separators

## What it does ##
Creates a log of every character change/zone change you do - it also shows how much of a level's XP you earned in your last area.
When you zone it queries your character profile and if you've earned XP it stores your gear/passives - from which we can make PoBs/Build Logs etc.
It also watches your clipboard for "Ctrl-C"ed Maps - if it finds one, it shows this in your log too

## What it creates ##
In the 'data' directory 
JSON files which are a complete dump of API data for Tree, Skills and Items - 1 entry per scan

In the "logs" directory 
LOG files - textfiles detailing changes made to a character over-time
HTML files - the same content as the LOG but hyperlinked/colourized 

In the "pob/builds" directory 
XML - a Path-of-Building-compatible savefile 

## Binary Releases ##
I will build Windows binaries for this (via pyinstaller) periodically - I don't have the time/resources to build and test Linux and MACOS ones tho - if anyone else would liek to do that, let me know (buildit.bat is the Windows build command)

## Known Issues ##
If the task-tray/program won't close - check you don't have a page open in a browser, this can keep the server alive/stop the program ending cleanly.