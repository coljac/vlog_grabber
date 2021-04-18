import discord
import os
import sys


client = discord.Client()
options = {"notify": False}

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name in options['channels']:
        if len(message.attachments) > 0:
            for a in message.attachments:
                if a.filename.endswith(".vlog"):
                    try:
                        await a.save(f"/tmp/{a.filename}")
                        if options['notify']:
                            await message.channel.send(f"Got {a.filename}.")
                    except Exception as e:
                        print(repr(e))


def printhelp():
    print("vlog_grabber_bot [-notify] <channel1[,channel2,...]> </path/to/save>")


def main():
    if "DISCORD_TOKEN" not in os.environ:
        print("Supply token in environment variable DISCORD_TOKEN")
        return

    token = os.getenv('DISCORD_TOKEN')

    if len(sys.argv) < 2:
        printhelp()
        return

    if "-notify" in sys.argv:
        options['notify'] = True
        sys.argv.remove('-notify')

    options['channels'] = sys.argv[1].split(",")
    try:
        options['savedir'] = sys.argv[2]
    except:
        options['savedir'] = "."

    if not os.path.exists(options['savedir']):
        print(f"Error: Save path {options['savedir']} does not exist.")
        return

    client.run(token)

if __name__ == "__main__":
    main()
