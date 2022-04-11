import keys

import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from peony import PeonyClient, events


intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = discord.Client()

TOKEN = keys.token
twtclient = PeonyClient(keys.cl1, keys.cl2, keys.cl3, keys.cl4)

async def track():
    stream = twtclient.stream.statuses.filter.post(track="twitch.tv/5hak_")

    async for tweet in stream:
        if events.tweet(tweet):
            tweet_id = tweet['id']
            username = tweet.user.screen_name

            if username == '5hak_':
                return
            

@client.event
async def on_ready():
    channel = client.get_channel(881654911287312395)
    print("Shakbot is ready!")
    while True:
        await track()
        await channel.send("<@&881658122941378651> HE'S LIVE! @ https://www.twitch.tv/5hak_")

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Shak Fan")
    await member.add_roles(role)


@client.event
async def on_raw_reaction_add(payload):
    if (payload.message_id == 881676625723392020 and payload.emoji.name == "❤️"):
        role = discord.utils.get(payload.member.guild.roles, name="Shak Fan")
        await payload.member.add_roles(role)
    if (payload.message_id == 881676625723392020 and payload.emoji.name == "🔔"):
        role = discord.utils.get(payload.member.guild.roles, name="I wanna be bugged by pings")
        await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    if (payload.message_id == 881676625723392020 and payload.emoji.name == "🔔"):
        guild = await client.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        role = discord.utils.get(member.guild.roles, name="I wanna be bugged by pings")
        await member.remove_roles(role)
    if (payload.message_id == 881676625723392020 and payload.emoji.name == "❤️"):
        guild = await client.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        role = discord.utils.get(member.guild.roles, name="Shak Fan")
        await member.remove_roles(role)

@client.event
async def on_message(message):
    if (message[0:8] == "@Shakbot" and message[9:13].lower() == "bash"):
        return


client.run(TOKEN)