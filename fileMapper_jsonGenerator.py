import os
import json
import sys

extensions2omit = []

identifier = input('Enter the name of the output JSON file: ')
rootDir = ''
rootSuc = False
outputDirSuc = False
outputDir = ''

while not rootSuc:
    rootDir = input('Enter the path of directory to use as the root: ')
    if rootDir == 'x':
        print('Terminating Session...')
        sys.exit()
    try:
        os.chdir(rootDir)
        rootSuc = True
        break
    except:
        print('Could not change to root directory')
        rootDir = input('Enter the path of directory to use as the root or enter [x] key to terminate: ')

dict = {}

l_root = len(rootDir)
for dir, subdirs, files in os.walk(os.getcwd()):
    for file in files:
        omitFile = False
        isDup = False
        pathNumber = 1
        filename = str(file)
        l = len(filename)
        path = dir[l_root:]

        for extension in extensions2omit:
            e = len(file) - len(extension)
            if file[e:] == extension:
                omitFile = True
        if omitFile:
            continue

        if len(dict) == 0:
            print('L EQUAL TO 0')
            fileInfo = {
                "identifier": identifier,
                "filename": filename,
                "number of paths": str(pathNumber),
                "filepath-" + str(pathNumber): str(path)
            }
            dict[filename] = fileInfo
            print('RUNNING... PLEASE WAIT...')
            continue

        else:
            for key in dict:
                try:
                    if key == filename:
                        pathNumber = int(dict[key]["number of paths"])
                        pathNumber += 1

                        fileInfo = {
                            "number of paths": str(pathNumber),
                            "filepath-" + str(pathNumber): str(path)
                        }
                        isDup = True
                except:
                    isDup = False

        if not isDup:
            fileInfo = {
                "identifier": identifier,
                "filename": filename,
                "number of paths": str(pathNumber),
                "filepath-" + str(pathNumber): str(path)
            }
            dict[filename] = fileInfo
        else:
            dict[filename]["number of paths"] = str(pathNumber)
            dict[filename]["filepath-" + str(pathNumber)] = str(path)

while not outputDirSuc:
    outputDir = input('Enter the path of the output directory (will create a /JSON folder here): ')
    if outputDir == 'x':
        print('Terminating Session...')
        sys.exit()
    try:
        os.chdir(outputDir)
        outputDirSuc = True
        break
    except:
        print('Could not change to output directory')
        rootDir = input('Enter the path of the output directory (will save a JSON file here) \
        or enter [x] key to terminate: ')

json_object = json.dumps(dict, indent=4)
f = open(identifier + "_fileMapper.json", "w")
f.write(json_object)
f.close()