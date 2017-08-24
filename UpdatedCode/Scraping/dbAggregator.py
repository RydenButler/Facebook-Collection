import sqlite3
import os

def db_aggregator(to_db):
  # List files in current working directory	
  files = os.listdir(os.getcwd())
  # Subset to only .db files
  databases = [file for file in files if '.db' in file]
  # Connect to main database
  conn = sqlite3.connect(to_db)
  # Iterate over databases
  for db in databases:
    # Attach component database
    conn.execute("ATTACH '" + db + "' as '" + db + "'")
    # Begin transaction
    conn.execute('BEGIN')
    # Store Users
    user_statement = "INSERT OR IGNORE INTO Users SELECT * FROM '" + db + "'.Users"
    print(user_statement)
    conn.execute(user_statement)
    # Store Pages
    page_statement = "INSERT OR IGNORE INTO Pages SELECT * FROM '" + db + "'.Pages"
    print(page_statement)
    conn.execute(page_statement)
    # Store Posts
    post_statement = "INSERT OR IGNORE INTO Posts SELECT * FROM '" + db + "'.Posts"
    print(post_statement)
    conn.execute(post_statement)
    # Store Likes
    like_statement = "INSERT OR IGNORE INTO Likes (post_id, WUSTL_id) SELECT post_id, WUSTL_id FROM '" + db + "'.Likes"
    print(like_statement)
    conn.execute(like_statement)
    # Commit transaction
    conn.commit()
    # Detach component databae from environment 
    conn.execute("DETACH DATABASE '" + db + "'")


# Navigate to the directory containing the .db files you want to merge and then run the following line
db_aggregator('/Users/r.butler/Dropbox/Facebook/Data/HouseDBs/House.db')