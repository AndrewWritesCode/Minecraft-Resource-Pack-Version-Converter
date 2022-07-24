import os
import json
from sys import exit
import shutil

from fileMapper import FileMapper


def json2pack(json2pack_path, pack_path_root, mode='ui'):
    if mode == 'ui':
        convertDict = json2pack_path


    try:
        os.chdir(pack_path_root)
    except:
        os.mkdir(pack_path_root)
    try:
        os.chdir(pack_path_root)
    except:
        print('Unable to change to directory:')
        print(pack_path_root)
        exit()

        if mode == 'terminal':
            try:
                with open(json2pack_path, encoding="utf-8") as json_file:
                    convertDict = json.load((json_file))
            except:
                exit('Failure to load JSON conversion file...')
        elif mode == 'ui':
            convertDict = json2pack_path
        else:
            print('mode error')
            exit()
    global json2pack_percent_finished
    file_count = -1 #start at -1 to account for the config info
    for key in convertDict:
        file_count += 1


    input_pack_root = convertDict["json2pack"]
    q = ''
    while True:
        if q.lower() == 'x':
            exit('Terminating program...')
        try:
            os.chdir(input_pack_root)
            break
        except:
            if mode == 'temrinal':
                print('Could not change to source pack root directory , define it below, regenerate conversion JSON, '
                      'or enter [x] to exit')
                input_pack_root = input('Enter root of pack here: ')
            else:
                print('Error')
                exit()
    i = 0
    for key in convertDict:
        i += 1
        try:
            if convertDict[key]["reference filepath"] == "UNDEFINED":
                continue
        except:
            pass # one of the entries will contain config info, pass over this entry
        else:
            src = input_pack_root + '/' + convertDict[key]["input filepath"] + '/' + convertDict[key]["input filename"]
            src = os.path.abspath(str(src))
            dst = pack_path_root + '/' + convertDict[key]["reference filepath"] + '/' + convertDict[key]["reference filename"]
            dst = os.path.abspath(str(dst))
            dst_path = pack_path_root + '/' + convertDict[key]["reference filepath"]
            dst_path = os.path.abspath(str(dst_path))
            try:
                os.chdir(dst_path)
            except:
                os.makedirs(dst_path)
                os.chdir(dst_path)
            shutil.copyfile(src, dst)

            #checks for .mcmeta file
            if convertDict[key]["input mcmeta filename"] != 'UNKNOWN':
                src = input_pack_root + '/' + convertDict[key]["input filepath"] + '/' + convertDict[key]["input mcmeta filename"]
                src = os.path.abspath(str(src))
                dst = pack_path_root + '/' + convertDict[key]["reference filepath"] + '/' + convertDict[key][
                    "reference mcmeta filename"]
                dst = os.path.abspath(str(dst))
                dst_path = pack_path_root + '/' + convertDict[key]["reference filepath"]
                dst_path = os.path.abspath(str(dst_path))
                try:
                    os.chdir(dst_path)
                except:
                    os.makedirs(dst_path)
                    os.chdir(dst_path)
                shutil.copyfile(src, dst)

            json2pack_percent_finished = i / file_count