import sqlite3

# connect database
conn = sqlite3.connect("vault.db")

# cursor
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()


def save_password(website, username, password):

    cursor.execute("""
    INSERT INTO passwords (website, username, password)
    VALUES (?, ?, ?)
    """, (website, username, password))

    conn.commit()


def get_passwords():

    cursor.execute("SELECT * FROM passwords")

    return cursor.fetchall()

def delete_password(record_id):

    cursor.execute(
        "DELETE FROM passwords WHERE id = ?",
        (record_id,)
    )

    conn.commit()