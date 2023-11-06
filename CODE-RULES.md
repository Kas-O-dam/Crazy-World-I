
<h1>If you want countributing</h1>
1) Pydroid and Python 3.5 in Astra Linux don't like "match" constructions and throw error. Don't use match/case<br/>
2) You must give big but understandable names of vars, but try choose the shortest variant, "button_instance" or simple "button" is better, then "tkinter_button_python_instance_in_some_coordinates_in_main_window".
<pre>
    Bad     Good
    
    btn     button
    cls     class
    ctx     context
    cnv     canvas
    
    But
    
    tkinter => tk
    implementation => impl
</pre>
Also you can use letters i, j, x, y, etc. in cycles
3) Only_snake_syntax
4) You can write comments how and where you can
```Python
class Peoples: #(in line)it is people of some country
    #(before line)init function
    def __init__(self, ...):
        #(after line)init function
        ...
```
5) If you can divide some to parts - do it like here
```Python
def create_settings_window(...):
#![INIT WINDOW]
    settings_window = tk.TK()
    settings_window.geometry(...)
    settings_window.title(...)
    ... #big code
    
#![CREATING SOME BUTTON]
    some_button = tk.Button(...)
    some_button.config(...)
    ... #big code yet
    
#![PLACING AND SHOWING]
    some_button.pack()
    settings_window.mainloop()
```
Such comments need, when code become big and hard oriantable
6) If you want to create some file, then call its in "kebab syntax" it is like snake, but "_" replace to "-": i-m-script.py, i-save-data.json
