import os

import discord
from discord.ext import commands


''' Events '''

@bot.event
async def on_ready():
  await bot.change_presence(game=discord.Game(name='Reply with `>reply`'))
  print("Good morning :)")

@bot.event
async def on_message(msg):
  print('messaged')
  print(msg)
  await bot.process_commands(msg)


''' Commands '''


''' Helpers '''


''' Run '''
bot = commands.Bot(command_prefix='>')
bot.run(os.environ['REPLY_BETA'])

