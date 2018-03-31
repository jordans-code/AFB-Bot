import database as db


def getsearch(session, base):
    """Main function, returns proper format of links and sneak peak of a comment."""
    sublist = getsubs(session, base)
    topcomments = gettopcomments(sublist)
    url = "[Create your own discussion.](https://www.reddit.com/r/RateMyAFB/submit)"
    if not sublist:
        return f"""I could not find a discussion in /r/RateMyAFB for this base, perhaps you could
[start one?](https://www.reddit.com/r/RateMyAFB/submit?selftext=true)\n\n{url}\n\n"""
    reply = getreply(sublist, topcomments)
    return reply

def getsubs(session, base):
    allsubmissions = []
    for submission in session.subreddit('ratemyafb').search(f"{base}"):
        if not db.checkblacklisted(submission.author, submission.id):
            allsubmissions.append(submission)
    return allsubmissions


def getreply(sublist, topcomments):
    """Generates reply text"""
    if len(topcomments) > 0:
        commentsneakpeak = sneakpeak(topcomments[0], True)
    else:
        commentsneakpeak = ""
    if len(sublist) == 1:
        sub1 = getformat(sublist[0], True)
    else:
        sub1 = getformat(sublist[0], False)
    reply = f"""Have a question or wish to join in a discussion? Check out the below submission:\n\n
{sub1}\n\n{commentsneakpeak}"""
    if len(sublist) >= 2:
        sub2 = getformat(sublist[1], False)
        reply = f"""Have a question or wish to join in a discussion? Check out the below submissions:\n\n
{sub1} | {sub2}\n\n{commentsneakpeak}"""
    if len(sublist) >= 3:
        sub3 = getformat(sublist[2], False)
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


def gettopcomments(sublist):
    """Gets a list of comments and sorts by top, and checks if the comment is blacklisted.
    Because of reddit's fuzzing of comment scores this is not 100% accurate resulting in
    slightly different scores each time."""
    topcomments = []
    for sub in sublist:
        sub.comment_sort = 'top'
        sub.comments.replace_more(limit=None, threshold=0)
        commentlist = sub.comments.list()

        commentlist.sort(key=lambda comment: comment.score, reverse=True)
        delete = []
        for i in range(len(commentlist)):
            if commentlist[i].body == "[deleted]":
                delete.append(i)
            elif db.checkblacklisted(commentlist[i].author, commentlist[i].id):
                delete.append(i)
        if delete:
            for index in sorted(delete, reverse=True):
                del commentlist[index]

        if len(commentlist) > 0:
            topcomments.append(commentlist[0])
        if len(commentlist) > 1:
            topcomments.append(commentlist[1])
    topcomments.sort(key=lambda comment: comment.score, reverse=True)
    return topcomments


def sneakpeak(comment, shorten):
    """Generates a sneak peak of a comment if possible."""
    if comment == "":
        return ""
    else:
        listbody = list(comment.body)
        for i in range(len(listbody)):
            if listbody[i] == '|':
                listbody[i] = ' '
        if shorten:
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
        quoted = quotetext(listbody, shorten)
        joinedbody = ''.join(quoted)
        final = f"""*Sneak peak of a top [comment](https://www.reddit.com/r/ratemyafb/comments/{comment.submission.id}//{comment.id})
by [{comment.author}](https://www.reddit.com/user/{comment.author}):*
\n\n{joinedbody}\n\n"""
        return final


def quotetext(listtext, notwiki):
    """Formats text to be quoted"""
    listtext.insert(0, '>')
    totalbreaks = 0
    while listtext[len(listtext) - 1] == '\n':
        del listtext[len(listtext) - 1]
    for i in range(len(listtext)):
        if listtext[i] == "\n" and listtext[i + 1] == "\n":
            totalbreaks += 1
        if notwiki:
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
            addquotespots = []
            for i in range(len(listtext)):
                if listtext[i] == "\n" and listtext[i + 1] == "\n":
                    addquotespots.append(i + 1)
                    continue
                elif listtext[i] == "\n" and listtext[i - 1] != "\n":
                    addquotespots.append(i + 1)
            if addquotespots:
                for index in sorted(addquotespots, reverse=True):
                    listtext.insert(index, ">")
            return listtext

    else:
        print("Something weird happened while getting comment quote: " + str(listtext))
        return ""

 #  Wiki stuff ----------------


def getwikisearch(session, base):
    url = "[Create your own discussion.](https://www.reddit.com/r/RateMyAFB/submit)"
    sublist = getsubs(session, base)
    if not sublist:
        return f"""##Discussions\nThere are no discussions in /r/RateMyAFB for this base, perhaps you could
start one?\n\n{url}\n\n"""
    topclist = gettopcomments(sublist)
    reply = getwikiformat(sublist, topclist)
    return reply


def getwikiformat(sublist, topclist):
    url = "[Create your own discussion.](https://www.reddit.com/r/RateMyAFB/submit)"
    sub1 = getsublistformat(sublist[0])
    sub2, sub3, sub4, sub5 = "", "", "", ""
    if len(sublist) > 1:
        sub2 = getsublistformat(sublist[1])
    if len(sublist) > 2:
        sub3 = getsublistformat(sublist[2])
    if len(sublist) > 3:
        sub4 = getsublistformat(sublist[3])
    if len(sublist) > 4:
        sub5 = getsublistformat(sublist[4])
    if not topclist:
        topc1 = "No comments found."
    else:
        topc1 = sneakpeak(topclist[0], False)
    topc2 = ""
    topc3 = ""
    if len(topclist) > 1:
        topc2 = sneakpeak(topclist[1], False)
    if len(topclist) > 2:
        topc3 = sneakpeak(topclist[2], False)
    format = f"""##Discussions\nStatus | Discussion Title\n- | -\n{sub1}{sub2}{sub3}{sub4}{sub5}
\n{url}\n##Top Comments\n{topc1}{topc2}{topc3}"""
    return format

def getsublistformat(sub):
    listtitle = list(sub.title)
    for i in range(len(listtitle)):
        if listtitle[i] == '|':
            listtitle[i] = ' '
            continue
        elif listtitle[i] == '-':
            listtitle[i] = ' '
            continue
        else:
            continue
    joinedtitle = ''.join(listtitle)
    url = f"[{joinedtitle}](https://www.reddit.com/r/RateMyAFB/comments/{sub.id})"
    status = sub.archived
    if status:
        status = "Archived"
    else:
        status = "Open"
    final = f"""{status} | {url}\n"""
    return final