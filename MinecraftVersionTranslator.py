from fileMapper import fileMapper
import itertools
import json
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
            input_pack_data = fileMapper(fxnRootDir=input_pack_path)
            break
        except:
            input_pack_path = input("FILEMAPPING ERROR: re-enter the root path of the resource pack you want to convert or enter [x] key to terminate: ")

    reference_pack_path = input('What is the path of your reference JSON file? ')
    # reference_pack_path = r'F:\Python_Projects\MineCraft_ResourcePack_Converter\JSON\1.16.5_resourcePackConventions.json'
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

# takes 2 list of (sub)words to add, then (sub)words to remove to the wordList
def manualWordSwap(ref_list, manual_inserts, manual_removes, extension):
    runBool = False
    i = 0
    for item in ref_list:
        for manual_remove in manual_removes:
            if item == manual_remove:
                i += 1
    if len(manual_removes) == i:
        runBool = True

    if runBool:
        iterList = []
        manualWordList = ref_list.copy()
        for manual_remove in manual_removes:
            manualWordList.remove(manual_remove)
        for manual_insert in manual_inserts:
            manualWordList.append(manual_insert)
        for i in range(len(manualWordList)):
            iterList.append(i)
        for p in itertools.permutations(iterList):
            possibleWord = ''
            for n in p:
                possibleWord += manualWordList[n] + '_'
            possibleWord = possibleWord[:-1]
            possibleFilenames.append(possibleWord + extension)
        for manual_insert in manual_inserts:
            manualWordList.remove(manual_insert)
        for manual_remove in manual_removes:
            manualWordList.append(manual_remove)
        return possibleFilenames

def VerTwelve_manualSwaps(possibleFilenames, wordList, ext):
    #possibleFilenames.append(manualWordSwap(wordList, ['inserts'], ['removals], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['block'], [], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stained'], [], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stone', 'bricks'], ['stonebrick'], ext))
    possibleFilenames.append(manualWordSwap(wordList, [], ['colored'], ext))
    possibleFilenames.append(manualWordSwap(wordList, [], ['base'], ext))
    possibleFilenames.append(manualWordSwap(wordList, [], ['damaged', '0'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['chipped'], ['damaged', '1'], ext))
    possibleFilenames.append(manualWordSwap(wordList, [], ['2'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stage0'], ['stage', '0'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stage1'], ['stage', '1'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stage2'], ['stage', '2'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stage3'], ['stage', '3'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stage4'], ['stage', '4'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stage5'], ['stage', '5'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stage6'], ['stage', '6'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stage7'], ['stage', '7'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['stage8'], ['stage', '8'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['bottom'], ['lower'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['top'], ['upper'], ext))
    possibleFilenames.append(manualWordSwap(wordList, [], ['flower'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['terracotta'], ['hardened', 'stained', 'clay'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['tall'], ['double', 'plant'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['redstone'], ['off', 'redstone'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['oak'], ['wood'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['oak', 'bottom'], ['wood', 'lower'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['oak', 'top'], ['wood', 'upper'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['trapdoor', 'oak'], ['trapdoor'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['tripwire'], ['trip', 'wire'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['tripwire', 'hook'], ['trip', 'wire', 'source'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['note', 'block'], ['noteblock'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['corner'], ['turned', 'normal'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['rail'], ['rail', 'normal'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['on'], ['powered'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['powered', 'on'], ['golden', 'powered'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['powered'], ['golden'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['torch'], ['on', 'torch'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['grass'], ['tallgrass'], ext))
    possibleFilenames.append(manualWordSwap(wordList, ['wooden'], ['wood'], ext))

# analyzes differences between naming conventions of each pack and tags resource_pack_data to keep note of differences
def conventionsDetector(convert_pack_data, ref_data):
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
        conErr = input('Cannot detect proper pathing convention, would you still like to continue? [y/n]: ')
        if conErr.lower() == 'y':
            pass
        else:
            exit()

########################################################################################################################
input_pack_data, reference_pack_data, reference_pack_path, input_pack_path, packname = setup()
print('RUNNING... PLEASE WAIT...')
conventionsDetector(input_pack_data, reference_pack_data)
outputDict = {}


namePathMatchCount = 0
nameMatchNoPathCount = 0
noMatchCount = 0
rewordCount = 0
manualRewordCount = 0
noMatchDict = {}
entryCount = 0

#DEBUG
output_path = reference_pack_path.replace(os.path.basename(reference_pack_path),'')

for key in input_pack_data:
    for inputSubKey in input_pack_data[key]:
        if inputSubKey.startswith('filepath-') and inputSubKey.endswith('-converted'):
            try:
                for refSubKey in reference_pack_data[key]:
                    if reference_pack_data[key][refSubKey] == input_pack_data[key][inputSubKey]: ####
                        fileInfo = {
                            "input filename": key,
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
    VerTwelve_manualSwaps(possibleFilenames, wordList, extension)

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

outputDict["json2pack"] = input_pack_path

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

print('SAVING REMAINING RED JSON TO: ' + os.path.join(output_path, "RemainingRef_Conversion.json"))
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


