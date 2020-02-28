--Updated. Delete existing and re-create
ATTACH DATABASE 'bible_jw.db' AS 'bible'; 
CREATE TABLE testament(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name	CHAR(3)
);
CREATE TABLE book(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	bible_id, 	INTEGER NOT NULL,
	name_en		CHAR	NOT NULL,
	name_kdi 	CHAR	NOT NULL,
	short_en	CHAR,
	short_kdi 	CHAR,
	chapters_num	INTEGER,
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
	verse_en	TEXT 	NOT NULL,
	verse_kdi	TEXT	NOT NULL
);

INSERT INTO testament VALUES(NULL, 'old');
INSERT INTO testament VALUES(NULL, 'new');
