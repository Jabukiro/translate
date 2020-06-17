from html.parser import HTMLParser
import re
import json

class Error(Exception):
    pass
class InvalidFileError(Error):
    """Exception raised for errors on given files.

    Attributes:
        expression -- expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, filename, message):
        self.filename = filename
        self.message = message

class Parser(HTMLParser):
    def setPatterns(self):
        #Reads in various patterns that are likely to change per language version.
        with open(self.patFileRef, 'r', encoding='utf8') as file:
           patterns=json.load(file)
           patterns=patterns["en"]

        self.titleTag = patterns["titleTag"]
        self.bookName = re.compile(patterns["bookName"])
        self.bookChap = re.compile(patterns["bookChap"])
        self.verseTag = patterns["verseTag"]
        self.verseID = patterns["verseAttrs"][0]
        self.verseAttrsVal = re.compile(patterns["verseAttrs"][1])

    def getBook(self):
        if "name" in self.book.keys():
            return self.book
        else:
            logMsg="File >" + self.file.name + " does not contain verses.\n"
            self.log('error', logMsg)
            return "no_verses_found"

    def getVerses(self):
        return self.verses

    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        if tag == self.verseTag:
            #print("tag >", self.verseTag, "Has attributes >", attrs)
            for _ , data in enumerate(attrs):
                if data[0] == self.verseID and self.verseAttrsVal.search(data[1]):
                    self.verseFound = True
                    break
                else:
                    continue
        else:
            return

    def handle_data(self, data):
        #print("Encountered some data >", data)
        #The most immediate tag in which the data was found.
        tag = self.get_starttag_text()
        #print("Starting tag was >", tag)
        if self.verseFound:
            #print("Possible Verse >", data)
            #print("Starting tag was >", tag)
            #Look for a verse or verseNumber
            if re.search("^[0-9]+\s*$", data) != None:
                #Strip the trailing space.
                self.currentVerse = int(data.strip()) if self.currentVerse != 0 else 1
                #print("Interpreted verse number >", self.currentVerse)
                self.lastVerse += 1 if self.currentVerse > self.lastVerse+1 else 0
                self.verseFound == True
                return
            elif self.currentVerse == self.lastVerse+1:
                #Most probably a verse. Note that verseNumber should have been set before the verse is found
                if str(self.currentVerse) in self.verses.keys():
                    self.verses[str(self.currentVerse)] += data
                else:
                    self.verses[str(self.currentVerse)] = data
                self.verseFound == True
                return
            elif re.search("^<p.*>", tag):
                #Most probably a verse. Note that verseNumber should have been set before the verse is found
                if str(self.currentVerse) in self.verses.keys():
                    self.verses[str(self.currentVerse)] += data
                else:
                    self.verses[str(self.currentVerse)] = data
                self.verseFound == True
                return
            self.verseFound = False
        elif tag == self.titleTag:
            bookChap=data
            print("Parsing title: ", bookChap)
            bookMatch=self.bookName.search(bookChap)
            chapMatch=self.bookChap.search(bookChap)

            if bookMatch != None and chapMatch != None:
                self.book["name"] = bookChap[bookMatch.span()[0]:bookMatch.span()[1]]
                self.book["chap"] = bookChap[chapMatch.span()[0]:chapMatch.span()[1]]
                self.verseFlag = True
            elif bookMatch != None and self.book == None:
                self.book["name"] = bookChap[bookMatch.span()[0]:bookMatch.span()[1]]
                self.book["chap"] = 1
                self.verseFlag = True
            elif not self.verseFlag:
                #Probably not a file that contains verses.
                #Actually raise exception.
                self.verseFlag = False
                logMsg="File >" + self.file.name + " does not contain verses.\n"
                self.log(logMsg=logMsg, logType="error")
                raise InvalidFileError(filename = self.file, message = "Given file was not valid.")

    def log(self, logMsg="", logType="end"):
        if logType == "error":
            logfile=self.__errorFile
        if logType == "end":
            logMsg = "~~~~ File >" + self.file.name + " Summary~~~~~~\n"
            logMsg += "Parsed Book >" + self.book["name"] +" With >" + self.book["chap"] + "chapters and >" + str(len(self.verses)) + " verses.\n"
            logMsg += "~~~~~~~~~~~~~~~~~~~~~~END SUMMARY\n"
            logfile=self.__summaryFile
        with open(logfile, 'a') as logFileRef:
            logFileRef.write(logMsg+'\n')
    def start(self, fileref, patFileRef=None):
        #Setting up needed flags ad variables.
        ##Reference to the xthml file that will be read
        self.file = fileref
        ##Store book name and chapter
        self.book = {}
        ##Store the verses found in the file according to their corresponding verse number
        self.verses = {}
        ##File for loggin errors.
        self.__errorFile="logs/errorLog"
        self.__summaryFile="logs/summaryLog"
        ##Will be set to True if the file is determined to contain verses. Early exit.
        self.verseFlag = False
        ##Flag used to parse data as verses.
        self.verseFound = False
        ##Reference to the last verse parsed.
        self.lastVerse = 0
        self.currentVerse = 0
        ##Pattern file that will be read.
        self.patFileRef = patFileRef if patFileRef else "patterns.json"
        ##Read and compile patterns that will oftenly be used.
        self.setPatterns()

        print("Parser Innitiated.")
        try:
            self.feed(self.file.read())
        except InvalidFileError:
            raise
        #try:
        #except Exception as e:
        #    logMsg="Exception: "+type(e).__name__+" whilst reading file >"+self.file.name + '\n'
        #    logMsg=logMsg + "\tFurther Details> " + str(e) + "\n"
        #    self.log("error", logMsg)
        print('Parsing of file >'+self.file.name)
        print('\tNumber of verses found >'+str(len(self.verses)))
        print("Parser Done. Logging results")
        self.log()
if __name__ == '__main__':
    filename = "bible/en/OEBPS/1001061125-split3.xhtml"#input("File name to parse >")
    f=open(filename, 'r', encoding='utf8')
    parser = Parser()
    parser.start(f)
    print("Breakpoint set. Debug away!")