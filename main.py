import functions as func
func.install("pyenchant")
import enchant
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
chkr = SpellChecker("en_US",filters=[EmailFilter,URLFilter])
d=enchant.Dict("en_US")

selectedFolder = func.chooseFolder()
selectedFiles = func.parseFolder(selectedFolder)

for x in selectedFiles:
    print("File found: "+x)
filesFoundSum = len(selectedFiles)
print("Files found: " + str(filesFoundSum))

try:
    for enchantFiles in selectedFiles:
        func.printLine()
        f=open(enchantFiles, encoding='utf-8')
        textPhase = f.read()
        chkr.set_text(textPhase)
        for err in chkr:
            print("Word: ('" + err.word + "') In: " + enchantFiles)
            failedWord = d.suggest(err.word)
            print("Here are a few suggestions: ", end =" ")
            print(failedWord)

except:
    print("Automatic failed, switching to manual...")
    for fileItself in selectedFiles:
        print(fileItself)
        f=open(fileItself, encoding='utf-8')
        textPhase = f.read()
        splitList = textPhase.split(" ")
        f.close()
        phraseIndex = 0
        listIndexProvider = []

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

        for x in faultyWords:
            wordPosition = splitList.index(x)
            print("Word: (" + x + ") In> " + fileItself) 
