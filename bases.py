import database as db


class Base(object):
    def __init__(self, location, majcom, displayname, names):
        self.location = location
        self.majcom = majcom
        self.displayname = displayname
        self.names = names

    def addrating(self, author, rating, commentid, threadid):
        if db.query_existing(self.names[0], author):
            return False
        else:
            db.data_entry(self.names[0], author, rating, commentid, threadid)
            print(f"Added rating {rating} to {self.names[0]} by {author}")
            return True

    def getrating(self):
        overallrating = db.query_rating(self.names[0])
        roundedrating = "%.2f" % overallrating
        return roundedrating

    def changerating(self, author, rating, commentid, threadid):
        db.change_entry(self.names[0], author, rating, commentid, threadid)

    def getmajcom(self):
        if self.majcom is not None:
            x = self.themajcom(self.majcom)
            return f" falls under {x} and"
        else:
            return ""

    @staticmethod
    def themajcom(majcom):
        if majcom == "AETC":
            return "Air Education and Training Command (AETC)"
        elif majcom == "ACC":
            return "Air Combat Command (ACC)"
        elif majcom == "AFGSC":
            return "Air Force Global Strike Command (AFGSC)"
        elif majcom == "AFMC":
            return "Air Force Material Command (AFMC)"
        elif majcom == "AFRC":
            return "Air Force Reserve Command (AFRC)"
        elif majcom == "AFSPC":
            return "Air Force Space Command (AFSPC)"
        elif majcom == "AFSOC":
            return "Air Force Spcial Operations Command (AFSOC)"
        elif majcom == "AMC":
            return "Air Mobility Command (AMC)"
        elif majcom == "PACAF":
            return "Pacific Air Forces (PACAF)"
        elif majcom == "USAFE-AFAFRICA":
            return "United States Forces in Europe - Air Forces Africa (USAFE-AFARICA)"
        elif majcom == "AFCENT":
            return "Air Forces Central Command (AFCENT)"
        else:# should not get here
            return "an unknown MAJCOM"


altus = Base("Altus, Oklahoma. United States.", "AETC", "Altus Air Force Base", ["altus"])
arnold = Base("Tullahoma, Tennessee. United States.", "AFMC", "Arnold Air Force Base", ["arnold"])
barksdale = Base("Bossier City, Louisiana. United States.", "AFGSC", "Barksdale Air Force Base", ["barksdale"])
beale = Base("Marysville, California. United States.", "ACC", "Beale Air Force Base", ["beale"])
buckley = Base("Aurora, Colorado. United States.", "AFSPC", "Buckley Air Force Base", ["buckley"])
cannon = Base("Clovis, New Mexico. United States.", "AFSOC", "Cannon Air Force Base", ["cannon"])
cavalier = Base("Mountain, North Dakota. United States.", "AFSPC", "Cavalier Air Force Station", ["cavalier"])
columbus = Base("Columbus, Mississippi. United States.", "AETC", "Columbus Air Force Base", ["columbus"])
creech = Base("Indian Springs, Nevada. United States.", "ACC", "Creech Air Force Base", ["creech"])
davismonthan = Base("Tucson, Arizona. United States.", "ACC",
                    "Davis-Monthan Air Force Base", ["davis", "monthan", "davis-monthan"])
dover = Base("Dover, Delaware. United States.", "AMC", "Dover Air Force Base", ["dover"])
dyess = Base("Abilene, Texas. United States.", "AFGSC", "Dyess Air Force Base", ["dyess"])
edwards = Base("Edwards, California. United States.", "AFMC", "Edwards Air Force Base", ["edwards"])
eglin = Base("Valparaiso, Florida. United States.", "AFMC", "Eglin Air Force Base", ["eglin"])
elisworth = Base("Box Elder, South Dakota. United States.", "AFGSC", "Elisworth Air Force Base", ["elisworth"])
warren = Base("Cheyenne, Wyoming. United States.", "AFGSC",
              "Francis E. Warren Air Force Base", ["francis", "warren", "francis-warren"])
fairchild = Base("Airway Heights, Washington. United States.", "AMC", "Fairchild Air Force Base", ["fairchild"])
jackson = Base("Columbia, South Carolina. United States.", None, "Fort Jackson", ["jackson"])
meade = Base("Odenton, Maryland. United States.", None, "Fort George G. Meade", ["meade"])
goodfellow = Base("San Angelo, Texas. United States.", "AETC", "Goodfellow Air Force Base", ["goodfellow"])
grandforks = Base("Grand Forks, North Dakota. United States.", "AMC", "Grand Forks Air Force Base", ["grandforks",
                                                                                                     "forks"])
