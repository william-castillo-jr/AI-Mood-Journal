import sqlite3

conn = sqlite3.connect('journal_entries.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE journal_entries (
	entry_id INT PRIMARY KEY NOT NULL,
	journal_entry TEXT,
	entry_date DATE,
	sentiment_id INT,
	FOREIGN KEY (sentiment_id) REFERENCES sentiment_data (sentiment_id)
); 
''')

cursor.execute('''
CREATE TABLE sentiment_data (
	sentiment_id ID PRIMARY KEY NOT NULL,
	mood TEXT NOT NULL
);
'''
)

conn.commit()
conn.close()