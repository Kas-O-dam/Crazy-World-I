class FileUndefinedError():
		def __init__(self, file:str):
			self.file = file
		def __str__(self):
			return f'[\033[34mE\033[0m] file {self.file} is undefined or specified wrong path'

class TkinterImportError():
    def __str__(self):
        return '''[\033[34mE\033[0m] Tkinter library is undefined in your system, try one of this commands:
    - pip install tkinter
    - sudo apt install python3-tk
    - apt install python-tkinter
Or if you in Termux, then you need download Pydroid, in Pydroid install Pillow and before this everything will be Ok'''

