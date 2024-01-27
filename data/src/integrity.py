import os


Ignore = ['__pycache__','.git','.github','.vscode','save','plugins']
NeedFolder = [
    "data","assets","musics","src","data","handler"
]
NeedFiles = [
    "auto_installer.py","camera.py","screens.py","game.py","config.py","integrity.py","player.py","world.py","requirements.txt","lines_counter.py"
]

def ForItemInDir(path):
    Folders = []
    Files = []
    Found = {
         'Folders':[],
         'Files':[]
    }
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            if item not in Ignore:
                Folders.append(item)
                NewFound = ForItemInDir(os.path.join(path, item))
                Files += NewFound['Files']
                Folders += NewFound['Folders']
        elif os.path.isfile(os.path.join(path, item)):
                if item not in Ignore:
                    if item in NeedFiles:
                        Files.append(item)

    Found['Folders'] = Folders
    Found['Files'] = Files
    return Found

def check(Found:dict['Folders':[],'Files':[]]):
    print('[Integrity] Start Checking...')
    print(f'[Integriy] Checking: {Found}') 
    Allright = True
    for Folder in NeedFolder:
        if Folder not in Found['Folders']:
            Allright = False
            print(f"[Integrity] Error: {Folder} Is Not In Folders Found Here.")

    for File in NeedFiles:
        if File not in Found['Files']:
            Allright = False
            print(f"[Integrity] Error: {File} Is Not In Files Found Here.")

    if Allright:
        print('[Integrity] All Right. Good Game.')
    else:
        print('[Integrity] Error: Some Files Or Folders Are Missing.')
    return Allright

def IntegrityCheck(path):
    return check(ForItemInDir(path))

if __name__ == '__main__':
    print(check(ForItemInDir('./')))