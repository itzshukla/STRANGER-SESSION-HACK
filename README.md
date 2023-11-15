<h1 align= center>Telegram Session Controller Bot</h1>
<h3 align = center>A telegram bot that control user id effortlessly whether its Pyrogram or Telethon (user string only)</h3>
<p align="center">
<a href="https://python.org"><img src="http://forthebadge.com/images/badges/made-with-python.svg" alt="made-with-python"></a>
<br>
    <img src="https://img.shields.io/github/stars/MaybeBots/SessionBot?style=for-the-badge" alt="Stars">
    <img src="https://img.shields.io/github/forks/MaybeBots/SessionBot?style=for-the-badge" alt="Forks">
    <img src="https://img.shields.io/github/watchers/MaybeBots/SessionBot?style=for-the-badge" alt="Watchers"> 
<br>
    <img src="https://img.shields.io/github/repo-size/MaybeBots/SessionBot?style=for-the-badge" alt="Repository Size">
    <img src="https://img.shields.io/github/contributors/MaybeBots/SessionBot?style=for-the-badge" alt="Contributors">
    <img src="https://img.shields.io/github/issues/MaybeBots/SessionBot?style=for-the-badge" alt="Issues">
</p>

## Config Vars

1. `API_ID` : Telegram API_ID, get it from my.telegram.org/apps
2. `API_HASH` : Telegram API_ID, get it from my.telegram.org/apps
3. `BOT_TOKEN` : A valid bot token, get it from [@BotFather](https://t.me/BotFather)
4. `SUDOERS` : Sudo ids (Example: 1357907531 2468097531 3579864213)
5. `MONGO_URL` : A Mongo Url for storing user ids, get it from cloud.mongodb.com
6. `LOG_GROUP_ID` : Your channel's or group's Telegram id (Example: -1001246808642)
7. `MUST_JOIN` : Telegram channel(username) for force subs
8. `DISABLED`: Menu names which you want to disable, without space (Example: a b j)

## Deployment Methods

### Vps

To deploy on a VPS, follow these steps

1. Update and upgrade your system packages:

```
sudo apt-get update && sudo apt-get upgrade -y
```

2. Clone the repository and navigate to the project directory:

```
git clone https://github.com/MaybeBots/SessionBot && cd SessionBot
```

3. Install the required packages:

```
pip3 install -U -r requirements.txt
```

4. Create .env using example.env

```
cp example.env .env
```

5. Now open the .env file using **vi .env**
6. Edit the vars, by pressing **I** on the keyboard
7. After editing save the file using **ctrl + c** then **:wq**
8. Run the script using Python 3:

```
python3 -m Hack
```

## Support

- [Channel](https://t.me/Maybebots)
- [Group](https://t.me/MaybeBotsSupport)

## Credits

- [Telethon](https://github.com/LonamiWebs/Telethon)
- [Ultroid](https://github.com/TeamUltroid/Ultroid)
