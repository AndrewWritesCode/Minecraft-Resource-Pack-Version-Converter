from fileMapper import FileMapper
import itertools
import json
import csv
import os
from sys import exit


# checks the files and directories, and initializes the pack data
def setup():
    print('Initial setup...')
    input_pack_path = input('What is the root path of the resource pack you want to convert? ')
    print('Mapping resource pack...')
    packname = input('What is the name of your output (will have .json added to the end)? ')
    while True:
        if input_pack_path == 'x':
            print('Terminating Session...')
            exit()
        try:
            input_pack_data = FileMapper(fxnRootDir=input_pack_path)
            break
        except:
            input_pack_path = input("FILEMAPPING ERROR: re-enter the root path of the resource pack you want to convert or enter [x] key to terminate: ")

    reference_pack_path = input('What is the path of your reference JSON file? ')
    while True:
        if reference_pack_path == 'x':
            print('Terminating Session...')
            exit()
        try:
            os.chdir(reference_pack_path.replace(os.path.basename(reference_pack_path), ''))
            if os.path.splitext(os.path.basename(reference_pack_path))[1] != '.json':
                print('Path does not end with .json')
                reference_pack_path = input('FILEMAPPING ERROR: re-enter the path of your reference JSON file or '
                                            'enter [x] key to terminate: ')
                continue
            with open(reference_pack_path) as json_file:
                reference_pack_data = json.load(json_file)
            break
        except:
            reference_pack_path = input('FILEMAPPING ERROR: re-enter the path of your reference JSON file or '
                                       'enter [x] key to terminate: ')
    return input_pack_data, reference_pack_data, reference_pack_path, input_pack_path, packname


# analyzes differences between naming conventions of each pack and tags resource_pack_data to keep note of differences
def conventionsDetector(convert_pack_data, ref_data, mode):
    convention = 0
    path_conv12 = r'\assets\minecraft\textures\blocks' #pathing from 1.12.2
    path_conv16 = r'\assets\minecraft\textures\block' #pathing from 1.16.6


    for key in ref_data:
        for subkey in ref_data[key]:
            if ref_data[key][subkey].startswith(path_conv12):
                convention = 12
                break
            elif ref_data[key][subkey].startswith(path_conv16):
                convention = 16
                break

    # re-paths a version 12 to a version version 16
    if convention == 12:
        for key in convert_pack_data.copy():
            for subkey in convert_pack_data[key].copy():
                outputKey = subkey + '-converted'
                if convert_pack_data[key][subkey].startswith(path_conv16):
                    convert_pack_data[key][outputKey] = convert_pack_data[key][subkey].replace(path_conv16, path_conv12)
                else:
                    convert_pack_data[key][outputKey] = convert_pack_data[key][subkey]

    # re-paths a version 16 to a version version 12
    elif convention == 16:
        for key in convert_pack_data.copy():
            for subkey in convert_pack_data[key].copy():
                outputKey = subkey + '-converted'
                if convert_pack_data[key][subkey].startswith(path_conv12):
                    convert_pack_data[key][outputKey] = convert_pack_data[key][subkey].replace(path_conv12, path_conv16)
                else:
                    convert_pack_data[key][outputKey] = convert_pack_data[key][subkey]
    else:
        if mode == 'terminal':
            conErr = input('Cannot detect proper pathing convention, would you still like to continue? [y/n]: ')
            if conErr.lower() == 'y':
                pass
            else:
                exit()
        else:
            print('Pathing convention error...')
            print('Terminating')
            exit()


