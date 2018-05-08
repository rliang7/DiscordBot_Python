
## https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import random
import asyncio
import requests
import discord
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = 'abcd'  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)

class MathOps():
    @client.command(category="stuff")
    async def square(number):
        squared_val = int(number) * int(number)
        await client.say(str(number) + "squared is" + str(squared_val))

#@client.command()
#async def square(number):
#    squared_value = int(number) * int(number)
#    await client.say(str(number) + " squared is " + str(squared_value))


#@client.event
#async def on_ready():
#    await client.change_presence(game=Game(name="with humans"))
#    print("Logged in as " + client.user.name)


#@client.command()
#async def bitcoin():
#    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
#    response = requests.get(url)
#    value = response.json()['bpi']['USD']['rate']
#    await client.say("Bitcoin price is: $" + value)


@client.command( 
    description="Plays the audio from youtube link.",
    brief="Play audio from youtube",
    pass_context=True  )
async def yt(ctx, url):
    print ( "Attempting to play from: "  + url )
    author = ctx.message.author
    voice_channel = author.voice_channel

    if voice_channel is None:
        print( "Unable to join voice channel for user " + str(author) + " as they are not in any channel atm." )
        return await client.say( ctx.message.author.mention + " has not joined any voice channel to listen to the audio.")
    
    #disconnect if already connected to channel
    for x in client.voice_clients:
        if x.server == ctx.message.server:
            await x.disconnect()

    await client.say( "Currently playing from: {0}".format(url))
    vc = await client.join_voice_channel(voice_channel)
    await client.change_presence(game=Game(name="Music from Youtube"))
    player = await vc.create_ytdl_player(url)
    player.start()

@client.command(
    description="Stops currently running music.",
    brief="Stop playing audio",
    pass_context=True)
async def stop(ctx):
    for x in client.voice_clients:
        if x.server == ctx.message.server:
            await x.disconnect()
            await client.change_presence(game=None)
            return await client.say( "Stopped playing music. ")
    return await client.say( "Unable to fully disconnect from channel ")

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)