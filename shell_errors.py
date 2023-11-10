class FileUndefinedError:
        def __str__(self, file:str):
            return f'[\033[34m E \033[0m] file {file} is undefined or specified wrong path'

class TkinterImportError:
    def __str__(self):
        return '''[\033[34m E \033[0m] Tkinter library is undefined in your system, try one of this commands:
    - pip install tkinter
    - sudo apt install python3-tk
    - apt install python-tkinter
Or if you in Termux, then you need download Pydroid, in Pydroid install Pillow and before this everything will be Ok'''

class TkinterExecuteError:
    def __str__(self):
        return f'[\033[34m E \033[0m] Your environment doesn\'t support tk'

class LibrariesAreUndefinedError:
    def __str__(self):
        return f'[\033[34mE\033[0m] You need to install next libraries:\n\t- pillow\n\t- icecream'

class ScenarioPathError:
    def __str__(self):
        return f'[\033[34mE\033[0m] This scenario isn\'t in true directory or scenario\'s files have wrong names'