# takes 2 list of (sub)words to add, then (sub)words to remove to the wordList
def manualWordSwap(possible_files_list, ref_list, manual_inserts, manual_removes, extension):
    runBool = False
    insertsEmpty = False
    removesEmpty = False
    if manual_inserts == ['']:
        insertsEmpty =True
    if manual_removes == ['']:
        removesEmpty =True
    if manual_removes == ['flower']:
        printOut = True
    i = 0
    # This is so that we only run the script if it can successfully remove all manual removes
    for item in ref_list:
        for manual_remove in manual_removes:
            if item == manual_remove:
                i += 1
    if len(manual_removes) == i:
        runBool = True
    out_list = []
    if runBool or removesEmpty:
        iterList = []
        manualWordList = ref_list.copy()
        if not removesEmpty:
            for manual_remove in manual_removes:
                manualWordList.remove(manual_remove)
        if not insertsEmpty:
            for manual_insert in manual_inserts:
                manualWordList.append(manual_insert)
        for word in range(len(manualWordList)):
            iterList.append(word)
        for p in itertools.permutations(iterList):
            possibleWord = ''
            for n in p:
                possibleWord += manualWordList[n] + '_'
            possibleWord = possibleWord[:-1]
            out_list.append(possibleWord + extension)
            possible_files_list.append(possibleWord + extension)
        if not insertsEmpty:
            for manual_insert in manual_inserts:
                manualWordList.remove(manual_insert)
        if not removesEmpty:
            for manual_remove in manual_removes:
                manualWordList.append(manual_remove)
        return out_list
        # return possibleFilenames


def VerTwelve2Sixteen_manualSwaps(csv_path_, possibleFilenames, wordList, ext):
    first_pass = True
    try:
        with open(csv_path_, newline='') as csv_file:
            manualFileChanges = csv.reader(csv_file, delimiter=',')
            for row in manualFileChanges:
                if first_pass:
                    first_pass = False
                    pass
                else:
                    additions = row[0].split(' ')
                    for entry in additions:
                        if entry == '':
                            additions.remove(entry)
                    removals = row[1].split(' ')
                    for entry in removals:
                        if entry == '':
                            removals.remove(entry)
                    manualWordSwap(possibleFilenames, wordList, additions, removals, ext)
    except:
        # if there are empty lines at the end of the .csv file the program will crash, so try statement catches them
        pass

########################################################################################################################


