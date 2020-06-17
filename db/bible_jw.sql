--Updated. Delete existing and re-create
ATTACH DATABASE 'bible_jw.db' AS 'bible'; 
CREATE TABLE testament(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name	CHAR(3)
);
CREATE TABLE book(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name		CHAR	NOT NULL,
	test_id INTEGER references testament(ID)
);
CREATE TABLE chapter(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	chapNum INTEGER NOT NULL,
	book_id INTEGER REFERENCES book(id),
	descript 	CHAR 	NULL
);
CREATE TABLE verses(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	chap_id INTEGER REFERENCES chapter(id),
	book_id INTEGER REFERENCES book(id),
	verseNum 	CHAR 	NOT NULL,
	verse	TEXT 	NOT NULL
);