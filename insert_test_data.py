import sqlite3

conn = sqlite3.connect('journal_entries.db')

cursor = conn.cursor()

cursor.execute('''
-- Insert journal entries
-- Insert Statements for SQLite
INSERT INTO journal_entries (journal_entry, sentiment_id, category) 
VALUES 
('I can''t believe how much homework I have. I feel completely overwhelmed, and no matter how hard I try, it feels like I''m failing. I''m so stressed out.', 1, 'School'),

('School is taking such a toll on me. I can''t focus, I''m constantly anxious, and I feel like I''m not making any progress. Everything just seems like too much.', 1, 'School'),

('I didn''t even make it through the first hour of studying. I just feel mentally drained, and I have no motivation left. I don''t even want to think about the exams coming up.', 1, 'School'),

('I spent the entire day trying to study but ended up feeling worse. My brain isn''t retaining anything. I can''t take this constant pressure from school anymore.', 1, 'School'),

('Another bad day at school. I couldn''t concentrate at all in class. I just feel so tired and frustrated. It seems like everything is going wrong.', 1, 'School'),

('I''m feeling exhausted from work and school. I can''t focus on anything. I''m burned out from trying to juggle everything, and I don''t know how to handle it all anymore.', 2, 'Work'),

('It''s been such a long week. I tried to relax, but I can''t stop thinking about the deadlines coming up. I feel like I''m losing control over my life.', 2, 'School'),

('I had a decent day at school. I finished my homework on time and felt pretty good about it. I actually enjoyed a few of the subjects today.', 3, 'School'),

('I don''t even know how to feel anymore. My friends and I had a small argument, and I''ve been feeling down ever since. I just wish everything could go back to normal.', 4, 'Personal'),

('Today was a mixed day. Work was stressful, but I managed to catch up with some friends afterward. It wasn''t perfect, but it was better than nothing.', 3, 'Work');
''')

conn.commit()
conn.close()