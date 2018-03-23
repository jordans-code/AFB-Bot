# AFB-Bot  - A Reddit Bot

**Features:**
* When summoned for information the bot will currently provide the full base name, the MAJCOM, the city/state/country, current weather information, and the overall base rating.

* Ability to easily rate bases / change your previous rating of a base.

* Ability to summon the bot for overall statistics. The bot will provide the highest and lowest rated bases along with the current coldest and warmest temperature bases. 

**Usage:**

- To summon the bot for base information, simply include the bot's name (**afbbot**) and a base name, ex: **Langley**. The base name triggers are keywords and nicknames. If you have any suggestions for additional bases or nicknames please let me know.
> **AFBbot**, tell me about **Langley**!

- To rate a base simply include the bot's name (**afbbot**), the word "**rate**", a **number** (can be anything but will be rounded between 1-10), and the **base name**. The only thing that matters is that the rating number comes after the word "rate".

>I was at **langley** for 2 years and the DFAC sucks! I **rate** it a **3.5** at best.

- To summon the bot for overall statistics, simply include the bot's name (**afbbot**) and "**stats**".

>**AFBbot**, lets see those **stats**!

**Planned Features:**

- Have the bot link the three most recent discussions for the base on /r/ratemyafb when called.

- Add additional bases as they are suggested. I did not include many National Guard / Reserve bases due to a lack of mentions, however if you think a base should be added please let me know and it can be easily done. Undisclosed locations will obviously not be added.

- Potentially add other branch bases (if requested).

- Open to any suggestions.

**Notes:**

- For base information the bot will only reply with a single base's information if multiple are mentioned.

- If a user has already rated a base it will change their previous rating, ratings are stored in a SQLite3 DB.

- The bot looks at both submissions and comments for all features.

- The bot can take negative numbers, decimals, 0, but will always round between 1-10. 

- The bot does not care about fractions, ex: if you say "I rate langley 5/5" it will rate it 10 (55 rounded down).  It just looks for the first number after the word rate along with spaces.

- The bot currently only runs on /r/AFBbot (feel free to test things here) and /r/RateMyAFB

>The bot will ignore single lines of quoted text and attempt to function as normal with the rest of the comment/thread.
>However, if there are multiple lines of quoted text such as this the bot will NOT reply.

Huge thanks to /u/Rate_My_AF_Base for letting me trial the bot.

Lastly if you wish to use any of the code you are absolutely welcome to it.

[/r/AFBbot](https://www.reddit.com/r/AFBbot/)
