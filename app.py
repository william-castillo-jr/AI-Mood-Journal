from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime
import sqlite3
import openai

# Gather all journal entries from database
def get_database_info():
    conn = sqlite3.connect('journal_entries.db')
    cursor = conn.cursor()

    # Select all journal entries and corresponding mood from sentiment_data table
    cursor.execute("""
        SELECT je.entry_id, je.journal_entry, je.entry_date, sd.mood, je.category
        FROM journal_entries je
        LEFT JOIN sentiment_data sd ON je.sentiment_id = sd.sentiment_id
    """)
    entries_with_mood = cursor.fetchall()

    conn.close()

    # Return the entries and moods as a list of dictionaries
    return [{"entry_id": entry[0], "journal_entry": entry[1], "entry_date": entry[2], "mood": entry[3], "category": entry[4]} for entry in entries_with_mood]

# Ensure the AI response ends with a complete sentence, 
# providing proper closure to the summary instead of ending abruptly.
def ensure_complete_sentence(text):
    # Check if the last character is a period
    if text.endswith('.'):
        return text
    # Attempt to remove an incomplete sentence by trimming to the last period
    last_period_index = text.rfind('.')
    if last_period_index != -1:
        return text[:last_period_index + 1]  # Include the last period
    return text  # Return as-is if no period is found

# Generate the chatGPT summary from the combined entries 
def get_chatgpt_summary(entries_info):
    # Combine all journal entries into one large text block
    combined_entries = "\n".join([f"Entry {i+1} (Mood: {entry['mood']}, Category: {entry['category']}): {entry['journal_entry']}" 
                                 for i, entry in enumerate(entries_info)])

    # Send the combined entries to OpenAI for analysis and summary
    prompt = f"""
    Please summarize the following journal entries, highlighting the mood (good, bad, excellent, etc.) and categories (work, school, personal, etc.).
    Provide a summary of the entries and then summarize any patterns or themes across them:
    {combined_entries}

    When sharing the response, provide a summary of the combined entries, including key observations, but avoid summarizing each entry individually. Focus on identifying overall trends and mood patterns. Ensure that the summary is cohesive and ends in a complete sentence, providing closure and positivity.
    """

    # Make the API call to OpenAI and configure with a specific role, temperature, tokens
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": """ 
             You are an AI assistant designed to summarize journal entries with a compassionate and empathetic tone. 
        Your task is to analyze the journal entries as a whole and provide a heartfelt summary.
        Think of yourself as a close friend or therapist who is listening carefully and offering understanding.
        Highlight the key emotions and recurring themes that come through in the entries, such as moods (excellent, great, good, okay, bad, very) and categories (work, education, hobbies, relationship, family, self-care). 
        Be sure to convey empathy and provide a sense of comfort, letting the user know that their feelings are valid and understood.
        Your summary should focus on offering encouragement and support, recognizing the user's struggles and celebrating their growth, where appropriate.
        Always ensure the summary ends with a complete sentence or conclusion, leaving the user with a sense of closure and understanding. 
        When writing the summary, keep in mind that it should feel like it’s coming from someone who genuinely cares about them, someone who understands how they’re feeling and is here to offer help and guidance.
        Ensure that the summary ends with a complete sentence and offers a sense of closure.
        Avoid leaving thoughts incomplete or ending abruptly. Complete the summary in 5 sentences.
        """},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=150
    )
    
    summary = response['choices'][0]['message']['content'].strip()
    summary = ensure_complete_sentence(summary)

    return summary

# Retrieve the most recent entry to display on homepage
def get_most_recent_entry():
    conn = sqlite3.connect('journal_entries.db')
    cursor = conn.cursor()

    # Query to fetch the most recent journal entry
    cursor.execute("""
        SELECT journal_entry, entry_date
        FROM journal_entries
        ORDER BY entry_date DESC
        LIMIT 1
    """)
    recent_entry = cursor.fetchone()
    conn.close()

    raw_date = recent_entry[1]
    formatted_date = datetime.strptime(raw_date, '%Y-%m-%d').strftime('%A %B %d, %Y')

    return {"journal_entry": recent_entry[0], "entry_date": formatted_date}

###### Start Routes ######

app = Flask(__name__)

# Homepage
@app.route('/')
def main_page():
    # Fetch the most recent entry
    recent_entry = get_most_recent_entry()
    
    # Fetch all entries for generating the summary
    entries = get_database_info()
    
    # Generate the summary
    summary = get_chatgpt_summary(entries)
    
    # Pass both the recent entry and summary to the template
    return render_template('index.html', recent_entry=recent_entry, summary=summary)

# Form to enter new journal entry
@app.route('/form')
def form_page():
    print("Form page route accessed!")
    return render_template('form.html')

# Process the form and insert into database - redirect to homepage
@app.route('/process_form', methods=['POST'])
def process_form():
    mood = request.form['mood_value']
    category = request.form['category']
    description = request.form['journal-entry']

    conn = sqlite3.connect('journal_entries.db')
    cursor = conn.cursor()

    cursor.execute(
    '''
    INSERT INTO journal_entries ( journal_entry, sentiment_id) VALUES (?, ?)
    ''', (description, mood))
    
    conn.commit()
    conn.close()

    return redirect(url_for('main_page'))

# Display the summary on a separate page from homepage
@app.route('/display_summary')
def display_summary():
    # Fetch all entries for generating the summary
    entries = get_database_info()

    # Generate the summary
    summary = get_chatgpt_summary(entries)

    # Render the summary page with the generated summary
    return render_template('display_summary.html', summary=summary)

# Used for the follow-up question from a user for the AI
def process_question_with_ai(user_question):
# Send the combined entries to OpenAI for analysis and summary
    prompt = f"""
The user has a follow-up question related to the summary you've already provided. The summary was compassionate and focused on providing support. Please answer their question with the same tone and empathy as the initial summary, while taking into account their feelings and thoughts:

User's question: {user_question}
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """
                You are an AI assistant who provides compassionate, empathetic responses. Your role is to offer support and understanding, especially when analyzing journal entries and their emotional context. 
                When responding to follow-up questions, always consider the feelings of the user and maintain a warm, understanding tone. 
                Acknowledge the user's emotional state and offer helpful insights, guidance, or encouragement as needed.
                Your responses should provide comfort and closure, ensuring the user feels heard and understood.
                Avoid providing vague answers and aim for clarity and empathy in every response.
                When interacting with the user, do not be overly formal. Instead, approach them like a close friend or therapist who cares deeply about their well-being.
                """},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    # Extract the response
    ai_answer = response['choices'][0]['message']['content'].strip()

    # Return the AI's response
    return ai_answer
  
# Render the page with the generated response
@app.route('/follow_up', methods=['GET', 'POST'])
def follow_up():
    # Retrieve the summary from the session
    summary = session.get('summary')

    if request.method == 'POST':
        # Get the follow-up question from the form
        user_question = request.form.get('question')

        if user_question:
            # Process the question with AI or save it
            ai_response = process_question_with_ai(user_question)

            # Render the follow-up page with the AI's response and the summary
            return render_template('follow_up.html', ai_response=ai_response, summary=summary)
        else:
            # If no question was submitted, inform the user
            ai_response = "I'm sorry, but it seems like there's no question provided in your message. Could you please provide me with the question you would like answered? I'm here to help and I'll do my best to assist you with empathy and understanding."
            return render_template('follow_up.html', ai_response=ai_response, summary=summary)

    # Default behavior if it's a GET request (first time visiting the page)
    return render_template('follow_up.html', ai_response=None, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)