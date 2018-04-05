import database as db


class Base(object):
    def __init__(self, location, manualweather, majcom, displayname, names):
        self.location = location
        self.manualweather = manualweather
        self.majcom = majcom
        self.displayname = displayname
        self.names = names

    def addrating(self, author, rtype, rating, commentid, threadid):
        if db.query_existing(self.names[0], author, rtype):
            return False
        else:
            db.data_entry(self.names[0], author, rtype, rating, commentid, threadid)
            print(f"Added rating {rating} to {self.names[0]} by {author}")
            return True

    def getrating(self, rtype):
        overallrating = db.query_rating(self.names[0], rtype)
        if overallrating < 1:
            return "Unrated"
        else:
            roundedrating = "%.2f" % overallrating
            return roundedrating

    def gettrueoverallrating(self):
        truerating = db.query_overallrating(self.names[0])
        if truerating:
            roundedrating = "%.2f" % truerating
            return roundedrating
        else:
            return "Unrated"

    def changerating(self, author, rtype, rating, commentid, threadid):
        db.change_entry(self.names[0], author, rtype, rating, commentid, threadid)

    def getranking(self, rtype):
        ranking, count = db.query_ranking(self, rtype, all_bases)
        if ranking:
            return ranking, count
        else:
            return "Unranked", count

    def getoverallranking(self):
        ranking, count = db.query_overallranking(self, all_bases)
        if ranking:
            ranking = f"**#{ranking}**"
            return ranking, count
        else:
            return "**Unranked**", count

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
        else:  # should not get here
            return "an unknown MAJCOM"

altus = Base("Altus, Oklahoma. United States.", None, "AETC", "Altus Air Force Base", ["altus"])
arnold = Base("Tullahoma, Tennessee. United States.", None, "AFMC", "Arnold Air Force Base", ["arnold"])
barksdale = Base("Bossier City, Louisiana. United States.", "USLA0052", "AFGSC", "Barksdale Air Force Base", ["barksdale"])
beale = Base("Marysville, California. United States.", None, "ACC", "Beale Air Force Base", ["beale"])
buckley = Base("Aurora, Colorado. United States.", None, "AFSPC", "Buckley Air Force Base", ["buckley"])
cannon = Base("Clovis, New Mexico. United States.", None, "AFSOC", "Cannon Air Force Base", ["cannon"])
cavalier = Base("Mountain, North Dakota. United States.", None, "AFSPC", "Cavalier Air Force Station", ["cavalier"])
columbus = Base("Columbus, Mississippi. United States.", None, "AETC", "Columbus Air Force Base", ["columbus"])
creech = Base("Indian Springs, Nevada. United States.", None, "ACC", "Creech Air Force Base", ["creech"])
davismonthan = Base("Tucson, Arizona. United States.", None, "ACC",
                    "Davis-Monthan Air Force Base", ["davis", "monthan", "davis-monthan", "dm"])
dover = Base("Dover, Delaware. United States.", None, "AMC", "Dover Air Force Base", ["dover"])
dyess = Base("Abilene, Texas. United States.", None, "AFGSC", "Dyess Air Force Base", ["dyess"])
edwards = Base("Edwards, California. United States.", None, "AFMC", "Edwards Air Force Base", ["edwards"])
eglin = Base("Niceville, Florida. United States.", None, "AFMC", "Eglin Air Force Base", ["eglin"])
ellsworth = Base("Box Elder, South Dakota. United States.", None, "AFGSC", "Ellsworth Air Force Base", ["ellsworth"])
warren = Base("Cheyenne, Wyoming. United States.", None, "AFGSC",
              "Francis E. Warren Air Force Base", ["warren", "francis-warren"])
fairchild = Base("Airway Heights, Washington. United States.", None, "AMC", "Fairchild Air Force Base", ["fairchild"])
jackson = Base("Columbia, South Carolina. United States.", None, None, "Fort Jackson (South Carolina)", ["jackson"])
meade = Base("Odenton, Maryland. United States.", None, None, "Fort George G. Meade", ["meade"])
goodfellow = Base("San Angelo, Texas. United States.", None, "AETC", "Goodfellow Air Force Base", ["goodfellow"])
forks = Base("Grand Forks, North Dakota. United States.", None, "AMC", "Grand Forks Air Force Base", ["forks",
                                                                                                     "grandforks"])
