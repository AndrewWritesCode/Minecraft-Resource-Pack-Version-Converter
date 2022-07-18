import os
import json
from sys import exit


def FileMapper(mode='function', fxnRootDir='', fxnJsonPath='', exts2omit=[]):
    if mode == 'function':
        rootDir = fxnRootDir
        jsonPath = fxnJsonPath
        jsonFilename = os.path.basename(jsonPath)
        try:
            os.chdir(rootDir)
        except:
            print('Unable to change to root directory')
            print('Terminating Session...')
            exit()

        if jsonFilename[:-5] != '.json':
            print('JSON filename does not end with .json')
            print('Terminating Session...')
            exit()

        try:
            fl = len(jsonFilename) + 1
            outputDir = jsonPath[:-fl]
            os.chdir(outputDir)
        except:
            print('Unable to change to output directory')
            print('Terminating Session...')
            exit()

    elif mode == 'terminal':
        rootSuc = False
        outputDirSuc = False
        extSuc = False

        while not rootSuc:
            rootDir = input('Enter the path of directory to use as the root: ')
            if rootDir == 'x':
                print('Terminating Session...')
                exit()
            try:
                os.chdir(rootDir)
                rootSuc = True
                break
            except:
                print('Could not change to root directory')
                rootDir = input('Enter the path of directory to use as the root or enter [x] key to terminate: ')

        jsonPath = input('Define path of the JSON file to be generated (include filename and .json): ')
        jsonFilename = os.path.basename(jsonPath)
        fl = len(jsonFilename) + 1
        outputDir = jsonPath[:-fl]
        while not outputDirSuc:
            if jsonPath == 'x':
                print('Terminating Session...')
                exit()
            try:
                outputDir = jsonPath[:-fl]
                os.chdir(outputDir)
                outputDirSuc = True
                break
            except:
                print('Could not change to output directory')
                jsonPath = input('Define path of the JSON file to be generated or enter [x] key to terminate \
                (include filename and .json): ')

        while not extSuc:
            if jsonFilename[(len(jsonFilename)-5):] == '.json':
                extSuc = True
            else:
                print('JSON filename does not end with .json')
                oldFilenameLength = len(jsonFilename)
                jsonFilename = input('Define JSON filename (without path): ')
                jsonPath = os.path.join(outputDir, jsonFilename)

        listingExt = False
        while True:
            if not listingExt:
                extQ = input('Would you like to omit certain file extension from your file map? [y/n]: ')
            if extQ.lower() == 'y':
                extOmission = input('Enter [STOP] to finish or enter a file extension that you would like to omit from your file map (such as .py, .cpp, etc): ')
                listingExt = True
                if extOmission.upper() == 'STOP':
                    break
                exts2omit.append(str(extOmission))
                print('Omitting ' + extOmission + ' from file map...')
            elif extQ.lower() == 'n':
                print('Including all file extensions')
                break
            else:
                print('Please answer question with [y/n]...')

    else:
        print('mode was not properly define, check spelling.')
        print('The following modes are available:')
        print('function')
        print('terminal')
        exit()

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

            for extension in exts2omit:
                e = len(file) - len(extension)
                if file[e:] == extension:
                    omitFile = True
            if omitFile:
                continue

            if len(dict) == 0:
                fileInfo = {
                    "filemapper_json": jsonFilename,
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
                    "filemapper_json": jsonFilename,
                    "filename": filename,
                    "number of paths": str(pathNumber),
                    "filepath-" + str(pathNumber): str(path)
                }
                dict[filename] = fileInfo
            else:
                dict[filename]["number of paths"] = str(pathNumber)
                dict[filename]["filepath-" + str(pathNumber)] = str(path)

    json_object = json.dumps(dict, indent=4)
    f = open(jsonPath, "w")
    f.write(json_object)
    f.close()


FileMapper(mode='terminal')
