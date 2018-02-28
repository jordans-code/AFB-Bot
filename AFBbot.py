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
    bases.db.log('Login', None, None, None, None, None, 'Successfully Logged In')
    return login


comments_checked = []


def checkbases(comment):  # Checks all base instances and checks to see if someone is trying to rate one.
    filterchars = '!@#$%^&*()-+<>=,.?:'
    filteredtext = comment.body.lower()
    for char in filterchars:
        filteredtext = filteredtext.replace(char, "")
    checktext = filteredtext.split()
    for base in bases.all_bases:
        for name in base.names:
            if name in checktext:
                if not bases.db.query_commentid(comment.id):  # check if we have already handled comment
                    if "rate" in checktext and checkvalidrating(comment.body.lower()):
                        if c.debugsearch:
                            print("User appears to be rating base.")
                        rating_list = list(comment.body)
                        rating = getratingnumber(rating_list)
                        bases.db.log('rate', base.names[0], name, rating, comment.id, comment.submission.id, None)
                        rated_reply(comment, base, rating)
                        print("Done!")
                    else:
                        for trigger in c.triggers:
                            if trigger.lower() in checktext:
                                bases.db.log('reply', base.names[0], name, None, comment.id, comment.submission.id, None)
                                reply(comment, base)
                            else:
                                pass
                else:
                    pass  # Already checked this comment.
            else:
                continue


def checkbasesthread(thread):  # Checks all base instances and checks to see if someone is trying to rate one.
    filterchars = '!@#$%^&*()-+<>=,.?:'
    filteredtext = thread.selftext.lower()
    for char in filterchars:
        filteredtext = filteredtext.replace(char, "")
    checktext = filteredtext.split()
    for base in bases.all_bases:
        for name in base.names:
            if name in checktext:
                if not bases.db.query_commentid(thread.id):  # check if we have already handled comment
                    if "rate" in checktext and checkvalidrating(thread.selftext.lower()):
                        if c.debugsearch:
                            print("User appears to be rating base.")
                        rating_list = list(thread.selftext.lower())
                        rating = getratingnumber(rating_list)
                        bases.db.log('rate', base.names[0], name, rating, thread.id, thread.id, None)
                        rated_reply(thread, base, rating)
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


def checkvalidrating(comment):
    numbers = [int(x) for x in comment if x.isdigit()]
    if c.debugsearch:
        print("Checking if the rating is valid, I found these numbers: " + str(numbers) + "Length "
               + str(len(numbers)))
    if len(numbers) > 2:
        if c.debugsearch:
            print ("More than 2 numbers, returning with a reply instead of a rating")
        return False
    elif len(numbers) < 1:
        if c.debugsearch:
            print("No numbers, returning with a reply instead of a rating")
        return False
    elif len(numbers) == 2:
        if int(str(numbers[0]) + str(numbers[1])) == 10:
            return True
        else:
            if c.debugsearch:
                print("Found 2 numbers but they are not 10, returning False")
            return False
    elif len(numbers) == 1:
        if numbers[0] in range(1, 10):
            return True
        else:
            if c.debugsearch:
                print("Found a number but it is not in range of 1 - 10, returning false.")
            return False


def getratingnumber(text):
    numbers = [int(x) for x in text if x.isdigit()]
    if len(numbers) == 2:
        if int(str(numbers[0]) + str(numbers[1])) == 10:
            return 10
    elif len(numbers) == 1:
        if numbers[0] in range(1, 10):
            return numbers[0]
    else:
        print ("Invalid rating number " + str(numbers))
        return 5


def reply(comment, base):
    print ("Adding reply to " + str(comment.id))
    comment.reply(f"""{base.displayname}{base.getmajcom()} is located in {base.location}\n\n
Base rating: {str(base.getrating())}/10 out of {str(bases.db.count_ratings(base.names[0]))} ratings.\n\n""" + c.bot_signature)


def rated_reply(comment, base, rating):
    print ("Adding rating to " + str(comment.id))
    if base.addrating(str(comment.author), rating, comment.id, comment.submission.id):  # Checks if they have already added a rating to this base
        comment.reply(f'''Your rating has been added to {base.displayname}.\n\n
Base rating: {str(base.getrating())}/10 out of {str(bases.db.count_ratings(base.names[0]))} ratings.\n\n''' + c.bot_signature)
    else:
        base.changerating(str(comment.author), rating, comment.id, comment.submission.id)
        comment.reply(f'''Your rating of {base.displayname} has been changed to {str(rating)}.  
Base rating: {str(base.getrating())}/10 out of {str(bases.db.count_ratings(base.names[0]))} ratings.\n\n''' + c.bot_signature)


def bot_main(login):
    try:
        session = login
        print("Checking comments...")
        for sub in c.reddit_subs:
            for comment in session.subreddit(sub).comments(limit=20):  # Need to check for locked thread, throws except
                if comment.id not in comments_checked and comment.author != c.reddit_user:
                    comments_checked.append(comment.id)
                    checkbases(comment)
                else:
                    if c.debugsearch:
                        print("I do not see a match")
            print("Checking threads...")
            for thread in session.subreddit(sub).new(limit=5):
                if thread.id not in comments_checked:
                    comments_checked.append(thread.id)
                    checkbasesthread(thread)

    except prawcore.exceptions.OAuthException as e:
        bases.db.log('Login Error', None, None, None, None, str(e))
        print("Invalid credentials while logging in!")
        time.sleep(15)
    except Exception as e:
        bases.db.log('Error', None, None, None, None, None, str(e))
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