hanscom = Base("Lincoln, Massachusetts. United States.", "AFMC", "Hanscom Air Force Base", ["hanscom"])
hill = Base("Ogden, Utah. United States.", "AFMC", "Hill Air Force Base", ["hill"])
holloman = Base("Alamogordo, New Mexico. United States.", "ACC", "Holloman Air Force Base", ["holloman"])
hurlburt = Base("Mary Esther, Florida. United States.", "AFSOC", "Hurlburt Field", ["hurlburt"])
keesler = Base("Biloxi, Mississippi. United States.", "AETC", "Keesler Air Force Base", ["keesler"])
kirtland = Base("Albuquerque, New Mexico. United States.", "AFMC", "Kirtland Air Force Base", ["kirtland"])
laughlin = Base("Del Rio, Texas. United States.", "AETC", "Laughlin Air Force Base", ["laughlin"])
littlerock = Base("Jacksonville, Arkansas. United States.", "AMC",
                  "Little Rock Air Force Base", ["littlerock", "little rock"])
losangeles = Base("El Segundo, California. United States.", "AFSPC", "Los Angeles Air Force Base", ["losangeles",
                                                                                                    "angeles"])
luke = Base("Glendale, Arizona. United States.", "AETC", "Luke Air Force Base", ["luke"])
macdill = Base("Tampa, Florida. United States.", "AMC", "MacDill Air Force Base", ["macdill"])
malmstrom = Base("Great Falls, Montana. United States.", "AFGSC", "Malmstrom Air Force Base", ["malmstrom"])
maxwell = Base("Montgomery, Alabama. United States.", "AETC", "Maxwell Air Force Base", ["maxwell"])
mcconnell = Base("Wichita, Kansas. United States.", "AMC", "McConnell Air Force Base", ["mcconnell"])
minot = Base("Minot, North Dakota. United States.", "AFGSC", "Minot Air Force Base", ["minot", "whynotminot"])
moody = Base("Valdosta, Georgia. United States.", "ACC", "Moody Air Force Base", ["moody"])
mountainhome = Base("Mountain Home, Idaho. United States.", "ACC",
                    "Mountain Home Air Force Base", ["mountainhome", "mountain"])
nellis = Base("Las Vegas, Nevada. United States.", "ACC", "Nellis Air Force Base", ["nellis"])
offutt = Base("Bellevue, Nebraska. United States.", "ACC", "Offutt Air Force Base", ["offutt"])
patrick = Base("Palm Bay, Florida. United States.", "AFSPC", "Patrick Air Force Base", ["patrick"])
peterson = Base("Colorado Springs, Colorado. United States.", "AFSPC", "Peterson Air Force Base", ["peterson"])
pope = Base("Fayetteville, North Carolina. United States.", "AMC", "Pope Field", ["pope"])
robins = Base("Warner Robins, Georgia. United States.", "AFMC", "Robins Air Force Base", ["robins"])
schriever = Base("Colorado Springs, Colorado. United States.", "AFSPC", "Schriever Air Force Base", ["schriever"])
scott = Base("Belleville, Illinois. United States.", "AMC", "Scott Air Force Base", ["scott"])
seymourjohnson = Base("Goldsboro, North Carolina. United States.", "ACC",
                      "Seymour Johnson Air Force Base", ["seymour", "seymour-johnson"])
shaw = Base("Sumter, South Carolina. United States.", "ACC", "Shaw Air Force Base", ["shaw"])
sheppard = Base("Wichita Falls, Texas. United States.", "AETC", "Sheppard Air Force Base", ["sheppard"])
tinker = Base("Oklahoma City, Oklahoma. United States.", "AFMC", "Tinker Air Force Base", ["tinker"])
travis = Base("Fairfield, California. United States.", "AMC", "Travis Air Force Base", ["travis"])
tyndall = Base("Panama City, Florida. United States.", "AETC", "Tyndall Air Force Base", ["tyndall"])
usafacademy = Base("Colorado Springs, Colorado. United States.", None,
                   "United States Air Force Academy", ["usafa", "academy"])
