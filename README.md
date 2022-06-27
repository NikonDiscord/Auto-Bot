# Auto-Moderation bot for admins
## Overview
This bot helps you return your messases from webhooks and quick ban members.\
[Bot in action (video)]("https://youtu.be/GTB7FlR2ku8")
#### Screenshots
![automod_ban]("/images/1.png", "automod_ban response")\
![automod_ban]("/images/2.png", "automod_ban response in dms")\
![echo_bot]("/images/3.png", "regular message")\
![echo_bot]("/images/4.png", "message with reply to another message")\
![echo_bot]("/images/5.png", "message with attachments")\
![echo_bot]("/images/3.png", "message with reply to another message and attachments")
## Installation
#### Your own VPS/hosting in linux
1. Install **git** to your VPS/hosting if it not installed: \
    Ubuntu: `sudo apt-get install git -y`\
    Alpine: `sudo apk add git`
2. Clone this repo to your system: `git clone https://github.com/hiprotect/automod`
3. cd into it: `cd automod`
4. Create bot application at [Discord Developer Portal](https://discord.com/developers/applications) and insert bot token to `token.txt` file.
5. Launch bot by executing this command: `screen ./run.sh` (if you're connected to your system via ssh, else `./run.sh`)
6. Copy the invitation link that was displayed in the console, follow it and add the bot to your server.
7. Copy server ID, where you invited your bot, open `cfg.json` and paste this id to value of key `guild_id`
8. Kill bot process and repeat only 4 step.
9. Enjoy!

#### Replit
We do not recommend to host this bot on Replit, because all bots on the Replit are restarted every day, which is not very good for its work and bot code not optimized for replit's public code view.

We will soon resolve issues with Replit hosting and publish information here.

#### Heroku
We don't recommend hosting this bot on Heroku, as the process of deploying to hosting has become a bit more complicated.
Soon we will solve problems with Heroku and publish instructions for installing the bot here.
## Credits
This bot was created by the HiProtect team for educational purposes.
Developer - `самсунг ассистент#5555`\
Telegram - https://t.me/t3rminalpro \
HiProtect - https://t.me/hiprotect 

2022 (c) All rights reserved.