import praw
import prawcore
import constants as c
import time
import bases


def reddit_login():
    if c.debuglogin:
        print("Logging in...")
    login = praw.Reddit(username=c.reddit_user,
                        password=c.reddit_pass,
                        client_id=c.reddit_api,
                        client_secret=c.reddit_secret,
                        user_agent="Air Force Base Bot /r/AFBbot")

    if c.debuglogin:
        print("Logged in!")
    #  bases.db.log('Login', None, None, None, None, None, 'Successfully Logged In')
    return login


comments_checked = []  # temporary, this is a fail safe for if the log fails and stops us from rechecking posts.
comment_checking = [None, None, None, None, None, None, None]


def checkbases(comment):  # Checks all base instances and checks to see if someone is trying to rate one.
    linebreaktext = list(comment.body.lower())
    checktext = filtertext(linebreaktext).split()
    stringtext = ''.join(checktext)
    if c.debugsearch:
        print(str(checktext))
    for base in bases.all_bases:
        for name in base.names:
            if name in checktext:
                if not bases.db.query_commentid(comment.id):  # check if we have already handled comment
                    if "rate" in checktext and checkvalidrating(stringtext):
                        if c.debugsearch:
                            print("User appears to be rating base.")
                        rating = getratingnumber(ratingfilter(list(comment.body.lower())))
                        if not c.debugnoreply:
                            rated_reply(comment, base, rating, "comment")
                    else:
                        for trigger in c.triggers:
                            if trigger.lower() in checktext:
                                bases.db.log('reply', base.names[0], name, None, comment.id,
                                             comment.submission.id, None)
                                reply(comment, base)
                            else:
                                pass
                else:
                    pass  # Already checked this comment.
            else:
                continue


def checkbasesthread(thread):  # Checks all base instances and checks to see if someone is trying to rate one.
    linebreaktext = list(thread.selftext.lower())
    checktext = filtertext(linebreaktext).split()
    stringtext = ''.join(checktext)
    global comments_checking
    for base in bases.all_bases:
        for name in base.names:
            if name in checktext:
                if not bases.db.query_commentid(thread.id):  # check if we have already handled comment
                    comments_checking[0] = name
                    if "rate" in checktext and checkvalidrating(stringtext):
                        if c.debugsearch:
                            print("User appears to be rating base.")
                        rating = getratingnumber(ratingfilter(list(thread.selftext.lower())))
                        comments_checking[2] = rating
                        rated_reply(thread, base, rating, "thread")
                    else:
                        for trigger in c.triggers:
                            if trigger.lower() in checktext:
                                bases.db.log('reply', base.names[0], name, None, thread.id, thread.id, None)
                                reply(thread, base)
                            else:
                                pass
                else:
                    pass
            else:
                continue


def ratingfilter(text):
    noquotetext = filterqtext(text)
    for char in noquotetext:
        if char == "\n":
            noquotetext[char] = ""
    if c.debugsearch:
        print("start of filtered text: " + str(noquotetext))
    filterchars = '!@#$%^&*()+<>=,?:;'
    filteredtext = ''.join(noquotetext)
    filteredtext = filteredtext.replace("/", " ")
    if c.debugsearch:
        print(str(filteredtext))
    for char in filterchars:
        filteredtext = filteredtext.replace(char, "")
    checktext = filteredtext.split()
    if c.debugsearch:
        print(str(checktext))
    return checktext


def filtertext(text):
    noquotetext = filterqtext(text)
    if c.debugsearch:
        print(noquotetext)
    for i in range(len(noquotetext)):
        if noquotetext[i] == "'":
            noquotetext[i] = ""
    filterchars = '!@#$%^&*()/-;+<>=,.?:'
    filteredtext = ''.join(noquotetext)
    for char in filterchars:
        filteredtext = filteredtext.replace(char, "")
    if c.debugsearch:
        print("Symbols have been removed: " + str(filteredtext))
    checktext = ''.join(filteredtext)
    if c.debugsearch:
        print("Final check to text: " + checktext)
    return checktext


def filterqtext(text):  # prevents replying to quoted text and for things like "langley?" from not being queried.
    checkquote = text
    if c.debugsearch:
        print("I am checking" + (str(text)) + "for a quote mark, I see " + str(checkquote[0][0]))
    if checkquote[0][0] == '>':
        if c.debugsearch:
            print("Quote found")
        if "\n" in checkquote:
            for z in range(len(checkquote)):
                for char2 in checkquote[z]:
                    if char2 == '\n':
                        if c.debugsearch:
                            print("Line break found")
                            print("Quote: " + str(checkquote))
                        del checkquote[0:(z + 2)]
                        if ">" in checkquote:
                            if c.debugsearch:
                                print("Multi quote comment, will not reply.")
                            return ""
                        else:
                            return checkquote
            else:
                if c.debugsearch:
                    print("No line break found, not replying.")
                return ""
    return checkquote


def checkvalidrating(comment):
    splitlist = comment.split("rate")
    del splitlist[0]
    joinedlist = ''.join(splitlist)
    if c.debugsearch:
        print(str(joinedlist))
    numbers = [int(x) for x in comment if x.isdigit()]
    if c.debugsearch:
        print(str(numbers))
    if c.debugsearch:
        print("Checking if the rating is valid, I found these numbers: " + str(numbers) + "Length "
              + str(len(numbers)))
    if len(numbers) < 1:
        if c.debugsearch:
            print("No numbers, returning with a reply instead of a rating")
        return False
    else:
        return True