vance = Base("Enid, Oklahoma. United States.", "AETC", "Vance Air Force Base", ["vance"])
vandenberg = Base("Lompoc, California. United States.", "AFSPC", "Vandenberg Air Force Base", ["vandenberg"])
whiteman = Base("Knob Noster, Missouri. United States.", "AFGSC", "Whiteman Air Force Base", ["whiteman"])
wrightpatterson = Base("Dayton, Ohio. United States.", "AFMC",
                       "Wright-Patterson Air Force Base", ["patterson", "patt", "wright-patterson"])


# DOD Joint Bases
bolling = Base("Washington, DC. United States.", None,
               "JB Anacostia-Bolling", ["bolling", "anacostia", "anacostia-bolling", "jbab"])
andrews = Base("Camp Springs, Maryland. United States.", None, "JB Andrews", ["andrews"])
charleston = Base("Charleston, South Carolina. United States.", "AMC", "JB Charleston", ["charleston"])
elmendorf = Base("Anchorage, Alaska. United States.", "PACAF",
                 "JB Elmendorf-Richardson", ["elmendorf", "elmendorf-richardson", "jber"])
langley = Base("Hampton, Virginia. United States.", "ACC", "JB Langley-Eustis", ["langley", "eustis", "langley-eustis"])
mcchord = Base("Tacoma, Washington. United States.", "AMC",
               "JB Lewis-McChord", ["mcchord", "lewis-mcchord"])
mcguire = Base("Trenton, New Jersey. United States.", None,
                "JB McGuire-Dix-Lakehurst", ["mcguire", "mcguire-dix-lakehurst"])
hickam = Base("Honolulu, Hawaii. United States.", "PACAF", "JB Pearl Harbor-Hickam", ["hickam"])
lackland = Base("San Antonio, Texas. United States.", "AETC", "JB San Antonio", ["lackland", "jbsa", "randolph"])
andersen = Base("Guam.", None, "Joint Region Marianas (Andersen AFB)", ["andersen", "marianas"])




# Foreign Countries

# Europe / Africa
thule = Base("Thule, Greenland.", "AFSPC", "Thule Air Base", ["thule"])
ankara = Base("Turkey.", "USAFE-AFAFRICA", "Ankara Support Facility", ["ankara"])
aviano = Base("Italy.", "USAFE-AFAFRICA", "Aviano Air Base", ["aviano"])
buchel = Base("Germany.", "USAFE-AFAFRICA", "Büchel Air Base", ["buchel", "büchel"])
chievres = Base("Belgium.", "USAFE-AFAFRICA", "Chièvres Air Base", ["chievres", "chièvres"])
ghedi = Base("Italy.", "USAFE-AFAFRICA", "Ghedi Air Base", ["ghedi"])
incirlik = Base("Turkey.", "USAFE-AFAFRICA", "Incirlik Air Base", ["incirlik"])
izmir = Base("Turkey.", "USAFE-AFAFRICA", "Izmir Air Station", ["izmir"])
kleinebrogel = Base("Belgium.", "USAFE-AFAFRICA", "Kleine Brogel Air Base", ["kleine", "brogel"])
lajes = Base("Lajes Acores, Portugal.", "USAFE-AFAFRICA", "Lajes Field", ["lajes"])
moron = Base("Spain.", "USAFE-AFAFRICA", "Morón Air Base", ["morón", "moron"])
geilenkirchen = Base("Germany.", "USAFE-AFAFRICA", "NATO Air Base Geilenkirchen", ["geilenkirchen"])
papa = Base("Hungary.", "USAFE-AFAFRICA", "Pápa Air Base", ["pápa", "papa"])
alconbury = Base("Cambridgeshire, United Kingdom.", "USAFE-AFAFRICA", "RAF Alconbury", ["alconbury"])
croughton = Base("Northamptonshire, United Kingdom.", "USAFE-AFAFRICA", "RAF Croughton", ["croughton"])
fairford = Base("Gloucestershire, United Kingdom.", "USAFE-AFAFRICA", "RAF Fairford", ["fairford"])
feltwell = Base("Norfolk, United Kingdom.", "USAFE-AFAFRICA", "RAF Feltwell", ["feltwell"])
flyingdales = Base("North Yorkshire, United Kingdom.", "USAFE-AFAFRICA", "RAF Flyingdales", ["flyingdales"])
lakenheath = Base("Suffolk, United Kingdom.", "USAFE-AFAFRICA", "RAF Lakenheath", ["lakenheath"])
menwith = Base("North Yorkshire, United Kingdom.", "USAFE-AFAFRICA", "RAF Menwith Hill", ["menwith"])
mildenhall = Base("Suffolk, United Kingdom.", "USAFE-AFAFRICA", "RAF Mildenhall", ["mildenhall"])
molesworth = Base("Cambridgeshire, United Kingdom.", "USAFE-AFAFRICA", "RAF Molesworth", ["molesworth"])
welford = Base("Berkshire, United Kingdom.", "USAFE-AFAFRICA", "RAF Welford", ["welford"])
ramstein = Base("Kaiserslautern, Germany.", "USAFE-AFAFRICA", "Ramstein Air Base", ["ramstein"])
spangdahlem = Base("Germany.", "USAFE-AFAFRICA", "Spangdahlem Air Base", ["spangdahlem"])
stavanger = Base("Norway.", "USAFE-AFAFRICA", "Stavanger Air Station", ["stavanger"])
volkel = Base("Netherlands.", "USAFE-AFAFRICA", "Volkel Air Base", ["volkel"])


