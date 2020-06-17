#Epub file parser
import re
import json
class Parser:
    def __init__(self, fileref):
        self.file = fileref
        self.book = {}
        self.verses = {}
        self.chap = False
        self.__errorFile="logs/errorLog"
        self.patFile = "patterns.json"
    def getBook(self):
        if "name" in self.book.keys():
            return self.book
        else:
            logMsg="File >" + self.file.name + " does not contain verses.\n"
            self.log('error', logMsg)
            return "no_verses_found" 
    def getVerses(self):
        return self.verses

    def setPatterns(self, patterns):
        self.titleSt = re.compile(patterns['titleStart'])
        self.titleEnd = re.compile(patterns['titleEnd'])

        self.verseSt = re.compile(patterns['verseStart'])
        self.verseEnd = re.compile(patterns['verseEnd'])

    def __bookMatch(self, line):
        match1 = self.titleSt.search(line) #matches pattern at beggining of string
        match2 = self.titleEnd.search(line) #searches anywhere in string
        #print(match1, match2)
        if match1 != None and match2 != None:
            #Getting whatever is between <title> and </title>
            print("Title-match Found")
            self.match1 = match1
            self.match2 = match2
            bookChap = line[match1.span()[1]:match2.span()[0]]
            bookName = re.search('([0-9]+ )*[a-zA-z]+', bookChap)
            chap_num = re.search('[0-9]+$', bookChap)
            if chap_num == None:
                self.book['chapter'] = 1
                self.book['name'] = bookChap
            else:
                self.book['chapter']= bookChap[chap_num.span()[0]:chap_num.span()[1]]
                self.book['name'] = bookChap[:bookName.span()[1]]
    def __verseMatch(self, line):
        vMatch1 = self.verseSt.search(line)

        #Specifically search for verse end after its start.
        if vMatch1 : vMatch2 = self.verseEnd.search(line, vMatch1.span()[1])
        if vMatch1 != None and vMatch2 != None:
            print(line)
            print("Verse found")
            vNumSlice = line[vMatch1.span()[0]:vMatch1.span()[1]]
            vNumMatch = re.search('[0-9]+', vNumSlice)
            try:
                vNum = vNumSlice[vNumMatch.span()[0]:vNumMatch.span()[1]]
                print(vNum)
            except:
                print("Unexcepted None match getting vNum. Possible pattern breaking\nLine>    ", line)
            if len(self.verses)==0 and vNumMatch:
                self.verses[1] = str(line[vMatch1.span()[1]:vMatch2.span()[0]])
                print(self.verses)
            elif len(self.verses) !=0:
                self.verses[str(vNum)] = str(line[vMatch1.span()[1]:vMatch2.span()[0]])
                #Some Chapters/Books have a few verseson the same line
                #Line traversal
                vMatch1 = self.verseSt.search(line, vMatch2.span()[1])
                while vMatch1 != None:
                    vNumSlice = line[vMatch1.span()[0]:vMatch1.span()[1]]
                    vNumMatch = re.search('[0-9]+', vNumSlice)
                    try:
                        vNum = vNumSlice[vNumMatch.span()[0]:vNumMatch.span()[1]]
                    except:
                        print("Unexcepted None match getting vNum. Possible pattern breaking\nLine>    ", line)

                    vMatch2 = self.verseEnd.search(line, vMatch1.span()[1])
                    self.verses[str(vNum)] = str(line[vMatch1.span()[1]:vMatch2.span()[0]])
                    vMatch1 = self.verseSt.search(line, vMatch2.span()[1])
                print(self.verses[str(vNum)])
            print(vNum)

    def log(self, logType, logMsg):
        if logType == "error":
            with open(self.__errorFile, 'a') as logFile:
                logFile.write(logMsg+'\n')

                
            
    def start(self):
        print("Parser Innitiated.")
        print("Search Patterns set")
        #try:
        Lines=self.file.readlines()
        for line in Lines:
            print("Parsing line >", line)
            if len(self.book)==0:
                self.__bookMatch(line)
            else:
                self.__verseMatch(line)
        #except Exception as e:
        #    logMsg="Exception: "+type(e).__name__+" whilst reading file >"+self.file.name + '\n'
        #    logMsg=logMsg + "\tFurther Details> " + str(e) + "\n"
        #    self.log("error", logMsg)
        print('Parsing of file >'+self.file.name)
        print('\tNumber of verses found >'+str(len(self.verses)))

if __name__ == '__main__':
    filename = "bible/en/OEBPS/1001061125-split3.xhtml"#input("File name to parse >")
    f=open(filename, 'r', encoding='utf8')
    parser = Parser(f)
    with open(parser.patFile, 'r') as file:
        parser.setPatterns(json.load(file)['en'])
    print("Breakpoint set. Debug away!")