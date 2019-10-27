import sqlite3

conn = sqlite3.connect("db.db")
c = conn.cursor()

def select_with_fetchone():
    cmd = "SELECT * FROM users WHERE user_id=%d" % 1000
    c.execute(cmd)
    result = c.fetchone()
    print(result)


def select_with_fetchall():
    cmd = "SELECT * FROM users"
    c.execute(cmd)
    result = c.fetchall()
    print(result)


def insert():
    cmd = "INSERT INTO users(user_id, state) VALUES (%d, '%s')" % (123, "registration")
    c.execute(cmd)
    conn.commit()
    print("inserted")


def update():
    cmd = "UPDATE users SET state='%s' WHERE user_id=%d" % (" ", 123)
    c.execute(cmd)
    conn.commit()
    print("updated")


def delete():
    cmd = "DELETE FROM users WHERE user_id=%d" % 123
    c.execute(cmd)
    conn.commit()
    print("deleted")


a = input()
select_with_fetchone()
a = input()
select_with_fetchall()
a = input()
insert()
a = input()
update()
a = input()
delete()
