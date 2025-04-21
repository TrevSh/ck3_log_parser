# 🛠️ CK3 Log Parser

A desktop GUI tool for parsing and viewing **Crusader Kings III logs**. Built in Python.

This tool helps modders and developers debug their mods by visualizing error, debug, and game logs in a user-friendly format.

##### Early Access Screenshot below.
![image](https://github.com/user-attachments/assets/fe40aa10-f0c8-4dc7-bf8d-5bfd534ee5d9)



## ✨ Features

- ✅ Parse `error.log`, `debug.log`, and `game.log` from the CK3 logs directory
- ✅ View logs in a searchable, sortable table
- ✅ Filter logs by type (Error, Debug, Game) (**only Error works for right now**)
- ✅ Load custom log folder paths
- ✅ One-click executable build (Windows)

## Roadmap/To-Do 

- [ ] Remove uneeded values from Message column
- [ ] Expand functionality to Debug, Game, and **Crash** logs
- [ ] Collect feedback from community
- [ ] Make tool more accessible during development

## 📦 Installation (Development)

```bash
git clone https://github.com/yourname/ck3-log-parser.git
cd ck3-log-parser
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
