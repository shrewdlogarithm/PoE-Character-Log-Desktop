pipreqs . --print | sort > requirements.txt
pyinstaller poeclog.py --add-data "./poeclog.png;." --add-data "./templates;templates" --add-data "./css/*;." --add-data "./passive-skill-tree*.json;." --icon "poeclog.ico" --onefile 