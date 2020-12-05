# Fortnite No Stream Snipers (FortniteNoSS)
Fortnite No Stream Snipers (FortniteNoSS) is a tool to track potential stream snipers players.
The goal is to help streamers to determine if a player is stream sniping and if so, get Epic to ban this player more easily.

The tool is targeted only to Windows platforms since Fortnite run only on Windows.

<p align="center">
<img src="screenshots/tracker.png" width="300px">
<img src="screenshots/last-match-players.png" width="300px">
<img src="screenshots/last-match-killfeed.png" width="385px">
</p>


## Download
I've not released the tool yet, but that should come soon!


## Manual Installation
If you prefer to install the tool manually, follow the instructions below.

### Prerequisites
 - Python 3.7+ (tested mainly with 3.8, but should work with other versions)
 - .NET 5.0 ([https://dotnet.microsoft.com/download](https://dotnet.microsoft.com/download))

### Install
Open your command line *cmd.exe* and simply run the *build.bat* file from the root directory of the project
```
$ build.bat
```

### Usage
After the install you should be in the *src/* directory.
Run the following command:
```
$ python app.py
```

## Tutorial
Everything is explained in the tool itself.
If you think something is not clear, feel free to contact me.


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


