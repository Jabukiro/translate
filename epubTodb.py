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
from epubParser import Parser


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

def insertAll(cursor, values, table):
    if (table == 'books'):
        cursor.executemany('INSERT INTO book VALUES(Null,?,?,?,?,?)', values)
        print('Books inserted succefully')
    if (table == 'chapters'):
        cursor.executemany('INSERT INTO chapter VALUES(Null,?,?,?)', values)
        print("Chapters succesfully inserted")
    if (table == 'verses'):
        cursor.executemany('INSERT INTO verse VALUES(Null,?,?,?,?)', values)
        print("Verses succesfully inserted")
def getId(cursor, table, term):
    if (table == 'book'):
        result = cursor.execute('SELECT id FROM book WHERE name=?', term)
        ID = result.fetchone()
        print('Books inserted succefully')
        return ID if ID else None

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
    conn = db.connect('db/bible_jw.db')
    patFile = open('patterns.json', 'r', encoding='utf8')
    patterns = json.load(patFile)
    cur = conn.cursor()
    print("Currently Supported Languages:\n    ", patterns['languages'])
    #language = input("Which language would you like?\n>    ")
    #path = input("Home directory of decompressed epub files:\n>    ")

    #Loading list of files
    enFileList = os.listdir(patterns['en']['home'])

    #Regex patterns for matching files containing verses
    #Significantly reduces files needed to be opened
    enFilePat = re.compile(patterns['en']['files'])
    enCorrList = [f for f in enFileList if (enFilePat.match(f) != None and int(f[:2])<71)]
    for f in enCorrList:
        filesParsed+=1
        print("reading file >", patterns['en']['home']+f)
        epubFile = open(patterns['en']['home']+f, 'r', encoding='utf8')
        parser = Parser(epubFile)

        #change to patterns[language]
        parser.setPatterns(patterns['en'])
        parser.start()
        chapter = parser.getBook()
        if chapter == "no_verses_found":
            filesParsed-=1
            continue
        else:
            bookId = getId(cur, table="books", term=chapter["name"])
            if bookId:
                insertAll
        print(chapter)
        books.append(chapter)
        verses[chapter['name']] = parser.getVerses()
        epubFile.close()
    cur.close()
    conn.close()
    print('All done. Files parsed>', filesParsed)
main()