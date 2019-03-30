import discord
import os


client = discord.Client()

@client.event  # event decorator
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    sentdex_guild = client.get_guild(538764109835927575)

    if "!member_count" == message.content.lower():
        await message.channel.send(f"```py\n{sentdex_guild.member_count}```")
    elif "hi there" == str(message.content).lower():
        await message.channel.send("Hola!")
    elif "you are idiot" == str(message.content).lower():
        await message.channel.send("Please fuck off -!-")
    elif "!out" == str(message.content).lower():
        await client.close()
    elif "!report" == message.content.lower():
        online = 0
        idle = 0
        offline = 0

        for m in sentdex_guild.members:
            if str(m.status) == "online":
                online += 1
            elif str(m.status) == "idle":
                idle += 1
            elif str(m.status) == "offline":
                idle += 1
            else:
                online += 1
    await message.channel.send(f"```Online: {online} \nIdle: {idle} \nOffline: {offline}```")
        

client.run(os.environ['LEARNING'])