# AFB-Bot  - A Reddit Bot

**Features:**
* When summoned for information the bot will currently provide the full base name, the MAJCOM, the city/state/country, current weather information, and the overall base rating.

* Ability to easily rate bases / change your previous rating of a base.

**Usage:**

- To summon the bot for general information, simply include the name "afbbot" (not case sensitive) and a base name, ex: Langley. The base name triggers are keywords and nicknames, you can review the full list on the source provided below. If you have any suggestions for additional bases or nicknames please let me know.
> **AFBbot**! Tell me about **Langley**!

- To rate a base you do not need to manually call the bot, simply include the word "rate" along with a number (can be anything but will be rounded between 1-10) and the base name. The only thing that matters currently is that the rating comes after the word "rate". Ex: I rate Langley a 9.5.
>I was at **langley** for 2 years and the DFAC sucks! I **rate** it a **3.5** at best.

**Planned Features:**

- Have the bot link the three most recent discussions for the base when called.

- Give the ability to call the bot for a stats page, statistics displayed could be things like top three rated bases, top three lowest rated bases, ect.

- Add additional bases as they are suggested. I did not include many National Guard / Reserve bases due to a lack of mentions, however if you think a base should be added please let me know and it can be easily done. Undisclosed locations will obviously not be added.

- Open to any suggestions. If there are any python gods out there (/u/HadManySons) who have the time to look over my git and see something that I could do better your feedback is always appreciated.

**Notes:**

- Ratings are stored in a SQLite3 DB, if a user has already rated a base it will change their previous rating.

- The bot looks at both submissions and comments for all features.

- The bot can take negative numbers, decimals, 0, but will always round it between 1-10. 

- The bot does not care about fractions, ex: if you say "I rate langley 5/5" it will rate it 5.0.  It just looks for the first number after the word rate.

- The bot currently only runs on /r/AFBbot (feel free to test things here) and /r/RateMyAFB , after I determine it is stable and am finished implementing some more planned features I will ask if it is something the mods over at /r/AirForce would be interested in adding or if any other subs are interested in it.

>The bot will ignore single lines of quoted text and attempt to function as normal with the rest of the comment/thread.
>However, if there are multiple lines of quoted text such as this the bot will NOT reply.

If you find a bug or want to give feedback feel free to leave it here or at the below links. Thanks for your time.

Huge thanks to /u/Rate_My_AF_Base for letting me trial the bot.

Lastly if you wish to use any of the code you are absolutely welcome to it.

[/r/AFBbot](https://www.reddit.com/r/AFBbot/)
