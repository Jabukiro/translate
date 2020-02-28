#Epub file parser

import re
class Parser:
    def __init__(self, fileref):
        self.file = fileref
        self.book = {}
        self.verses = {}
        self.chap = False
    def getBook(self):
        return self.book
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
        if match1 != None and match2 != None:
            #Getting whatever is between <title> and </title>
            print("Title-match Found")
            self.match1 = match1
            self.match2 = match2
            self.book['name'] = line[match1.span()[1]:match2.span()[0]]
            chap_num = re.search('[0-9]+$', self.book['name'])
            if chap_num == None:
                self.book['chapter']= 1
            else:
                self.book['chapter']= self.book['name'][chap_num.span()[0]:chap_num.span()[1]]

    def __verseMatch(self, line):
        vMatch1 = self.verseSt.search(line)

        #Specifically search for verse end after its start.
        if vMatch1 : vMatch2 = self.verseEnd.search(line, vMatch1.span()[1])
        if vMatch1 != None and vMatch2 != None:
            print("Verse found")
            vNumSlice = line[vMatch1.span()[0]:vMatch1.span()[1]]
            vNumMatch = re.search('[0-9]+', vNumSlice)
            try:
                vNum = vNumSlice[vNumMatch.span()[0]:vNumMatch.span()[1]]
            except:
                print("Unexcepted None match getting vNum. Possible pattern breaking\nLine>    ", line)
            if len(self.verses)==0 and vNumMatch:
                self.verses[1] = str(line[vMatch1.span()[1]:vMatch2.span()[0]])
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


                
            
    def start(self):
        print("Parser Innitiated.")
        print("Search Patterns set")
        for line in self.file.read().split('\n'):
            if len(self.book)==0:
                self.__bookMatch(line)
            else:
                self.__verseMatch(line)
        print('Parser Done')