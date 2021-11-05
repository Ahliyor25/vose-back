from flask import request

img =   request.files.getlist('img')

if img is None:
    print("No file")    
