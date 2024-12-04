import sqlite3

conn = sqlite3.connect('journal_entries.db')

cursor = conn.cursor()

cursor.execute('''           
-- Insert sentiment data (moods)
INSERT INTO sentiment_data (sentiment_id, mood) VALUES 
(6, 'excellent'),
(5, 'great'),
(4, 'good'),
(3, 'okay'),
(2, 'bad'),
(1, 'very bad');
''')

cursor.execute('''
-- Insert journal entries
INSERT INTO journal_entries (entry_id, journal_entry, entry_date, sentiment_id) VALUES 
    (1, 'I had an amazing day today, everything went perfectly! I’m feeling excellent.', '2024-11-25', 1), -- excellent
    (2, 'Today was great! I got everything done that I needed to and felt great about it.', '2024-11-26', 2),  -- great
    (3, 'It was a good day overall, nothing major happened but I felt satisfied.', '2024-11-27', 3),            -- good
    (4, 'I’m feeling okay today, nothing extraordinary, but I made it through the day.', '2024-11-28', 4),     -- okay
    (5, 'I had a tough day. Things didn’t go as planned, but it could have been worse.', '2024-11-29', 5),     -- bad
    (6, 'I’ve been feeling down all day, nothing seems to go right, and it’s been very hard.', '2024-11-30', 6), -- very bad
    (7, 'I’m so happy! Today was simply the best day ever. I feel excellent.', '2024-12-01', 1),              -- excellent
    (8, 'Everything went smoothly today and I’m in a great mood!', '2024-12-02', 2),                          -- great
    (9, 'Today was a good day, I felt productive and content.', '2024-12-03', 3),                             -- good
    (10, 'I didn’t feel great today, but I still managed to get things done, so that’s something.', '2024-12-04', 4),  -- okay
    (11, 'It was an okay day, not bad but not great either. I can’t wait for tomorrow.', '2024-12-05', 3),        -- good
    (12, 'I had some issues today, but I’m trying to stay positive and not let it ruin my mood.', '2024-12-06', 2); -- great
''')

conn.commit()
conn.close()