import sqlite3
from tabulate import tabulate
from fastapi import HTTPException
import httpx

def create_table(db_file):
    con = sqlite3.connect(db_file)
    cursor_obj = con.cursor()

    query_table = """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        total_solved INTEGER,
        points INTEGER,
        easy_solved INTEGER DEFAULT 0,
        medium_solved INTEGER DEFAULT 0,
        hard_solved INTEGER DEFAULT 0
    );
    """
    cursor_obj.execute(query_table)
    print("Table is ready")
    con.close()

def add_user(db_file, username, total_solved, points, easy_solved, medium_solved, hard_solved):
    con = sqlite3.connect(db_file)
    cursor_obj = con.cursor()
    query_table = """
    INSERT INTO users (username, total_solved, points, easy_solved, medium_solved, hard_solved)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor_obj.execute(query_table, (username, total_solved, points, easy_solved, medium_solved, hard_solved))
    print("Inserting Data...")

    data = cursor_obj.execute('SELECT * FROM users')
    for row in data:
        print(row)
    
    con.commit()
    con.close()

def update_user(db_file, username, total_solved, points, easy_solved=0, medium_solved=0, hard_solved=0):
    try:
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        query = """
        UPDATE users
        SET total_solved = ?, points = ?, easy_solved = ?, medium_solved = ?, hard_solved = ?
        WHERE username = ?
        """
        cursor.execute(query, (total_solved, points, easy_solved, medium_solved, hard_solved, username))
        db.commit()
    except Exception as e:
        print(f"Error updating user: {e}")
    finally:
        db.close()

def display_all_user(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    output = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    if output:
        print("Displaying all registered users")
        print(tabulate(output, headers=column_names, tablefmt="grid"))
    else:
        print("No users found in the database.")
    
    conn.close()
    return output

def top_user(db_file):
    try:
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        query = """
        SELECT username, total_solved, points, easy_solved, medium_solved, hard_solved
        FROM users
        ORDER BY points DESC
        LIMIT 3
        """
        cursor.execute(query)
        users = cursor.fetchall()
        
        if not users:
            print("No users found in database")
            return {"first": None, "second": None, "third": None}
        
        rankings = ["first", "second", "third"]
        result = {}
        for i, rank in enumerate(rankings):
            if i < len(users):
                user = users[i]
                result[rank] = {
                    "username": user[0],
                    "total_solved": user[1],
                    "points": user[2],
                    "easy_solved": user[3],
                    "medium_solved": user[4],
                    "hard_solved": user[5]
                }
            else:
                result[rank] = None
        print("\nTop Users:")
        print(tabulate(result.values(), headers="keys", tablefmt="pretty"))        
        return result
    finally:
        db.close()

def check_user_exists(db_file, username):
    conn = sqlite3.connect(db_file)
    curr = conn.cursor()
    query_table = "SELECT COUNT(1) FROM users WHERE username=? LIMIT 1"

    curr.execute(query_table, (username,))
    existing_user = curr.fetchone()

    conn.close()
    
    if existing_user and existing_user[0] == 1:
        return True
    else:
        print("User given is not registered")
        return False

def get_first_place(db_file):
    conn = sqlite3.connect(db_file)
    curr = conn.cursor()
    query_table = "SELECT * FROM users ORDER BY points DESC LIMIT 1"

    curr.execute(query_table)
    column_names = [description[0] for description in curr.description]
    data = curr.fetchall()

    print("Showing the top user")
    if data:
        print(tabulate(data, headers=column_names, tablefmt="grid"))
    else:
        print("No users added")
    
    conn.close()
    return data

def delete_user(db_file, username):
    conn = sqlite3.connect(db_file)
    curr = conn.cursor()
    query_table = 'DELETE FROM users WHERE username=?'
    curr.execute(query_table, (username,))
    conn.commit()
    conn.close()

async def fetch_user_stats(username):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://0.0.0.0:8000/{username}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch stats for user {username}: {response.text}")
            return None

async def update_all_users_stats(db_file):
    try:
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        query = "SELECT username FROM users"
        cursor.execute(query)
        users = cursor.fetchall()

        for user in users:
            username = user[0]
            updated_stats = await fetch_user_stats(username)
            
            if updated_stats:
                total_solved = updated_stats.get("EASY", 0) + updated_stats.get("MEDIUM", 0) + updated_stats.get("HARD", 0)
                points = (updated_stats.get("EASY", 0) * 1) + (updated_stats.get("MEDIUM", 0) * 3) + (updated_stats.get("HARD", 0) * 5)
                easy_solved = updated_stats.get("EASY", 0)
                medium_solved = updated_stats.get("MEDIUM", 0)
                hard_solved = updated_stats.get("HARD", 0)

                update_user(db_file, username, total_solved, points, easy_solved, medium_solved, hard_solved)
    except Exception as e:
        print(f"Error updating all users' stats: {e}")
    finally:
        db.close()
