import itertools


# takes 2 list of (sub)words to add, then (sub)words to remove to the wordList
def manualWordSwap(possible_files_list, ref_list, manual_inserts, manual_removes, extension):
    runBool = False
    i = 0
    for item in ref_list:
        for manual_remove in manual_removes:
            if item == manual_remove:
                i += 1
    if len(manual_removes) == i:
        runBool = True
    out_list = []
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
            out_list.append(possibleWord + extension)
            possible_files_list.append(possibleWord + extension)
            #PossibleFilenames.append(possibleWord + extension)
        for manual_insert in manual_inserts:
            manualWordList.remove(manual_insert)
        for manual_remove in manual_removes:
            manualWordList.append(manual_remove)
        return out_list
        # return possibleFilenames

def VerTwelve_manualSwaps(possibleFilenames, wordList, ext):
    #possibleFilenames.append(manualWordSwap(wordList, ['inserts'], ['removals], ext))
    manualWordSwap(possibleFilenames, wordList, ['block'], [], ext)
    manualWordSwap(possibleFilenames, wordList, ['stained'], [], ext)
    manualWordSwap(possibleFilenames, wordList, ['stone', 'bricks'], ['stonebrick'], ext)
    manualWordSwap(possibleFilenames, wordList, [], ['colored'], ext)
    manualWordSwap(possibleFilenames, wordList, [], ['base'], ext)
    manualWordSwap(possibleFilenames, wordList, [], ['damaged', '0'], ext)
    manualWordSwap(possibleFilenames, wordList, ['chipped'], ['damaged', '1'], ext)
    manualWordSwap(possibleFilenames, wordList, [], ['2'], ext)
    manualWordSwap(possibleFilenames, wordList, ['stage0'], ['stage', '0'], ext)
    manualWordSwap(possibleFilenames, wordList, ['stage1'], ['stage', '1'], ext)
    manualWordSwap(possibleFilenames, wordList, ['stage2'], ['stage', '2'], ext)
    manualWordSwap(possibleFilenames, wordList, ['stage3'], ['stage', '3'], ext)
    manualWordSwap(possibleFilenames, wordList, ['stage4'], ['stage', '4'], ext)
    manualWordSwap(possibleFilenames, wordList, ['stage5'], ['stage', '5'], ext)
    manualWordSwap(possibleFilenames, wordList, ['stage6'], ['stage', '6'], ext)
    manualWordSwap(possibleFilenames, wordList, ['stage7'], ['stage', '7'], ext)
    manualWordSwap(possibleFilenames, wordList, ['stage8'], ['stage', '8'], ext)
    manualWordSwap(possibleFilenames, wordList, ['bottom'], ['lower'], ext)
    manualWordSwap(possibleFilenames, wordList, ['top'], ['upper'], ext)
    manualWordSwap(possibleFilenames, wordList, [], ['flower'], ext)
    manualWordSwap(possibleFilenames, wordList, ['terracotta'], ['hardened', 'stained', 'clay'], ext)
    manualWordSwap(possibleFilenames, wordList, ['tall'], ['double', 'plant'], ext)
    manualWordSwap(possibleFilenames, wordList, ['redstone'], ['off', 'redstone'], ext)
    manualWordSwap(possibleFilenames, wordList, ['oak'], ['wood'], ext)
    manualWordSwap(possibleFilenames, wordList, ['oak', 'bottom'], ['wood', 'lower'], ext)
    manualWordSwap(possibleFilenames, wordList, ['oak', 'top'], ['wood', 'upper'], ext)
    manualWordSwap(possibleFilenames, wordList, ['trapdoor', 'oak'], ['trapdoor'], ext)
    manualWordSwap(possibleFilenames, wordList, ['tripwire'], ['trip', 'wire'], ext)
    manualWordSwap(possibleFilenames, wordList, ['tripwire', 'hook'], ['trip', 'wire', 'source'], ext)
    manualWordSwap(possibleFilenames, wordList, ['note', 'block'], ['noteblock'], ext)
    manualWordSwap(possibleFilenames, wordList, ['corner'], ['turned', 'normal'], ext)
    manualWordSwap(possibleFilenames, wordList, ['rail'], ['rail', 'normal'], ext)
    manualWordSwap(possibleFilenames, wordList, ['on'], ['powered'], ext)
    manualWordSwap(possibleFilenames, wordList, ['powered', 'on'], ['golden', 'powered'], ext)
    manualWordSwap(possibleFilenames, wordList, ['powered'], ['golden'], ext)
    manualWordSwap(possibleFilenames, wordList, ['torch'], ['on', 'torch'], ext)
    manualWordSwap(possibleFilenames, wordList, ['grass'], ['tallgrass'], ext)
    manualWordSwap(possibleFilenames, wordList, ['wooden'], ['wood'], ext)
    manualWordSwap(possibleFilenames, wordList, ['furnace'], ['furnace', 'off'], ext)
    manualWordSwap(possibleFilenames, wordList, ['poppy'], ['flower', 'rose'], ext)