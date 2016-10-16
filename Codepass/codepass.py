#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from base64 import b64encode
import json


def encode():
    passwd = entry.get()
    passwd = b64encode(passwd)
    entry.delete(0, END)
    entry.insert(0, passwd)


def clean():
    entry.delete(0, END)


def cpclipboard():
    root.clipboard_clear()
    root.clipboard_append(entry.get())


LANGUAGE = "en"

with open('language.json') as json_file:
    data = json.load(json_file, encoding="utf-8")

root = Tk()
root.title('Codepass')
root.iconbitmap('key.ico')
Label(text=data[LANGUAGE]['label']).pack(side=TOP, padx=10, pady=10)
entry = Entry(root, width=30)
entry.pack(side=TOP, padx=5, pady=5)
Button(root, text=data[LANGUAGE]['codeBtn'], command=encode).pack(side='left')
Button(root, text=data[LANGUAGE]['cleanBtn'], command=clean).pack(side='left')
Button(root, text=data[LANGUAGE]['cpclipboardBtn'], command=cpclipboard).pack(side='left')

entry.focus()
root.bind("<Return>", lambda event: encode())
root.resizable(0, 0)
root.mainloop()