hanscom = Base("Lincoln, Massachusetts. United States.", None, "AFMC", "Hanscom Air Force Base", ["hanscom"])
hill = Base("Ogden, Utah. United States.", "USUT0188", "AFMC", "Hill Air Force Base", ["hill"])
holloman = Base("Alamogordo, New Mexico. United States.", None, "ACC", "Holloman Air Force Base", ["holloman"])
hurlburt = Base("Mary Esther, Florida. United States.", None, "AFSOC", "Hurlburt Field", ["hurlburt"])
keesler = Base("Biloxi, Mississippi. United States.", None, "AETC", "Keesler Air Force Base", ["keesler"])
kirtland = Base("Albuquerque, New Mexico. United States.", None, "AFMC", "Kirtland Air Force Base", ["kirtland"])
laughlin = Base("Del Rio, Texas. United States.", None, "AETC", "Laughlin Air Force Base", ["laughlin"])
rock = Base("Jacksonville, Arkansas. United States.", None, "AMC",
                  "Little Rock Air Force Base", ["rock", "littlerock"])
losangeles = Base("El Segundo, California. United States.", None, "AFSPC", "Los Angeles Air Force Base", ["angeles",
                                                                                                    "losangeles"])
luke = Base("Glendale, Arizona. United States.", None, "AETC", "Luke Air Force Base", ["luke"])
macdill = Base("Tampa, Florida. United States.", None, "AMC", "MacDill Air Force Base", ["macdill"])
malmstrom = Base("Great Falls, Montana. United States.", None, "AFGSC", "Malmstrom Air Force Base", ["malmstrom"])
maxwell = Base("Montgomery, Alabama. United States.", None, "AETC", "Maxwell Air Force Base", ["maxwell"])
mcconnell = Base("Wichita, Kansas. United States.", None, "AMC", "McConnell Air Force Base", ["mcconnell"])
minot = Base("Minot, North Dakota. United States.", None, "AFGSC", "Minot Air Force Base", ["minot", "whynotminot"])
moody = Base("Valdosta, Georgia. United States.", None, "ACC", "Moody Air Force Base", ["moody"])
mountain = Base("Mountain Home, Idaho. United States.", None, "ACC",
                    "Mountain Home Air Force Base", ["mountain", "mountainhome"])
nellis = Base("Las Vegas, Nevada. United States.", None, "ACC", "Nellis Air Force Base", ["nellis"])
offutt = Base("Bellevue, Nebraska. United States.", None, "ACC", "Offutt Air Force Base", ["offutt"])
patrick = Base("Palm Bay, Florida. United States.", None, "AFSPC", "Patrick Air Force Base", ["patrick"])
peterson = Base("Colorado Springs, Colorado. United States.", "USCO0078", "AFSPC", "Peterson Air Force Base", ["peterson"])
pope = Base("Fayetteville, North Carolina. United States.", None, "AMC", "Pope Field", ["pope"])
robins = Base("Warner Robins, Georgia. United States.", None, "AFMC", "Robins Air Force Base", ["robins"])
schriever = Base("Colorado Springs, Colorado. United States.", None, "AFSPC", "Schriever Air Force Base", ["schriever"])
scott = Base("Belleville, Illinois. United States.", None, "AMC", "Scott Air Force Base", ["scott"])
seymourjohnson = Base("Goldsboro, North Carolina. United States.", None, "ACC",
                      "Seymour Johnson Air Force Base", ["seymour", "seymour-johnson"])
shaw = Base("Sumter, South Carolina. United States.", None, "ACC", "Shaw Air Force Base", ["shaw"])
sheppard = Base("Wichita Falls, Texas. United States.", None, "AETC", "Sheppard Air Force Base", ["sheppard"])
tinker = Base("Oklahoma City, Oklahoma. United States.", None, "AFMC", "Tinker Air Force Base", ["tinker"])
travis = Base("Fairfield, California. United States.", None, "AMC", "Travis Air Force Base", ["travis"])
tyndall = Base("Panama City, Florida. United States.", None, "AETC", "Tyndall Air Force Base", ["tyndall"])
usafacademy = Base("Colorado Springs, Colorado. United States.", None, None,
                   "United States Air Force Academy", ["usafa", "academy"])
vance = Base("Enid, Oklahoma. United States.", None, "AETC", "Vance Air Force Base", ["vance"])
vandenberg = Base("Lompoc, California. United States.", None, "AFSPC", "Vandenberg Air Force Base", ["vandenberg"])
whiteman = Base("Knob Noster, Missouri. United States.", None, "AFGSC", "Whiteman Air Force Base", ["whiteman"])
wrightpatterson = Base("Dayton, Ohio. United States.", None, "AFMC",
                       "Wright-Patterson Air Force Base", ["patterson", "patt", "wright-patterson"])


# DOD Joint Bases
bolling = Base("Washington, DC. United States.", None, None,
               "JB Anacostia-Bolling", ["bolling", "anacostia", "anacostia-bolling", "jbab"])
