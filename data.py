import sqlite3

def view_table(table_name):
    conn = sqlite3.connect('instance/data.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

def main():
    table_name = 'counter_log'
    print(f"Viewing contents of the '{table_name}' table:")
    view_table(table_name)

if __name__ == "__main__":
    main()
