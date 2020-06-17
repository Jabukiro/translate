########
#Author: Jabukiro
########
#----- File used to parse the epub files and save the bible

#Only 11510 verses are separated(out of 30000-ish)
#Include error detection in epubParser
#Use unit testing.
import sqlite3 as db
import os
import re
import json
from xhtmlParser import Parser
from xhtmlParser import InvalidFileError

def openFile(filename, usedFile=None):
    if (int(filename[:2]) <=71 or int(filename[:2]) >= 5):
        try:
            fileRef = open(filename, 'r')
        except OSError:
            print("Error: File could not be loaded")
            return "Error: File could not be loaded"
        else:
            return fileRef
    elif (not usedFile):
        os.close(usedFile)

def insertAll(cursor, table, values):
    if (table == 'book'):
        cursor.execute('INSERT INTO book VALUES(NULL,?,?)', values)
        print('Books inserted succefully')
        return getId(cursor, "book", [values[0]])

    if (table == 'chapters'):
        cursor.execute('INSERT INTO chapter ("id", "chapNum", "book_id", "descript") VALUES(null,?,?,null)', values)
        print("Chapters succesfully inserted")
        return getId(cursor, "chapter", values)

    if (table == 'verses'):
        cursor.execute('INSERT INTO verses VALUES(NULL,?,?,?,?)', values)
        print("Verses succesfully inserted")

def getId(cursor, table, term):
    if (table == 'book'):
        result = cursor.execute('SELECT id FROM book WHERE name=?', term)
        ID = result.fetchone()
        print('Books inserted succefully')
        return ID[0] if ID else None
    elif (table == 'chapter'):
        result = cursor.execute('SELECT id FROM chapter WHERE chapNum=? and book_id=?', term)
        ID = result.fetchone()
        print('Books inserted succefully')
        return ID[0] if ID else None

def getVerseCount(bookId, cursor):
    result = cursor.execute("SELECT COUNT(*) FROM verse WHERE bookId=?", bookId)
    return result.fetchone()
def getAllPerTable(table, cursor):
    result = cursor.execute("SELECT COUNT(*) FROM verse WHERE bookId=?", bookId)
    return result.fetchone()


def main():
    books = []
    verses = {}
    filesParsed=0
    patFile = open('patterns.json', 'r', encoding='utf8')
    patterns = json.load(patFile)
    print("Currently Supported Languages:\n    ", patterns['languages'])
    language = input("Which language would you like?\n>    ")
    #path = input("Home directory of decompressed epub files:\n>    ")

    #Loading list of files and DB
    conn = db.connect('db/ru_bible_jw.db')
    cur = conn.cursor()
    enFileList = os.listdir(patterns[language]['home'])

    #Regex patterns for matching files containing verses
    #Significantly reduces files needed to be opened
    enFilePat = re.compile(patterns[language]['files'])
    enCorrList = [f for f in enFileList if (enFilePat.match(f) != None and int(f[:2])<71)]
    for f in enCorrList:
        filesParsed+=1
        print("reading file >", patterns[language]['home']+f)
        epubFile = open(patterns[language]['home']+f, 'r', encoding='utf8')
        parser = Parser()

        #Start parsing the file
        try:
            parser.start(epubFile)
        except InvalidFileError:
            continue
        chapter = parser.getBook()
        if chapter == "no_verses_found":
            filesParsed-=1
            continue
        else:
            bookID = getId(cur, table="book", term=[chapter["name"]])
            chapID = getId(cur, table="chapters", term=[chapter["chap"]])
            if not bookID:
                #This should not happen
                bookID = insertAll(cur, table="book", values=[chapter["name"], "unsanitary"])
            if not chapID:
                chapID = insertAll(cur, table="chapters", values=[chapter["chap"], str(bookID)])
        #print(chapter)
        books.append(chapter)
        verses = parser.getVerses()
        for versekey in verses:
            insertAll(cur, table="verses", values=[str(chapID), str(bookID), str(versekey), verses[versekey]])
        epubFile.close()
    conn.commit()
    cur.close()
    conn.close()
    print('All done. Files parsed>', filesParsed)
main()