andrews = Base("Camp Springs, Maryland. United States.", None, None, "JB Andrews", ["andrews"])
charleston = Base("Charleston, South Carolina. United States.", None, "AMC", "JB Charleston", ["charleston"])
elmendorf = Base("Anchorage, Alaska. United States.", None, "PACAF",
                 "JB Elmendorf-Richardson", ["elmendorf", "elmendorf-richardson", "jber"])
langley = Base("Hampton, Virginia. United States.", None, "ACC", "JB Langley-Eustis", ["langley", "eustis", "langley-eustis"])
mcchord = Base("Tacoma, Washington. United States.", None, "AMC",
               "JB Lewis-McChord", ["mcchord", "lewis-mcchord"])
mcguire = Base("Trenton, New Jersey. United States.", None, None,
                "JB McGuire-Dix-Lakehurst", ["mcguire", "mcguire-dix-lakehurst"])
hickam = Base("Honolulu, Hawaii. United States.", None, "PACAF", "JB Pearl Harbor-Hickam", ["hickam"])
lackland = Base("San Antonio, Texas. United States.", None, "AETC", "JB San Antonio", ["lackland", "jbsa", "randolph"])
andersen = Base("Yigo, Guam.", None, None, "Joint Region Marianas", ["andersen", "marianas"])
cape = Base("Bourne, Massachusetts. United States.", None, "AFSPC", "Joint Base Cape Cod", ["cape", "cod"])



# Foreign Countries

soto = Base("Honduras.", None, None, "Soto Cano Air Base", ["soto"])

# Europe / Africa
thule = Base("Thule, Greenland.", None, "AFSPC", "Thule Air Base", ["thule"])
ankara = Base("Ankara, Turkey.", None, "USAFE-AFAFRICA", "Ankara Support Facility", ["ankara"])
aviano = Base("Pordenone, Italy.", "ITXX0375", "USAFE-AFAFRICA", "Aviano Air Base", ["aviano"])
buchel = Base("Germany.", None, "USAFE-AFAFRICA", "Büchel Air Base", ["buchel", "büchel"])
chievres = Base("Belgium.", None, "USAFE-AFAFRICA", "Chièvres Air Base", ["chievres", "chièvres"])
ghedi = Base("Italy.", None, "USAFE-AFAFRICA", "Ghedi Air Base", ["ghedi"])
incirlik = Base("Adana, Turkey.", None, "USAFE-AFAFRICA", "Incirlik Air Base", ["incirlik"])
izmir = Base("Izmir, Turkey.", None, "USAFE-AFAFRICA", "Izmir Air Station", ["izmir"])
kleinebrogel = Base("Belgium.", None, "USAFE-AFAFRICA", "Kleine Brogel Air Base", ["kleine", "brogel"])
lajes = Base("Lajes Acores, Portugal.", None, "USAFE-AFAFRICA", "Lajes Field", ["lajes"])
moron = Base("Spain.", None, "USAFE-AFAFRICA", "Morón Air Base", ["moron", "morón"])
geilenkirchen = Base("Germany.", None, "USAFE-AFAFRICA", "NATO Air Base Geilenkirchen", ["geilenkirchen"])
papa = Base("Hungary.", None, "USAFE-AFAFRICA", "Pápa Air Base", ["papa", "pápa"])
alconbury = Base("Cambridgeshire, United Kingdom.", None, "USAFE-AFAFRICA", "RAF Alconbury", ["alconbury"])
croughton = Base("Northamptonshire, United Kingdom.", None, "USAFE-AFAFRICA", "RAF Croughton", ["croughton"])
fairford = Base("Gloucestershire, United Kingdom.", None, "USAFE-AFAFRICA", "RAF Fairford", ["fairford"])
feltwell = Base("Norfolk, United Kingdom.", None, "USAFE-AFAFRICA", "RAF Feltwell", ["feltwell"])
lakenheath = Base("Suffolk, United Kingdom.", None, "USAFE-AFAFRICA", "RAF Lakenheath", ["lakenheath"])
menwith = Base("North Yorkshire, United Kingdom.", None, "USAFE-AFAFRICA", "RAF Menwith Hill", ["menwith"])
mildenhall = Base("Suffolk, United Kingdom.", None, "USAFE-AFAFRICA", "RAF Mildenhall", ["mildenhall"])
molesworth = Base("Cambridgeshire, United Kingdom.", None, "USAFE-AFAFRICA", "RAF Molesworth", ["molesworth"])
welford = Base("Berkshire, United Kingdom.", None, "USAFE-AFAFRICA", "RAF Welford", ["welford"])
ramstein = Base("Kaiserslautern, Germany.", "GMXX1141", "USAFE-AFAFRICA", "Ramstein Air Base", ["ramstein"])
spangdahlem = Base("Germany.", None, "USAFE-AFAFRICA", "Spangdahlem Air Base", ["spangdahlem"])
stavanger = Base("Norway.", None, "USAFE-AFAFRICA", "Stavanger Air Station", ["stavanger"])
volkel = Base("Netherlands.", None, "USAFE-AFAFRICA", "Volkel Air Base", ["volkel"])

