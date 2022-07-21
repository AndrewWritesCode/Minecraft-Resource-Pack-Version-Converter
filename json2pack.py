import os
import json
from sys import exit
import shutil


print('You will need a .json file generated from MinecraftVersionTranslator.py before running this script')
print('You will also need to be sure there is not a folder with the same name as your.json file in the same directory')
json2pack_path = input('What is the path of your .json file? ')
pack_path_root = json2pack_path.replace(os.path.basename(json2pack_path), '')
pack_folder = os.path.basename(json2pack_path)
pack_folder = os.path.splitext(pack_folder)[0]
pack_path_root = os.path.join(pack_path_root, pack_folder)
fileCount = 0
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
try:
    with open(json2pack_path, encoding="utf-8") as json_file:
        convertDict = json.load((json_file))
except:
    exit('Failure to load JSON conversion file...')

input_pack_root = convertDict["json2pack"]
q = ''
while True:
    if q.lower() == 'x':
        exit('Terminating program...')
    try:
        os.chdir(input_pack_root)
        break
    except:
        print('Could not change to source pack root directory , define it below, regenerate conversion JSON, '
              'or enter [x] to exit')
        input_pack_root = input('Enter root of pack here: ')

for key in convertDict:
    try:
        if convertDict[key]["reference filepath"] == "UNDEFINED":
            continue
    except:
        print('string error')
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
        os.chdir('F:')
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
            os.chdir('F:')
            shutil.copyfile(src, dst)


