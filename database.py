import sqlite3
import time
import datetime
import constants

db = sqlite3.connect('ratings.db')
c = db.cursor()


def log(typeof, base, name, rating, commentid, threadid, message):
    unix = time.time()
    now = datetime.datetime.now()
    datestamp = f"{now.year}-{now.month}-{now.day}"
    c.execute('INSERT INTO log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (unix, datestamp, typeof, base,
                                                           name, rating, commentid, threadid, message),)
    db.commit()


def create_table(base):
    c.execute(f'''CREATE TABLE IF NOT EXISTS {base}(unix REAL, datestamp TEXT, username TEXT, value REAL,
    commentid TEXT)''')
    db.commit()


def create_logtable():
    c.execute('''CREATE TABLE IF NOT EXISTS log(unix REAL, datestamp TEXT, type TEXT, base TEXT, 
    username TEXT, value REAL, commentid TEXT, threadid TEXT, message TEXT)''')


def data_entry(base, name, rating, commentid, threadid):
    unix = time.time()
    now = datetime.datetime.now()
    datestamp = f"{now.year}-{now.month}-{now.day}"
    print (f"insert into {base} {unix} {datestamp} {name} {rating} {commentid}")
    c.execute(f"INSERT INTO {base} VALUES(?, ?, ?, ?, ?)", (unix, datestamp,
                                                            name, rating, commentid),)

    c.execute("INSERT INTO log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (unix, datestamp, 'rating', base,
                                                                    name, rating, commentid, threadid, None),)
    db.commit()


def change_entry(base, name, rating, commentid, threadid):
    print("Changing rating to " + str(rating))
    unix = time.time()
    now = datetime.datetime.now()
    datestamp = f"{now.year}-{now.month}-{now.day}"
    c.execute(f"UPDATE {base} SET unix = ?, datestamp = ?, value = ?, commentid = ? WHERE username = ?",
              (unix, datestamp, rating, commentid, name),)

    c.execute("INSERT INTO log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (unix, datestamp, 'change', base,
                                                                    name, rating, commentid, threadid, None),)
    db.commit()


def query_rating(base):
    c.execute(f"SELECT TOTAL(value) FROM {base}")
    ratings = str(c.fetchone())
    ratings = ratings.translate({ord(i): None for i in '(),'})
    userratings = count_ratings(base)
    ratingssum = float(ratings)
    print(f"Querying rating of {base}, there are {userratings} ratings")
    if userratings == 0:
        return 10
    else:
        final = ratingssum / userratings
        return final


def query_commentid(commentid):  # check if we have already handled this comment
    c.execute("SELECT * FROM log WHERE commentid = ?", (commentid,))
    x = c.fetchall()
    if len(x) > 0:
        return True
    else:
        return False


def query_threadid(threadid):
    c.execute("SELECT * FROM log WHERE threadid = ?", (threadid,))
    x = c.fetchall()
    if len(x) > 0:
        return True
    else:
        return False


def count_ratings(base):
    c.execute(f"select count(*) from {base}")
    totalratings = str(c.fetchone())
    newratings = int(totalratings.translate({ord(i): None for i in '(),'}))
    return newratings


def query_existing(base, name):
    c.execute(f"SELECT rowid FROM {base} WHERE username = '{name}'")
    existing = c.fetchall()
    if len(existing) == 0:
        if constants.debugsearch:
            print(f"There is no existing rating for {name} in {base}")
            print("queryexisting returning false")
        return False
    else:
        print(f"There is an existing rating for {name} in {base}, updating rating.")
        return True
