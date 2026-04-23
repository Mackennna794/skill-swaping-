import sqlite3

def get_connection():
    # check_same_thread=False is required for Streamlit's multi-threading
    conn = sqlite3.connect('skill_swap.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
    return conn

def init_db():
    """Initializes the database and creates necessary tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            skills_offered TEXT,
            skills_wanted TEXT,
            bio TEXT,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Messages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (receiver_id) REFERENCES users (id)
        )
    ''')
    
    # Create Reviews Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reviewer_id INTEGER NOT NULL,
            reviewed_user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            FOREIGN KEY (reviewer_id) REFERENCES users (id),
            FOREIGN KEY (reviewed_user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_users():
    """Get all users except the current one."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, skills_offered, skills_wanted, bio FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_by_id(user_id):
    """Get user by id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, skills_offered, skills_wanted, bio FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user(user_id, name, email, skills_offered, skills_wanted, bio):
    """Update user profile."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name = ?, email = ?, skills_offered = ?, skills_wanted = ?, bio = ? WHERE id = ?",
        (name, email, skills_offered, skills_wanted, bio, user_id)
    )
    conn.commit()
    conn.close()

def get_messages_for_user(user_id):
    """Get messages for user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT m.id, m.content, m.timestamp, u.name as sender_name FROM messages m JOIN users u ON m.sender_id = u.id WHERE m.receiver_id = ? ORDER BY m.timestamp DESC",
        (user_id,)
    )
    messages = cursor.fetchall()
    conn.close()
    return messages

def send_message(sender_id, receiver_id, content):
    """Send a message."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
        (sender_id, receiver_id, content)
    )
    conn.commit()
    conn.close()