import sqlite3
from database import get_connection

# --- USER MODELS ---

def create_user(name, email, hashed_pw):
    """Inserts a new user into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                       (name, email, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email already exists
    finally:
        conn.close()

def get_user_by_email(email):
    """Fetches a user record by email for login validation."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Fetches a user record by their ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_profile(user_id, name, bio, skills_offered, skills_wanted):
    """Updates the profile details of an existing user."""
    conn = get_connection()
    cursor = conn.cursor()
    offered_str = ", ".join(skills_offered) if skills_offered else ""
    wanted_str = ", ".join(skills_wanted) if skills_wanted else ""
    
    cursor.execute("""
        UPDATE users 
        SET name = ?, bio = ?, skills_offered = ?, skills_wanted = ?, last_active = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (name, bio, offered_str, wanted_str, user_id))
    conn.commit()
    conn.close()

def get_all_other_users(current_user_id):
    """Fetches all users except the currently logged-in user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id != ?", (current_user_id,))
    users = cursor.fetchall()
    conn.close()
    return users

# --- MESSAGING MODELS ---

def send_message(sender_id, receiver_id, content):
    """Saves a message to the database, preventing identical back-to-back spam."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Spam check
    cursor.execute('''
        SELECT content FROM messages 
        WHERE sender_id = ? AND receiver_id = ? 
        ORDER BY timestamp DESC LIMIT 1
    ''', (sender_id, receiver_id))
    last_msg = cursor.fetchone()
    
    if last_msg and last_msg['content'] == content:
        conn.close()
        return False  # Duplicate detected
        
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
                   (sender_id, receiver_id, content))
    conn.commit()
    conn.close()
    return True

def get_messages_for_user(user_id, role="receiver"):
    """Fetches messages either sent to or sent by a user."""
    conn = get_connection()
    cursor = conn.cursor()
    if role == "receiver":
        cursor.execute('''
            SELECT m.content, m.timestamp, u.name as other_person 
            FROM messages m 
            JOIN users u ON m.sender_id = u.id 
            WHERE m.receiver_id = ? ORDER BY m.timestamp DESC
        ''', (user_id,))
    else:
        cursor.execute('''
            SELECT m.content, m.timestamp, u.name as other_person 
            FROM messages m 
            JOIN users u ON m.receiver_id = u.id 
            WHERE m.sender_id = ? ORDER BY m.timestamp DESC
        ''', (user_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

# --- REVIEW MODELS ---

def add_review(reviewer_id, reviewed_id, rating, comment):
    """Saves a review for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (reviewer_id, reviewed_user_id, rating, comment) VALUES (?, ?, ?, ?)",
                   (reviewer_id, reviewed_id, rating, comment))
    conn.commit()
    conn.close()

def get_user_rating(user_id):
    """Calculates the average rating for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(rating) as avg_rating FROM reviews WHERE reviewed_user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result['avg_rating'] if result['avg_rating'] else 0