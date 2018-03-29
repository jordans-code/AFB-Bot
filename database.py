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
    c.execute(f'''CREATE TABLE IF NOT EXISTS {base}(unix REAL, datestamp TEXT, username TEXT, commentid TEXT,
    ratingtype TEXT, value REAL)''')
    db.commit()


def create_logtable():
    c.execute('''CREATE TABLE IF NOT EXISTS log(unix REAL, datestamp TEXT, type TEXT, base TEXT, 
    username TEXT, value REAL, commentid TEXT, threadid TEXT, message TEXT)''')


def create_blacklist():
    c.execute('''CREATE TABLE IF NOT EXISTS blacklist(username TEXT, commentid TEXT)''')


def data_entry(base, name, rtype, rating, commentid, threadid):
    unix = time.time()
    now = datetime.datetime.now()
    datestamp = f"{now.year}-{now.month}-{now.day}"
    print(f"insert into {base} {unix} {datestamp} {name} {commentid} {rating} {rtype}")
    c.execute(f"INSERT INTO {base} VALUES(?, ?, ?, ?, ?, ?)", (unix, datestamp,
                                                            name, commentid, rtype, rating),)

    c.execute("INSERT INTO log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (unix, datestamp, rtype, base,
                                                                    name, rating, commentid, threadid, None),)
    db.commit()


def checkblacklisted(User, ID):
    if User and ID:
        c.execute(f"SELECT rowid FROM blacklist WHERE commentid = '{ID}' OR username = '{User}'")
        existing = c.fetchall()
        if len(existing) != 0:
            if constants.debugsearch:
                print("User or ID is blacklisted, ignoring.")
            return True
    if not User:
        c.execute(f"SELECT rowid FROM blacklist WHERE commentid = '{ID}'")
        existing = c.fetchall()
        if len(existing) == 0:
            return False
        else:
            return True
    if not ID:
        c.execute(f"SELECT rowid FROM blacklist WHERE username = '{User}'")
        existing = c.fetchall()
        if len(existing) == 0:
            return False
        else:
            return True


def change_entry(base, name, rtype, rating, commentid, threadid):
    unix = time.time()
    now = datetime.datetime.now()
    datestamp = f"{now.year}-{now.month}-{now.day}"
    c.execute(f"UPDATE {base} SET unix = ?, datestamp = ?, commentid = ?, value = ? WHERE username = ? AND ratingtype = ?",
              (unix, datestamp, commentid, rating, name, rtype),)

    c.execute("INSERT INTO log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (unix, datestamp, rtype, base,
                                                                    name, rating, commentid, threadid, 'change'),)
    db.commit()


def query_rating(base, rtype):
    c.execute(f"SELECT TOTAL(value) FROM {base} WHERE ratingtype = '{rtype}'")
    ratings = str(c.fetchone())
    ratings = ratings.translate({ord(i): None for i in '(),'})
    userratings = count_ratings(base, rtype)
    ratingssum = float(ratings)
    if constants.debugsearch:
        pass
    if constants.debugsearch:
        print(f"Querying rating of {base}, there are {userratings} ratings")
    if userratings == 0:
        return 10
    else:
        final = ratingssum / userratings
        return final


def query_overallrating(base):
    general = float(query_rating(base, "rate"))
    area = float(query_rating(base, "arearate"))
    housing = float(query_rating(base, "housingrate"))
    sum = general + area + housing
    final = sum / 3
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


def count_ratings(base, rtype):
    """Returns the total number of ratings for a base."""
    if rtype:
        c.execute(f"select count(*) from {base} WHERE ratingtype = '{rtype}'")
        totalratings = str(c.fetchone())
        newratings = int(totalratings.translate({ord(i): None for i in '(),'}))
        return newratings
    else:
        c.execute(f"select count(*) from {base}")
        totalratings = str(c.fetchone())
        newratings = int(totalratings.translate({ord(i): None for i in '(),'}))
        return newratings


def query_existing(base, name, rtype):
    """Check for an existing rating by the comment/thread author for the base."""
    c.execute(f"SELECT rowid FROM {base} WHERE username = '{name}' AND ratingtype = '{rtype}'")
    existing = c.fetchall()
    if len(existing) == 0:
        if constants.debugsearch:
            print(f"There is no existing rating for {name} in {base} for {rtype}")
            print("queryexisting returning false")
        return False
    else:
        if constants.debugsearch:
            print(f"There is an existing rating for {name} in {base} for {rtype}, updating rating.")
        return True
