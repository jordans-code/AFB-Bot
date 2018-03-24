import database as db


def getsearch(session, base):
    """Main function, returns proper format of links and sneak peak of a comment."""
    threesubmissions, topcomment = getthree(session, base)
    if not threesubmissions:
        return """I could not find a discussion in /r/RateMyAFB for this base, perhaps you could
[start one?](https://www.reddit.com/r/RateMyAFB/submit?selftext=true)\n\n"""
    reply = getreply(threesubmissions, topcomment)
    return reply


def getthree(session, base):
    """Gets the three most relevant submissions from ratemyafb, or as many as it can."""
    allsubmissions = []
    for submission in session.subreddit('ratemyafb').search(f"{base}"):
        allsubmissions.append(submission)
    if len(allsubmissions) >= 3:
        threesubmissions = [allsubmissions[2], allsubmissions[1], allsubmissions[0]]
        topcomment = gettopcomment(threesubmissions[0], threesubmissions[1], threesubmissions[2])
    elif len(allsubmissions) == 2:
        threesubmissions = [allsubmissions[1], allsubmissions[0]]
        topcomment = gettopcomment(threesubmissions[0], threesubmissions[1], False)
    elif len(allsubmissions) == 1:
        threesubmissions = [allsubmissions[0]]
        topcomment = gettopcomment(threesubmissions[0], False, False)
    else:
        return "", ""
    return threesubmissions, topcomment


def getreply(threesubmissions, topcomment):
    """Generates reply text"""
    commentsneakpeak = sneakpeak(topcomment)
    if len(threesubmissions) == 1:
        sub1 = getformat(threesubmissions[0], True)
    else:
        sub1 = getformat(threesubmissions[0], False)
    reply = f"""Have a question or wish to join in a discussion? Check out the below submission:\n\n
{sub1}\n\n{commentsneakpeak}"""
    if len(threesubmissions) >= 2:
        sub2 = getformat(threesubmissions[1], False)
        reply = f"""Have a question or wish to join in a discussion? Check out the below submissions:\n\n
{sub1} | {sub2}\n\n{commentsneakpeak}"""
    if len(threesubmissions) >= 3:
        sub3 = getformat(threesubmissions[2], False)
        reply = f"""Have a question or wish to join in a discussion? Check out the below submissions:\n\n
{sub1} | {sub2} | {sub3}\n\n{commentsneakpeak}"""

    return reply


def getformat(sub, single):
    """Shortens submission titles and returns proper format"""
    url = f"https://www.reddit.com/r/RateMyAFB/comments/{sub.id}"
    if single:
        maxlength = 64
    else:
        maxlength = 28
    title = list(sub.title)
    if len(title) > maxlength:
        del title[maxlength:len(title)]
        title.insert(len(title), "-")
    joinedtitle = ''.join(title)
    full = f"[{joinedtitle}]({url})"
    return full


def gettopcomment(sub1, sub2, sub3):
    """Gets a list of comments and sorts by top, and checks if the comment is blacklisted"""
    if db.checkblacklisted(False, sub1.id):
        if sub2 and not db.checkblacklisted(False, sub2.id):
            sub = sub2
        elif sub3 and not db.checkblacklisted(False, sub3.id):
            sub = sub3
        else:
            return ""
    else:
        sub = sub1
    sub.comment_sort = 'top'
    commentlist = sub.comments.list()
    commentlist.sort(key=lambda comment: comment.score, reverse=True)
    delete = []
    for i in range(len(commentlist)):
        if commentlist[i].body == "[deleted]":
            delete.append(i)
        elif db.checkblacklisted(False, commentlist[i].id):
            delete.append(i)
    if delete:
        for index in sorted(delete, reverse=True):
            del commentlist[index]

    if len(commentlist) > 0:
        return commentlist[0]
    else:
        return ""


def sneakpeak(comment):
    """Generates a sneak peak of a comment if possible."""
    if comment == "":
        return ""
    else:
        listbody = list(comment.body)
        if len(listbody) > 360:  # Kills comment after 4 line breaks.
            breaks = 0
            for i in range(len(listbody)):
                if breaks > 4:
                    del listbody[i:len(listbody)]
                    break
                if listbody[i] == '\n':
                    breaks += 1
        if len(listbody) > 1000:  # Prevents wall of text with no line breaks from getting through.
            del listbody[1001:len(listbody)]
        quoted = quotetext(listbody)
        joinedbody = ''.join(quoted)
        final = f"""*Sneak peak of a top [comment](https://www.reddit.com/r/ratemyafb/comments/{comment.submission.id}//{comment.id})
by [{comment.author}](https://www.reddit.com/user/{comment.author}):*
\n\n{joinedbody}\n\n"""
        return final


def quotetext(listtext):
    """Formats text to be quoted"""
    listtext.insert(0, '>')
    totalbreaks = 0
    if listtext[len(listtext) - 1] == '\n':
        del listtext[len(listtext) - 1]
    for i in range(len(listtext)):
        if listtext[i] == "\n" and listtext[i + 1] == "\n":
            totalbreaks += 1
    if totalbreaks == 2:
        break1 = 0
        for i in range(len(listtext)):
            if listtext[i] == "\n" and listtext[i + 1] == "\n":
                break1 = i + 1
                break
        break2 = 0
        for i in range(len(listtext) - 1, break1, -1):
            if listtext[i] == "\n" and listtext[i - 1] == "\n":
                break2 = i
                break
        listtext.insert(break1 + 1, '>')
        listtext.insert(break2 + 2, '>')
        return listtext
    elif totalbreaks == 2:
        for i in range(len(listtext)):
            if listtext[i] == "\n" and listtext[i + 1] == "\n":
                listtext.insert(i + 2, '>')
                break
        return listtext
    elif totalbreaks == 0:
        return listtext

    else:
        print("Something weird happened while getting comment quote: " + str(listtext))
        return ""