# Pacific
eielson = Base("Fairbanks, Alaska. United States.", "USAK0084", "PACAF", "Eielson Air Force Base", ["eielson"])
kadena = Base("Okinawa, Japan.", "JAXX0027", "PACAF", "Kadena Air Base", ["kadena"])
kunsan = Base("Kunsan, South Korea.", "KSXX0046", "PACAF", "Kunsan Air Base", ["kunsan"])
misawa = Base("Misawa, Japan.", "JAXX0120", "PACAF", "Misawa Air Base", ["misawa"])
osan = Base("Osan, South Korea.", "KSXX0018", "PACAF", "Osan Air Base", ["osan"])
yokota = Base("Tokyo, Japan.", "JAXX0085", "PACAF", "Yokota Air Base", ["yokota"])


# AFCENT
aldhafra = Base("Abu Dhabi, United Arab Emirates.", "AEXX0001", "AFCENT", "Al Dhafra Air Base", ["dhafra", "adab"])
aludeid = Base("Doha, Qatar.", "QAXX0003", "AFCENT", "Al Udeid Air Base", ["udeid", "deid", "auab"])
alialsalem = Base("Al Jahra, Kuwait.", "KUXX0003", "AFCENT", "Ali Al Salem Air Base", ["salem", "alsalem"])
bagram = Base("Bagram, Afghanistan.", "AFXX0003", "AFCENT", "Bagram Airfield", ["bagram"])
kabul = Base("Kabul, Afghanistan.", "AFXX0003", "AFCENT", "Kabul International Airport", ["kabul"])
kandahar = Base("Kandahar, Afghanistan.", "AFXX0004", "AFCENT", "Kandahar Airfield", ["kandahar", "khandahar"])
sheikisa = Base("Bahrain", "BAXX0096", "AFCENT", "Isa Air Base", ["sheik", "isa"])
shindand = Base("Shindand, Afghanistan.", "AFXX0009", "AFCENT", "Shindand Air Base", ["shindand"])
thumrait = Base("Thumrait, Oman.", "MUXX0011", "AFCENT", "RAFO Thumrait", ["thumrait"])

# Army
presidio = Base("Monterey, California. United States.", None, None, "Presidio of Monterey", ["presidio", "monterey"])
redcloud = Base("Seoul, South Korea.", None, None, "Camp Red Cloud", ["cloud"])
yongsan = Base("Seoul, South Korea.", None, None, "Yongsan Garrison", ["yongsan"])
zama = Base("Sagamihara, Japan.", None, None, "Camp Zama", ["zama"])

# Have abstained from adding ANG bases due to a lack of mentions and to save time.

all_bases = [altus, arnold, barksdale, beale, buckley, cape, cannon, cavalier, columbus, creech, davismonthan,
             dover, dyess, edwards, eglin, ellsworth, warren, fairchild, jackson, meade, goodfellow, forks,
             hanscom, hill, holloman, hurlburt, keesler, kirtland, laughlin, rock, losangeles, luke,
             macdill, malmstrom, maxwell, mcconnell, minot, moody, mountain, nellis, offutt, patrick,
             peterson, pope, robins, schriever, scott, seymourjohnson, shaw, sheppard, tinker, travis, tyndall,
             usafacademy, vance, vandenberg, whiteman, wrightpatterson, bolling, andrews, charleston, elmendorf,
             langley, mcchord, mcguire, hickam, lackland, andersen, soto, thule, ankara, aviano, buchel, chievres,
             ghedi, incirlik, izmir, kleinebrogel, lajes, moron, geilenkirchen, papa, alconbury, croughton, fairford,
             feltwell, lakenheath, menwith, mildenhall, molesworth, welford, ramstein, spangdahlem,
             stavanger, volkel, eielson, kadena, kunsan, misawa, osan, yokota, aldhafra, aludeid, alialsalem, bagram,
             kabul, kandahar, sheikisa, shindand, shindand, thumrait, presidio, redcloud, yongsan, zama]


def maketables():
    print("Creating tables...")
    db.create_logtable()
    db.create_blacklist()
    for base in all_bases:
        db.create_table(base.names[0])