def getratingnumber(text):
    delete = []  # deletes everything up to and including the indexes "rate"
    for i in range(len(text)):
        word = text[i]
        if word == 'rate':
            for z in range(0, i):
                delete.append(z)
            continue
    for i in sorted(delete, reverse=True):
        del text[i]

    delete = []  # deletes every index that begins with an alpha character, only need numbers/periods at this point.
    for i in range(len(text)):
        word = list(text[i])
        realword = word[0]
        if realword.isalpha():
            delete.append(i)
            continue
    for i in sorted(delete, reverse=True):
        del text[i]

    finalnumber = []

    for char in text:
        number = []
        appenededperiod = False  # Weird way of doing this but works, prevents something like "9.5." from happening.
        charlist = list(char)  # Also handles weird things like 52.643096.4,.,53//432
        for i in range(len(charlist)):
            if charlist[i] == ".":
                if not appenededperiod:
                    number.append(".")
                    appenededperiod = True
            else:
                number.append(str(charlist[i]))
        if c.debugsearch:
            print(str(number))
        truenumber = ''.join(str(i) for i in number)
        finalnumber.append(truenumber)
    if c.debugsearch:
        print(str(finalnumber))

    numbers = [float(x) for x in finalnumber if not x.isalpha()]
    if c.debugsearch:
        print(str(numbers))

    if numbers[0] > 10:
        return 10.00
    elif 1 <= numbers[0] <= 10:
        rounded = "%.2f" % numbers[0]
        return rounded
    elif numbers[0] <= 1:
        return 1.00
    else:
        print("Something weird happened with the getrating number, " + str(numbers[0]))
        return 10.00


def reply(comment, base):
    print("Adding reply to " + str(comment.id))
    if not c.debugnoreply:
        comment.reply(f"""{base.displayname}{base.getmajcom()} is located in {base.location}\n\n
Base rating: {str(base.getrating())}/10 out of {str(bases.db.count_ratings(base.names[0]))} ratings.\n\n"""
                      + c.bot_signature)


def rated_reply(comment, base, rating, self):
    if self == "comment":
        print("Adding rating to " + str(comment.id))  # Checks if they have already added a rating to this base
        if base.addrating(str(comment.author), rating, comment.id, comment.submission.id):
            if not c.debugnoreply:
                comment.reply(f'''Your rating has been added to {base.displayname}.\n\n
Base rating: {str(base.getrating())}/10 out of {str(bases.db.count_ratings(base.names[0]))} ratings.\n\n'''
                              + c.bot_signature)
        else:
            base.changerating(str(comment.author), rating, comment.id, comment.submission.id)
            if not c.debugnoreply:
                comment.reply(f'''Your rating of {base.displayname} has been changed to {str(rating)}.  
Base rating: {str(base.getrating())}/10 out of {str(bases.db.count_ratings(base.names[0]))} ratings.\n\n'''
                              + c.bot_signature)
    else:
        print("Adding rating to " + str(comment.id))
        if base.addrating(str(comment.author), rating, comment.id,
                          comment.id):
            if not c.debugnoreply:  # Checks if they have already added a rating to this base
                comment.reply(f'''Your rating has been added to {base.displayname}.\n\n
Base rating: {str(base.getrating())}/10 out of {str(bases.db.count_ratings(base.names[0]))} ratings.\n\n'''
                              + c.bot_signature)
        else:
            base.changerating(str(comment.author), rating, comment.id, comment.id)
            if not c.debugnoreply:
                comment.reply(f'''Your rating of {base.displayname} has been changed to {str(rating)}.  
Base rating: {str(base.getrating())}/10 out of {str(bases.db.count_ratings(base.names[0]))} ratings.\n\n'''
                              + c.bot_signature)


def bot_main(login):
    global comments_checking
    try:
        comments_checking = [None, None, None, None, None, None, None]
        session = login
        print("Checking comments...")
        for sub in c.reddit_subs:
            print("Checking in sub " + str(sub))
            for comment in session.subreddit(sub).comments(limit=20):  # Need to check for locked thread, throws except
                if comment.id not in comments_checked and comment.author != c.reddit_user\
                        and len(comment.body.lower()) > 0:
                    comments_checking[1] = comment.author
                    comments_checking[3] = comment.id
                    comments_checking[4] = comment.submission.id
                    if c.debugsearch:
                        print("Comment " + str(comment.id) + " is not in " + str(comments_checked))
                    comments_checked.append(comment.id)
                    checkbases(comment)
                else:
                    continue
            print("Checking threads...")
            for thread in session.subreddit(sub).new(limit=5):
                if thread.id not in comments_checked and len(thread.selftext.lower()) > 0:
                    comments_checking[1] = thread.author
                    comments_checking[3] = thread.id
                    comments_checking[4] = thread.id
                    comments_checked.append(thread.id)
                    checkbasesthread(thread)

    except prawcore.exceptions.OAuthException as e:
        bases.db.log('Login Error', None, None, None, None, None, str(e))
        print("Invalid credentials while logging in!")
        time.sleep(15)

    except Exception as e:
        print (f"Logging {comments_checking[0]} {comments_checking[1]} {comments_checking[2]} {comments_checking[3]} {comments_checking[4]} {e}")
        bases.db.log('Error', str(comments_checking[0]), str(comments_checking[1]), comments_checking[2],
                     str(comments_checking[3]), str(comments_checking[4]), str(e))
        print(e)
    else:
        print("Completed loop successfully.")

    finally:
        print("Sleeping...")
        time.sleep(30)


if __name__ == "__main__":
    if c.createdb:
        bases.maketables()
    while True:  # Main loop
        bot_main(reddit_login())
