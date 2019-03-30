''' Bot only as an API; to be used by a GUI '''

import os

import discord
from discord.ext import commands

from .helper import FILE_EXT, DATA_DIR

bot = commands.Bot(command_prefix=prefix)


''' Commands '''

@bot.command(pass_context=True)
async def add_courses(ctx, *args):
  pass
  
@bot.command(pass_context=True)
async def add_to_course(ctx, *args):
  pass
  
@bot.command(pass_context=True)
async def add_to_batch(ctx, *args):
  pass

@bot.command(pass_context=True)
async def add_to_year(ctx, *args):
  pass
