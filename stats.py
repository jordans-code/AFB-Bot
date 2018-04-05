import bases
import weather
import time
import constants
from collections import OrderedDict


class Stats:
    """Keeps track of weather info. Gets new information if the function is called and it has been
    over an hour since it last updated the weather."""
    lastweather = 0
    allweather = {}
    warmest = bases.minot
    coldest = bases.minot

    def getreply(self):
        """Main function, returns the comment."""
        Stats.temp(thestats)
        lowest, lowestvalue, highest, highestvalue = Stats.overallratings()

        reply = f"""Here are the overall stats,\n\n
Highest rated base overall: {highest.displayname}. {highestvalue}/10 from {bases.db.count_ratings(highest.names[0], False)} ratings.\n\n
Lowest rated base overall: {lowest.displayname}. {lowestvalue}/10 from {bases.db.count_ratings(lowest.names[0], False)} ratings.\n\n
Current highest base temperature: {self.warmest.displayname}. {weather.getweather(self.warmest.location, self.warmest.manualweather)}
Current lowest base temperature: {self.coldest.displayname}. {weather.getweather(self.coldest.location, self.coldest.manualweather)}"""
        return reply

    def temp(self):
        """Checks to see if we need to update weather information (1 hour intervals), then returns information."""
        if self.lastweather + 3600 < time.time():
            print(f"{str(self.lastweather + 1800)} < {time.time()}, getting new temps.")
            self.gettemps()
            self.lastweather = time.time()
            self.reporttemps()
            return True
        else:
            return True

    def gettemps(self):
        """Update allweather dictionary"""
        for base in bases.all_bases:
            if constants.debugweather:
                print("Getting weather for " + base.names[0])
            self.allweather[base.names[0]] = int(weather.getallweather(base.location, base.manualweather))
            time.sleep(1)

    def reporttemps(self):
        """Finds the coldest and warmest base from allweather"""
        alltemps = OrderedDict(sorted(self.allweather.items(), key=lambda z: z[1]))
        coldest = str(list(alltemps.keys())[0])
        warmest = str(list(alltemps.keys())[-1])
        for base in bases.all_bases:
            if base.names[0] == coldest:
                self.coldest = base
            elif base.names[0] == warmest:
                self.warmest = base

    @staticmethod
    def overallratings():
        allratings = {}
        for base in bases.all_bases:
            if bases.db.count_ratings(base.names[0], False) != 0:
                allratings[base.names[0]] = float(base.gettrueoverallrating())
        orderedratings = OrderedDict(sorted(allratings.items(), key=lambda a: a[1]))
        lowest = str(list(orderedratings.keys())[0])
        lowestvalue = str(list(orderedratings.values())[0])
        highest = str(list(orderedratings.keys())[-1])
        highestvalue = str(list(orderedratings.values())[-1])

        for base in bases.all_bases:
            if base.names[0] == lowest:
                lowest = base
            elif base.names[0] == highest:
                highest = base

        tenratings = {}
        if highestvalue == 10.0:
            """If the top rating is a 10 it then sorts by the 10 ratings with the most ratings."""
            for key, value in orderedratings:
                if value == 10.0:
                    tenratings[key] = int(bases.db.count_ratings(key, False))
            orderedcount = OrderedDict(sorted(tenratings.items(), key=lambda a: a[1]))
            highest = str(list(orderedcount.keys())[-1])
            highestvalue = str(list(orderedcount.values())[-1])
            return lowest, lowestvalue, highest, highestvalue
        else:
            return lowest, lowestvalue, highest, highestvalue


thestats = Stats()
