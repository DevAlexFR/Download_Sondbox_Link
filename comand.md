
## comand
```shell 
pyinstaller --noconfirm --onefile --windowed --icon "web/assets/css/favicon.ico" --add-data "web;web/" --add-data "project/data;data/" --add-data "project/py_front;py_front/" --add-data "project/pynguin;pynguin/" --add-data "project/x3270;x3270/" --add-data "project/b2k;b2k/" --paths ".venv/Lib/site-packages" --hidden-import "tkinter.filedialog" "project/main.py"
````