def MinecraftVersionTranslator(input_pack_data, reference_pack_data, input_pack_path, packname, csv_path = os.getcwd(),
                               reference_pack_path='UNDEFINED', mode='ui'):
    print('RUNNING... PLEASE WAIT...')
    conventionsDetector(input_pack_data, reference_pack_data, mode)
    outputDict = {}
    noMatchDict = {}

    #DEBUG
    if mode != 'ui':
        output_path = reference_pack_path.replace(os.path.basename(reference_pack_path),'')

    for key in input_pack_data:
        for inputSubKey in input_pack_data[key]:
            if inputSubKey.startswith('filepath-') and inputSubKey.endswith('-converted'):
                try:
                    for refSubKey in reference_pack_data[key]:
                        if reference_pack_data[key][refSubKey] == input_pack_data[key][inputSubKey]:
                            fileInfo = {
                                "input filename": key,
                                "input mcmeta filename": 'UNKNOWN',
                                "reference mcmeta filename": 'UNKNOWN',
                                "reference filename": key,
                                "input filepath": input_pack_data[key][inputSubKey.replace('-converted', '')],
                                "reference filepath": reference_pack_data[key][refSubKey]
                            }
                            try:
                                outputDict[inputSubKey + '-' + key] = fileInfo
                            except:
                                print('Dictionary save error!')
                except:
                    inputFileInfo = {
                        "input filename": key,
                        "input mcmeta filename": 'UNKNOWN',
                        "reference mcmeta filename": 'UNKNOWN',
                        "reference filename": 'UNKNOWN',
                        "input filepath": input_pack_data[key][inputSubKey.replace('-converted', '')],
                        "reference filepath": 'UNKNOWN'
                    }
                    noMatchDict[inputSubKey + '-' + key] = inputFileInfo

    for key in noMatchDict.copy():
        input_asset = noMatchDict[key]["input filename"]
        name = os.path.splitext(input_asset)[0]
        extension = os.path.splitext(input_asset)[1]
        wordList = []  # filenames can be broken down into several words separated by an underscore
        word = ''
        for letter in name:
            if letter == '_':
                wordList.append(word)
                word = ''
            else:
                word += letter
        wordList.append(word)
        possibleFilenames = []  # now rearrange all the words into possible keys (equal to the factorial of subwords)
        iterList = []
        for i in range(len(wordList)):
            iterList.append(i)
        for p in itertools.permutations(iterList):
            possible_phrase = ''
            for n in p:
                possible_phrase += wordList[n] + '_'
            possible_phrase = possible_phrase[:-1]  # remove the last '_'
            possibleFilenames.append(possible_phrase + extension)
        VerTwelve2Sixteen_manualSwaps(csv_path, possibleFilenames, wordList, extension)

        for possibleFilename in possibleFilenames:
            try:
                for refKey in reference_pack_data.copy():
                    if possibleFilename == reference_pack_data[refKey]["filename"]:
                        noMatchDict[key]["reference filename"] = possibleFilename
                        mostLikelyPath = 'UNDETERMINED PATH'
                        for refSubKey in reference_pack_data[refKey].copy():
                            if refSubKey.startswith('filepath-'):
                                if reference_pack_data[refKey][refSubKey] == noMatchDict[key]["input filepath"]:
                                    mostLikelyPath = noMatchDict[key]["input filepath"]
                                elif reference_pack_data[refKey][refSubKey] == noMatchDict[key]["input filepath"][:-1]:
                                    mostLikelyPath = noMatchDict[key]["input filepath"][:-1]
                        noMatchDict[key]["reference filepath"] = mostLikelyPath
                        key_prefix = noMatchDict[key]["input filepath"]
                        try:
                            outputDict[key_prefix + '-' + key + '-' + 'resolved'] = noMatchDict[key]
                            del noMatchDict[key]
                        except:
                            print('Dictionary save error!')
            except:
                pass

    # mcmeta checks
    for key in outputDict.copy():
        possible_mcmeta = input_pack_path + '/' + outputDict[key]["input filepath"] + '/' + outputDict[key]["input filename"] + '.mcmeta'
        if os.path.exists(os.path.abspath(possible_mcmeta)):
            outputDict[key]["input mcmeta filename"] = outputDict[key]["input filename"] + '.mcmeta'
            outputDict[key]["reference mcmeta filename"] = outputDict[key]["reference filename"] + '.mcmeta'
            for no_match_key in noMatchDict.copy():
                if noMatchDict[no_match_key]["input filename"] == outputDict[key]["input mcmeta filename"]:
                    del noMatchDict[no_match_key]

    outputDict["json2pack"] = input_pack_path
    if mode == 'ui':
        return outputDict, noMatchDict

    print('SAVING CONSTRUCTOR JSON TO: ' + os.path.join(output_path, packname + '.json'))
    json_object = json.dumps(outputDict, indent=4)
    f = open(os.path.join(output_path, packname + '.json'), "w")
    f.write(json_object)
    f.close()

    print('SAVING NO MATCH JSON TO: ' + os.path.join(output_path, "NoMatch_Conversion.json"))
    json_object = json.dumps(noMatchDict, indent=4)
    f = open(os.path.join(output_path, "NoMatch_Conversion.json"), "w")
    f.write(json_object)
    f.close()

    print('SAVING REMAINING REF JSON TO: ' + os.path.join(output_path, "RemainingRef_Conversion.json"))
    json_object = json.dumps(noMatchDict, indent=4)
    f = open(os.path.join(output_path, "RemainingRef_Conversion.json"), "w")
    f.write(json_object)
    f.close()

    outputCount = 0
    for key in outputDict:
        outputCount += 1
    noMatchCount = 0
    for key in noMatchDict:
        noMatchCount += 1
    print('Found ' + str(outputCount) + ' matches!')
    print('Found ' + str(noMatchCount) + ' with no matches')


# input_pack_data = FileMapper(fxnRootDir='F:/Python_Projects/MineCraft_ResourcePack_Converter/FireLeaf121218 fixed GUI')
# reference_pack_data = FileMapper(fxnRootDir='F:/Python_Projects/MineCraft_ResourcePack_Converter/faithful_packs/Faithful+32x+-+1.16.5')
# input_pack_path = 'F:/Python_Projects/MineCraft_ResourcePack_Converter/FireLeaf121218 fixed GUI'
# packname = 'manualPack'
# outputDict, noMatchDict = MinecraftVersionTranslator(input_pack_data, reference_pack_data, input_pack_path, packname, reference_pack_path='UNDEFINED', mode='ui')
# output_path = 'F:\Python_Projects\MineCraft_ResourcePack_Converter\Python\JSON_templates\sfFIRSRT1111.json'
# json_object = json.dumps(outputDict, indent=4)
# f = open(output_path, "w")
# f.write(json_object)
# f.close()
