
def getsearch(session, base):
    threesubmissions = getthree(session, base)
    if not threesubmissions:
        return ""
    reply = getreply(threesubmissions)
    return reply


def getthree(session, base):
    """Gets the three most relevant submissions from ratemyafb, or as many as it can."""
    allsubmissions = []
    for submission in session.subreddit('ratemyafb').search(f"{base}"):
        allsubmissions.append(submission)
    if len(allsubmissions) >= 3:
        threesubmissions = [allsubmissions[0], allsubmissions[1], allsubmissions[2]]
    elif len(allsubmissions) == 2:
        threesubmissions = [allsubmissions[0], allsubmissions[1]]
    elif len(allsubmissions) == 1:
        threesubmissions = [allsubmissions[0]]
    else:
        return ""
    return threesubmissions


def getreply(threesubmissions):
    sub1 = getformat(threesubmissions[0])
    reply = f"""Discussion: {sub1}\n\n"""
    if len(threesubmissions) >= 2:
        sub2 = getformat(threesubmissions[1])
        reply = f"""Discussions: {sub1} | {sub2}\n\n"""
    if len(threesubmissions) >= 3:
        sub3 = getformat(threesubmissions[2])
        reply = f"""Discussions: {sub1} | {sub2} | {sub3}\n\n"""

    return reply


def getformat(sub):
    url = f"https://www.reddit.com/r/RateMyAFB/comments/{sub.id}"
    maxlength = 24
    title = list(sub.title)
    if len(title) > maxlength:
        del title[maxlength:len(title)]
    joinedtitle = ''.join(title)
    full = f"[{joinedtitle}]({url})"
    return full

