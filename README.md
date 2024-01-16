# Justia Doc Formatter


## SetUp
Install python first

Ativate de dev env in python 
```bash
python -m venv content-generator-env
source  content-generator-env/bin/activate
```

Deactivate de env
```bash
deactivate
```

Run Requirements to install dependencies
```python
 python -m pip install -r requirements.txt
```

You need in your "My documents" a directory call "justia" the process is inside the justia dir create your ticket directory with the name of the ticket inside that folder create a directory call files and there add all your files

Example:

Documents>justia>WXN-53693-936>files>[ all files ]

Then run
```python
 python main.py start
```
