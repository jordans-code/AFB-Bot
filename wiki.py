import bases
import search
import wikipedia
import constants as c
import prawcore
import time

class Wiki(object):
    def __init__(self):
        self.currentsession = None
        self.updatedict = {}
        self.filldict()

    def update(self, session):
        self.currentsession = session
        self.main()

    def filldict(self):
        for i in range(len(bases.all_bases)):
            self.updatedict[bases.all_bases[i]] = i

    def getorderedlist(self):
        d = self.updatedict
        orderedlist = [(k, d[k]) for k in sorted(d, key=d.get)]
        if c.debugwiki:
            print("Ordered list: ")
            print(str(orderedlist))
        return orderedlist

    def main(self):
        values = self.getorderedlist()

        for i in range(3):
            self.updatedict[values[i][0]] = time.time()
            page = checkforpage(self.currentsession, values[i][0])
            if page:
                if c.debugwiki:
                    print("Checking if i need to update the page for " + str(values[i][0].names[0]))
                self.checkforupdate(values[i][0], page)


    def checkforupdate(self, base, old):
        current = genpage(self.currentsession, base)
        if old == current:
            if c.debugwiki:
                print(str(current) + str(old))
                print("Matching!")
            return True
        else:
            if c.debugwiki:
                print(str(current) + str(old))
                print("Not matching!")
            updatepage(self.currentsession, current, base)
            return False

maintainer = Wiki()


def checkforpage(session, base):
    """Checks if a wiki page exists"""
    try:
        wikipage = session.subreddit('ratemyafb').wiki[f'bases/{base.names[0]}']
        useless = wikipage.content_md
    except prawcore.exceptions.NotFound:
        print("Creating wiki page for: " + str(base.names[0]))
        createpage(session, base)
        return False
    except prawcore.exceptions.BadRequest as e:
        print("400 response: " + str(e))
        print(str(base.names[0]) + str(session))
    except prawcore.exceptions.RequestException as e:
        print("Reddit timed out, sleeping and retrying. " + str(e))
    except Exception as e:
        print(str(e))
    else:
        return useless


def createpage(session, base):
    try:
        session.subreddit('ratemyafb').wiki.create(f"bases/{base.names[0]}", f"{genpage(session, base)}",
reason="""Bleep Bloop, initial page creation.""")
        if c.debugwiki:
            print("Created wiki page for " + str(base.names[0]))
    except Exception as e:
        print("Bot may not have permisson to create a new wiki page." + str(e))


def updatepage(session, content, base):
    page = session.subreddit('ratemyafb').wiki[f'bases/{base.names[0]}']
    page.edit(content, reason="Bleep Bloop, updating the page.")
    if c.debugwiki:
        print("Updated page!")


def genpage(session, base):
    "Generates the text for an entire wiki page"
    if c.debugwiki:
        print("Generating wiki page for " + (str(base.displayname)))
    wikisummary = getwiki(base)
    ratings = getratings(base)
    discussions = search.getwikisearch(session, base.names[0])
    final = f"""#{base.displayname}\n{wikisummary}\n\n---\n\n
{ratings}{discussions}"""
    if c.debugwiki:
        print(str(final))
    return final


def getwiki(base):
    """Gets actual Wikipedia article summary"""
    try:
        summary = wikipedia.summary(f"{base.displayname}")
    except Exception as e:
        print("Wiki too busy, sleeping. " + str(e))
        time.sleep(10)
    else:
        return summary


def getratings(base):
    """Generates all ratings and places in format for wiki"""
    url = f"""*Want to add a rating?* [Check out the bot usage page.](https://www.reddit.com/r/AFBbot/wiki/about)"""
    overall = str(base.gettrueoverallrating())
    overalltotal = str(bases.db.count_ratings(base.names[0], False))
    general = str(base.getrating("rate"))
    generaltotal = str(bases.db.count_ratings(base.names[0], "rate"))
    area = str(base.getrating("arearate"))
    areatotal = str(bases.db.count_ratings(base.names[0], "arearate"))
    housing = str(base.getrating("housingrate"))
    housingtotal = str(bases.db.count_ratings(base.names[0], "housingrate"))
    final = f"""##Ratings\nCategory | Rating | Total Ratings\n- | - | -
**Overall Rating** | {overall}/10 | {overalltotal}
General Rating | {general}/10 | {generaltotal}
Local Area Rating | {area}/10 | {areatotal}
Housing Rating | {housing}/10 | {housingtotal}\n\n{url}\n\n"""
    return final


