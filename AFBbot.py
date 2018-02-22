import praw
import constants as c
import time

def reddit_login():
    if c.debuglogin:
        print ("Logging in...")
    login = praw.Reddit(username = c.reddit_user,
                    password = c.reddit_pass,
                    client_id = c.reddit_api,
                    client_secret = c.reddit_secret,
                    user_agent = "Air Force Base Bot /r/AFBbot")
    if c.debuglogin:
        print ("Logged in!")
    return login


def bot_main(login):
    comments_replied_to = []
    session = login
    for sub in c.reddit_subs:
        if c.debugsearch:
            print (sub)
        for comment in session.subreddit(sub).comments(limit=20):
            if c.debugsearch:
                print (comment)
            if "Langley" in comment.body and comment.id not in comments_replied_to and comment.author != c.reddit_user:
                print ("I see a base!")
                print (str(comments_replied_to))
                comment.reply('''JB Langley-Eustis is located in Virginia, United States.  
                              Overall base rating:  
                              [Base Discussion]  
                               ---------------------------------------------------  
                                ^^I ^^am ^^a ^^bot. ^^To ^^rate ^^a ^^base ^^simply ^^write ^^the ^^name ^^followed 
                              ^^by ^^a ^^comma ^^and ^^an ^^integer ^^between ^^1-10. ^^Ex: ^^Langley, ^^5. ^^If ^^you 
                              ^^already ^^rated ^^that ^^base ^^your ^^rating ^^will ^^be ^^changed.''')
                comments_replied_to.append(comment.id)
            else:
                print ("I do not see a match")

    time.sleep(10) # Delay


if __name__ == "__main__":
    while True: # Main loop
        bot_main(reddit_login())


