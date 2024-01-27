import os

PATH_DATA = './data/'

Readable = ['md','txt','py','pyplugin','json','html','js','gitignore']
Ignore = ['__pycache__']

def ForItemInDir(path):
    Lines = 0
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            if item not in Ignore:
                Lines+=ForItemInDir(os.path.join(path, item))
        else:
            ty = item.split('.')[-1]
            if ty in Readable:
                with open(os.path.join(path, item), 'r') as f:
                    Lines += len(f.readlines())

    return Lines