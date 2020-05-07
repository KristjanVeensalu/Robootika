import functions as func

#Force install pyenchant
func.install("pyenchant")

#Set up enchant spellchecker and dictionary
chkr = func.SpellChecker("en_US",filters=[func.EmailFilter,func.URLFilter])
d=func.enchant.Dict("en_US")

#Ready a output file
outputFile = "results.txt"
func.clearFile(outputFile)

#Let user choose folder or file
userChoice = "None"
while userChoice != "F" and userChoice !="f" and userChoice!="d" and userChoice!="D":
    userChoice = input("F = Specific file spellcheck, D = Directory wide spellcheck: ")
    if userChoice == "D" or userChoice == "d":
        selectedFolder = func.chooseFolder()
        selectedFiles = func.parseFolder(selectedFolder)
    if userChoice == "F" or userChoice == "f":
        selectedSingleFile = func.chooseFile()
        selectedFiles = []

#Parse files in chosen folder
if userChoice == "d" or userChoice == "D":
    for x in selectedFiles:
        print("File found: "+x)
    filesFoundSum = len(selectedFiles)
    print("Files found: " + str(filesFoundSum))
if userChoice == "f" or userChoice == "F":
    selectedFiles.append(selectedSingleFile)

#Run automatic spellcheck with suggestions, output into file
try:
    for enchantFiles in selectedFiles:
        func.printLine()
        f=open(enchantFiles, encoding='utf-8')
        textPhase = f.read()
        chkr.set_text(textPhase)
        for err in chkr:
            failedWord = d.suggest(err.word)
            func.writeFile("Word: ('" + err.word + "') In: " + enchantFiles,outputFile)
            func.writeFile("Here are a few suggestions: ",outputFile)
            func.writeFile(str(failedWord).strip('[]')+ "\n",outputFile)

#If automatic fails, switch to manual
except:
    print("Automatic failed, switching to manual...")
    
    #Split sentences in file into a list
    for fileItself in selectedFiles:
        print(fileItself)
        f=open(fileItself, encoding='utf-8')
        textPhase = f.read()
        splitList = textPhase.split(" ")
        f.close()
        phraseIndex = 0
        listIndexProvider = []

        #Start filtering the list of words
        for x in splitList:
                if "\n" in x:
                    splitList[splitList.index(x)] = x.replace("\n","")

        for x in splitList:
                if "\t" in x:
                    splitList[splitList.index(x)] = x.replace("\t","")

        for x in splitList:
                if ":" in x:
                    splitList[splitList.index(x)] = x.replace(":","")

        for x in splitList:
                if ";" in x:
                    splitList[splitList.index(x)] = x.replace(";","")

        for z in range(0,10):
            for x in splitList:
                if x.endswith("."):
                    if x == "e.g." or x == "etc." or x == "eg." or x =="e.g":
                        splitList[splitList.index(x)] = x.replace(".","")
                    else:
                        phraseIndex = phraseIndex + 1
                        listIndexProvider.append(splitList.index(x))
                        splitList[splitList.index(x)] = x.replace(".","")
                if x.endswith(","):
                    splitList[splitList.index(x)] = x.replace(",","")

        for x in splitList:
            if x.endswith('"') or x.startswith('"'):
                splitList[splitList.index(x)] = x.replace('"',"")

        #Fetch sentence endpoints
        modifiedIndexProvider = []

        for x in listIndexProvider:
            x = x+1
            modifiedIndexProvider.append(x)

        if len(modifiedIndexProvider)>1:
            modifiedIndexProvider.remove(modifiedIndexProvider[len(modifiedIndexProvider)-1])


        for x in modifiedIndexProvider:
            if len(modifiedIndexProvider)>1:
                newPhraseWord = splitList[x]
                splitList[x] = newPhraseWord + "NEW"

        #Check word syntax
        faultyWords = []
        for x in splitList:
            if x == splitList[0] and x.isupper():
                d.check(x)
                if d.check(x) == False:
                    faultyWords.append(x)
            else:
                if x == "eg":
                    pass
                else:
                    if not x:
                        splitList.remove(x)
                    else:
                        if x[0].isupper() and "NEW" not in x:
                            pass
                        else:
                            if "NEW" not in x:
                                if d.check(x) == False:
                                    faultyWords.append(x)
                            else:
                                holder = x.replace("NEW","")
                                if d.check(holder) == False:
                                    faultyWords.append(holder)

        wordPosition = 0

        #Return output
        for x in faultyWords:
            wordPosition = splitList.index(x)
            func.writeFile("Word: (" + x + ") In> " + fileItself + "\n", outputFile)
