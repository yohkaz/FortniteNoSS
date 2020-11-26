# Fortnite No Stream Snipers (FortniteNoSS)
Fortnite No Stream Snipers (FortniteNoSS) is a tool to track potential stream snipers players.
The goal is to help streamers to determine if a player is stream sniping and if so, get Epic to ban this player more easily.
<br />

## Download
I've not released the tool yet, but that should come soon!
<br />

## General Questions

### How can this tool be useful ?
At the moment, the only feature that I've implemented is tracking players that the user manually entered. You will be able to see the number of times the tracked players appear in your matches, and also see the corresponding replay files. Stream sniping being ban-able by Epic, hopefully this tool will help you to find stream snipers ruining your stream and get them banned.
I intend to implement other features in order to find automatically the potential stream snipers players using all the data a replay file contains.

### An Authentication is needed, why ?
Replays contain only the Account ID of players in the match (Usernames of players being encrypted). In order to be able to convert between a Account ID and an Username, we need to send requests to the Epic Servers.\
**If you prefer not to use your main Epic account, you can create and use a new one.**

### How do you get the matches data ?
Using the [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) parser, FortniteNoSS analyzes your replays and collect data about your matches.\
**You need to have "Record Replays" set to ON in your Fortnite settings and specify the replay directory in the FortniteNoSS Settings!**


## Screenshot

<p align="center">
<img src="screenshots/screenshot.png" width="400px">
</p>