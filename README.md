# PoE-Character-Log-Desktop #
## Path of Exile Character Log - track your own PoE characters as you play ##

This is VERY much work-in-progress - sharing for feedback/ideas!

### What it Does ###
It lives in your task tray monitoring your PoE client.txt
When it detects an active character changing zone, it logs XP, passives and gear for that character

We use this data to...
 * Create a 'Build Log' showing changes to the character over-time (txt and HTML)
 * Create a Path-of-Building pastecode/XML file using the same data
 
This is basically a 'desktop' version of https://github.com/shrewdlogarithm/PoE-Character-Log-Python - there's [video here (YouTube Link)](https://www.youtube.com/watch?v=Mje0pl9L8sY) explaining that but I intend to add more 'local' features as I get time.

## How to Use ##
You can either run this as Python source or download a binary release version for your platform (if available - see below)

This will create an icon in your task-tray (and whilst testing, a console window to show errors)
You're now tracking your characters in the background - you can use the tray menu to view the log, your characters, change settings and close the program 
Note: it this upto 5secs to close everything gracefully - be patient!

## First time Setup ##
First run will create "settings.json" - edit that file (or use the Settings option in the tray menu) to assign...
 * Your account name (login name for PoE NOT a character name)
 * The full path to your PoE/logs/client.txt file (e.g. c:\\program files\\path of exile\\logs/client.txt) << Note use either \\ or / as separators and include client.txt at the end!

## How it works ##
By tracking client.txt it knows when you zone - after each zone it queries your character profile and if you've earned XP it logs how much you earned since the last check
It also queries your gear/passives and stores those in JSON format in the data/ directory
A DB of your chars is also kept in accountdb.json for easy access

## Additional 'local' features ##
 * Watches your clipboard for "Ctrl-C"ed Maps - if it finds one, it shows the details of the map in your log - so you can track the map against XP gained
 * more features coming soon - ideas welcomed!

## What are all the files created? ##
In the 'data' directory 
JSON files - a complete dump of API data for Tree, Skills and Items - 1 entry per scan

In the "logs" directory 
LOG files - textfiles detailing changes made to a character over-time
HTML files - the same content as the LOG but hyperlinked/colourized 

In the "pob/builds" directory 
XML - a Path-of-Building-compatible savefile 

## Binary Releases ##
I will build Windows binaries for this (via pyinstaller) periodically
I don't have the resources to build and test Linux and MACOS releases - if anyone else could do that, let me know (buildit.bat is the Windows build command)

## Known Issues ##
If the task-tray/program won't close - close your browser, this usually frees the server to close...
