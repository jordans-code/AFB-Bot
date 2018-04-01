# AFB-Bot  - A Reddit Bot

**Features:**

* When summoned for information the bot will currently provide the full base name, the MAJCOM, the city/state/country, links to recent discussions on /r/ratemyafb, a sneak peak of the top comment from one of those discussions, current weather information, and the various base ratings.

* Ability to easily rate bases / change your previous rating of a base in up to four categories: "rate", "arearate", "offbaserate", and "onbaserate". 

* Ability to summon the bot for overall statistics. The bot will provide the highest and lowest rated bases along with the current coldest and warmest temperature bases. 

* Maintains a dynamic wiki for all of the bases which includes base discussions, top comments, the base ranking against others, and more.

**Usage:**

- To summon the bot for base information, either in a comment or a submission include the bot's name (**afbbot**) and a base name, ex: **Langley**. The base name triggers are keywords and nicknames. If you have any suggestions for additional bases or nicknames please let me know.
> **AFBbot**, tell me about **Langley**!

- To rate a base, either in a comment or a submission include the bot's name (**afbbot**), one or more of the following words: **rate**/**arearate**/**onbaserate**/**offbaserate**, a **number** (can be anything but will be rounded between 1-10) after each rating word, and the **base name**. The only thing that matters is that the rating number comes after the rating word.

- **Rate** is for a general rating of the base. 

- **AreaRate** is for a rating of the local area around the base.

- **OnBaseRate** is for a rating of the on base housing (dorms/actual housing).

- **OffBaseRate** is for a rating of the off base housing.

>I was at **langley** for 2 years and the housing is great! Overall I **rate** it an **8**, and I **arearate** it **9.5** **AFBbot**.

- To summon the bot for overall statistics, either in a comment or a submission include the bot's name (**afbbot**) and "**stats**".

>**AFBbot**, lets see those **stats**!

**Planned Features:**

- Add the ability to request a blacklist addition. Currently I have to manually add usernames/submission id's/comment id's to the blacklist to not appear on sneak peaks/get replies from the bot. I would like to give select users the ability to simply PM the bot with the comment/thread/user id and the word "blacklist".

- Add additional bases as they are suggested. I did not include many National Guard / Reserve bases due to a lack of mentions, however if you think a base should be added please let me know and it can be easily done. Undisclosed locations will obviously not be added.

- Add a leaderboard for the base rankings.

- Potentially add other branch bases (if requested).

- Open to any suggestions.

**Notes:**

- For base information the bot will only handle one base per comment, if multiple bases are mentioned it will take the first it sees in it's list. This is to prevent the bot from giving huge wall of text replies. 

- If a user has already rated a base it will change their previous rating, ratings are stored in a SQLite3 DB.

- The bot looks at both submissions and comments for all features.

- The bot can take negative numbers, decimals, 0, but will always round between 1-10. 

- The bot does not care about fractions, ex: if you say "I rate langley 5/5" it will rate it 10 (55 rounded down).  It just looks for the first number after the word rate along with spaces.

- The bot currently runs on /r/AFBbot (feel free to test things here), /r/AirForce, and /r/RateMyAFB

>The bot will ignore single lines of quoted text and attempt to function as normal with the rest of the comment/thread.
>However, if there are multiple lines of quoted text such as this the bot will NOT reply.

- The bot maintains a wiki on /r/RateMyAFB for all bases. The bot loops through each base page to check for an update roughly every 15 minutes. Sometimes the bot will cycle top comments when the scores are similar, this is due to reddit's anti upvote bot fuzzing which randomly changes the scores.

Huge thanks to /u/Rate_My_AF_Base for letting me trial the bot.

Lastly if you wish to use any of the code you are absolutely welcome to it.

[/r/AFBbot](https://www.reddit.com/r/AFBbot/)
