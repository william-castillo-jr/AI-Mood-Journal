import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('journal_entries.db')
cursor = conn.cursor()

# Drop the old table if it exists (this will delete all data)
cursor.execute('DROP TABLE IF EXISTS journal_entries')

# Now create the table again with the correct schema
cursor.execute('''
    CREATE TABLE journal_entries (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        journal_entry TEXT NOT NULL,
        entry_date DATE DEFAULT (DATE('now')),
        sentiment_id INTEGER,
		category VARCHAR(50)
    )
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