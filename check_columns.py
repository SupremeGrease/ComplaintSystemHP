import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get the table info
cursor.execute("PRAGMA table_info(complaints_issue_category)")
columns = cursor.fetchall()

# Print the columns
print("Current columns in complaints_issue_category:")
for col in columns:
    print(f"Column: {col[1]}, Type: {col[2]}")

conn.close() 