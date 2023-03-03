import sqlite3
from sqlite3 import Error

#
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def work_table(a1, a2, a3, a4, a5, a6, a7, a8):

    connection = create_connection("hist_app.sqlite")
    c = connection.cursor()
    # c.execute('DELETE FROM history;',);

    create_history_table = """
    CREATE TABLE IF NOT EXISTS history (
      query TEXT,
      date_time TEXT,
      hotel TEXT DEFAULT 40,
      price REAL,
      total_price REAL,
      dist REAL,
      lat REAL,
      lon REAL  
    );
    """

    execute_query(connection, create_history_table)

    # print(a1, a2, a3, a4, a5, a6, a7, a8)
    if len(a3) < 30:
        a3 = a3 + ' ' * (30 - len(a3))

    c.execute(f"INSERT INTO history (query, date_time, hotel, price, total_price, dist, lat, lon) VALUES(?,?,?,?,?,?,?,?)",
              (a1, a2, a3, a4, a5, a6, a7, a8))
    connection.commit()



    # create_history = f"""
    # INSERT INTO
    #   history (query, date_time, hotel, price, total_price, dist, lat, lon)
    # VALUES
    #   ({a1}, {a2}, {a3}, {a4}, {a5}, {a6}, {a7}, {a8});
    # """

    # ('lp', '2023-03-02 20:44', 'Riga', 30.22, 60.44, 1.8, 56.936607, 24.071348)

    # execute_query(connection, create_history)



