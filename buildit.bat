pipreqs . --force
pyinstaller poeclog.py --add-data "./poe.png;." --add-data "./templates;templates" --add-data "./css/*;." --add-data "./passive-skill-tree*.json;." --onefile 