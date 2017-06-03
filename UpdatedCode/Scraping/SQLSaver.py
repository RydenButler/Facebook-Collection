import sqlite3
from sqlite3 import Error

def create_connection(db_file):
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Error as e:
    print(e)
 
  return None


def create_table(conn, create_table_sql):
  try:
    c = conn.cursor()
    c.execute(create_table_sql)
  except Error as e:
    print(e)


def create_database(database_name):
 
  sql_create_ID_table = """ CREATE TABLE IF NOT EXISTS ID (
                            id integer PRIMARY KEY,
                            name text NOT NULL,
                            Facebook_id text UNIQUE
                            ); """
 
  sql_create_Data_table = """CREATE TABLE IF NOT EXISTS Data (
                            id integer PRIMARY KEY,
                            WUSTL_id integer NOT NULL,
                            page text NOT NULL,
                            message text NOT NULL,
                            message_id text NOT NULL,
                            post_time text NOT NULL,
                            FOREIGN KEY (WUSTL_id) REFERENCES ID (id)
                            );"""
 
  # create a database connection
  conn = create_connection(database_name)
  if conn is not None:
    # create ID table
    create_table(conn, sql_create_ID_table)
    # create data table
    create_table(conn, sql_create_Data_table)
  else:
    print("Error! cannot create the database connection.")


def create_ID(conn, user):
  sql = ''' INSERT OR IGNORE INTO ID(name, Facebook_id)
            VALUES(?,?) '''
  cur = conn.cursor()
  cur.execute(sql, user)
  cur.execute('SELECT rowid FROM ID WHERE Facebook_id = ?', (user[1],))
  return cur.fetchone()[0]

def create_Data(conn, data): 
  sql = ''' INSERT INTO Data(WUSTL_id, page, message, message_id, post_time)
            VALUES(?,?,?,?,?) '''
  cur = conn.cursor()
  cur.execute(sql, data)
  return cur.lastrowid

def check_existing_user(conn, user):
  cur = conn.cursor()
  cur.execute("SELECT * FROM ID WHERE Facebook_id=?", (user,))
  rows = cur.fetchall()
  for row in rows:
    return(row)


def populate_database(giant_tree, database_name):
  # create a database connection
  conn = create_connection(database_name)
  tally = 0
  with conn:
  # Iterate over facebook page names
    for page in giant_tree.keys():
      # Iterate over posts on a facebook page
      for post in giant_tree[page]:
        # Iterate over individual likes on a post
        for liker in post['likes']:
          tally += 1
          print 'Storing data for observation %d' % (tally)
          try:
            # Store name and id of liker
            user = (liker['name'], liker['id']);
          except KeyError, name:
            # If no name field, record placeholder
            user = ('NO NAME FIELD', liker['id']);
          user_id = create_ID(conn, user)
          print 'Current row id is %s' % (user_id)
          try:
            like_data = (user_id, page, post['message'], post['id'], post['created_time'])
          except KeyError, message:
            try:
              like_data = (user_id, page, post['story'], post['id'], post['created_time'])
            except KeyError, story:
              like_data = (user_id, page, 'NO MESSAGE CONTENT', post['id'], post['created_time'])
          create_Data(conn, like_data)
  conn.close()

def add_to_database(database_name, page_name, post):
  # create a database connection
  conn = create_connection(database_name)
  # Tally used for user notifications. These are suppressed below.
  #tally = 0
  with conn:
    for liker in post['likes']:
      #tally += 1
      # Suppressed comment for being too verbose on execution
      #print 'Storing data for observation %d' % (tally)
      try:
        # Store name and id of liker
        user = (liker['name'], liker['id']);
      except KeyError, name:
        # If no name field, record placeholder
        user = ('NO NAME FIELD', liker['id']);
      user_id = create_ID(conn, user)
      # Suppressed comment for being too verbose on execution
      #print 'Current row id is %s' % (user_id)
      try:
        like_data = (user_id, page_name, post['message'], post['id'], post['created_time'])
      except KeyError, message:
        try:
          like_data = (user_id, page_name, post['story'], post['id'], post['created_time'])
        except KeyError, story:
          like_data = (user_id, page_name, 'NO MESSAGE CONTENT', post['id'], post['created_time'])
      create_Data(conn, like_data)
  conn.close()
