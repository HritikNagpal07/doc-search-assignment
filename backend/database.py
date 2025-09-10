import sqlite3

# Creates the SQLite database and table to store file information
def init_db():
    conn = sqlite3.connect('search_metadata.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL,
            repo_name TEXT NOT NULL,
            title TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Saves information about a document into the database
def insert_document(file_path: str, repo_name: str, title: str):
    conn = sqlite3.connect('search_metadata.db')
    c = conn.cursor()
    c.execute("INSERT INTO documents (file_path, repo_name, title) VALUES (?, ?, ?)",
              (file_path, repo_name, title))
    conn.commit()
    conn.close()