# Pacific
eielson = Base("Fairbanks, Alaska. United States.", "PACAF", "Eielson Air Force Base", ["eielson"])
kadena = Base("Okinawa, Japan.", "PACAF", "Kadena Air Base", ["kadena"])
kunsan = Base("South Korea.", "PACAF", "Kunsan Air Base", ["kunsan"])
misawa = Base("Japan", "PACAF", "Misawa Air Base", ["misawa"])
osan = Base("South Korea.", "PACAF", "Osan Air Base", ["osan"])
yokota = Base("Tokyo, Japan.", "PACAF", "Yokota Air Base", ["yokota"])


# AFCENT
aldhafra = Base("United Arab Emirates.", "AFCENT", "Al Dhafra Air Base", ["dhafra", "adab"])
aludeid = Base("Doha, Qatar.", "AFCENT", "Al Udeid Air Base", ["udeid", "deid", "auab"])
alialsalem = Base("Kuwait.", "AFCENT", "Ali Al Salem Air Base", ["alsalem", "salem"])
bagram = Base("Bagram, Afghanistan.", "AFCENT", "Bagram Airfield", ["bagram"])
kabul = Base("Afghanistan.", "AFCENT", "Kabul International Airport", ["kabul"])
kandahar = Base("Afghanistan.", "AFCENT", "Kandahar Airfield", ["kandahar"])
sheikisa = Base("Bahrain", "AFCENT", "Sheik Isa Air Base", ["sheik", "isa"])
shindand = Base("Afghanistan.", "AFCENT", "Shindand Air Base", ["shindand"])
thumrait = Base("Thumrait, Oman.", "AFCENT", "RAFO Thumrait", ["thumrait"])

# Army

zama = Base("Sagamihara, Japan.", None, "Camp Zama", ["zama"])

# Have abstained from adding ANG bases due to a lack of mentions and to save time.

all_bases = [altus, arnold, barksdale, beale, buckley, cannon, cavalier, columbus, creech, davismonthan,
             dover, dyess, edwards, eglin, elisworth, warren, fairchild, jackson, meade, goodfellow, grandforks,
             hanscom, hill, holloman, hurlburt, keesler, kirtland, laughlin, littlerock, losangeles, luke,
             macdill, malmstrom, maxwell, mcconnell, minot, moody, mountainhome, nellis, offutt, patrick,
             peterson, pope, robins, schriever, scott, seymourjohnson, shaw, sheppard, tinker, travis, tyndall,
             usafacademy, vance, vandenberg, whiteman, wrightpatterson, bolling, andrews, charleston, elmendorf,
             langley, mcchord, mcguire, hickam, lackland, andersen, thule, ankara, aviano, buchel, chievres,
             ghedi, incirlik, izmir, kleinebrogel, lajes, moron, geilenkirchen, papa, alconbury, croughton, fairford,
             feltwell, flyingdales, lakenheath, menwith, mildenhall, molesworth, welford, ramstein, spangdahlem,
             stavanger, volkel, eielson, kadena, kunsan, misawa, osan, yokota, aldhafra, aludeid, alialsalem, bagram,
             kabul, kandahar, sheikisa, shindand, shindand, thumrait, zama]


def maketables():
    print("Creating tables...")
    db.create_logtable()
    for base in all_bases:
        db.create_table(base.names[0])
