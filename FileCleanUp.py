from shutil import move, unpack_archive, rmtree
import os
import json
import sys

"""
Credits:
JoshesMom
FlareGood
"""

#FUNCTIONS
def update_cfg(edit_key: str, key: str, value: str):
    with open('config.json', 'r+') as cfg:
        data: dict = json.load(cfg)
        data[edit_key].update({key: value})
        cfg.seek(0)
        json.dump(data, cfg)
        cfg.truncate()

def get_cfg(dir_or_ext) -> dict:
    with open('config.json', 'r') as cfg:
        data: dict = json.load(cfg)
        cfg.close()
        return data[dir_or_ext]

def auto_unzip(ext, cwd, path):
    if ext == '.zip':
        unpack_archive(f'{cwd}/{path}', cwd)
        os.remove(f'{cwd}\{path}')

def try_move(file_path, new_path):
    try:
        move(file_path, new_path)
    except:
        if os.path.isdir(file_path):
            rmtree(file_path)
        else:
            os.remove(file_path)
        print(f'{os.path.basename(file_path)} already exists at:\n{new_path}\nRemoved the Duplicate')

def manual():
    cwd: str = input('What folder would you like to sort: ')
    for path in os.listdir(cwd):
        
        ext: str = os.path.splitext(path)[-1].lower()


        #auto unzip
        auto_unzip(ext, cwd, path)
        
        if ext == '.tmp' or ext == '.opdownload':
            pass

        else:
            #if ext
            if ext:

                ext_path = get_cfg('ext_path')
                #use config path if possible
                if ext in ext_path.keys():
                    try_move(f'{cwd}/{path}', ext_path[ext])
                
                else:
                    new_dir_path = input(f'Path to where {ext} files should be sent to: ')
                    try_move(f'{cwd}/{path}', new_dir_path)
                    update_cfg('ext_path', ext, new_dir_path)
                

            
            #if dir
            else:
                dir_path = get_cfg('dir_path')
                prompt: str = 'Choose a file path option, or provide a new file path:\n'
                for key in dir_path: 
                    prompt += f'{key}. {dir_path[key]}\n'
                new_dir_path = input(prompt)

                #use config path if possible
                if new_dir_path in dir_path.keys():
                    try_move(f'{cwd}/{path}', dir_path[new_dir_path])

                
                else: 
                    try_move(f'{cwd}/{path}', new_dir_path)
                    update_cfg('dir_path', '1' if len(list(dir_path.keys())) == 0 else str(int(list(dir_path.keys())[-1])+1), new_dir_path)

def automatic(cwd):
    while True:
        for path in os.listdir(cwd):
            ext: str = os.path.splitext(path)[-1].lower()
            auto_unzip(ext, cwd, path)
            if ext == '.tmp' or ext == '.opdownload':
                pass
            elif ext:
                ext_path = get_cfg('ext_path')
                if ext in ext_path.keys() and os.path.exists(f'{cwd}\{path}'):
                        try_move(f'{cwd}\{path}', ext_path[ext])
             
def main(arg):
    
    if arg[1:]:
        print('running automatically')
        automatic(arg[1])
    else:
        manual()


if __name__ == '__main__':
    main(sys.argv)
    