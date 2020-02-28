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

def insertAll(values, table, cursor):
    if (table == 'books'):
        cursor.executemany('INSERT INTO book VALUES(Null,?,?,?,?,?)', values)
        print('Books inserted succefully')
    if (table == 'chapters'):
        cursor.executemany('INSERT INTO chapter VALUES(Null,?,?,?)', values)
        print("Chapters succesfully inserted")
    if (table == 'verses'):
        cursor.executemany('INSERT INTO verse VALUES(Null,?,?,?,?)', values)
        print("Verses succesfully inserted")

def main():
    books = []
    verses = {}
    conn = db.connect('bible_jw.db')
    patFile = open('patterns.json', 'r')
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
        epubFile = open(patterns['en']['home']+f)
        obj = Parser(epubFile)

        #change to patterns[language]
        obj.setPatterns(patterns['en'])
        obj.start()
        chapter = obj.getBook()
        books.append(chapter)
        verses[chapter['name']] = obj.getVerses()
        epubFile.close()
    print('All done')
main()