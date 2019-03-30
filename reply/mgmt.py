''' Bot only as an API; to be used by a GUI '''

import os, json, datetime

import discord
from discord.ext import commands
import asyncio

from helper import STUD_FILE, SERVER_INFO

prefix = ';'
bot = commands.Bot(command_prefix=prefix)
server,data = {},{}
WELCOME_CHANNEL = None

''' Events '''

@bot.event
async def on_ready():
  act = discord.Activity()
  act.type = discord.ActivityType.watching
  act.name = 'your every move'
  await bot.change_presence(activity=act)
  print(bot.guilds)
  print('Awake')

@bot.event
async def on_member_join(mem):
  global server,data
  with open(SERVER_INFO) as f: server = json.load(f)
  with open(STUD_FILE) as f: data = json.load(f)
  dm = await mem.create_dm() if not mem.dm_channel else mem.dm_channel
  # TODO convert to from_dict()
  em = discord.Embed( 
    title = 'CSE@BU Server',
    description='This is official communication channel of the CSE department at Bennett University. Ask doubts, connect with peers and alumni, and hear about announcements here first!',
    timestamp=datetime.datetime.now(),
    color=0x57C77E
  )
  em.set_author(name='BU.hack()',url='http://buhack.org',icon_url='http://buhack.org/assets/BUhack-logo.png')
  await dm.send(embed=em)
  await dm.send('Welcome!! Please enter your Bennett email')

  def check(m): return m.channel.id == dm.id and m.author == dm.recipient
  stud = None
  retries,endloop = 0, False
  while not endloop: # Email loop
    try: msg = await bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError: await dm.send('You took too long!!')
    else:
      if retries > 5: 
        await mem.kick(reason='Max retries for email reached. Are you sure you\'re in the right server?')
        return
      stud,index = get_member(email=msg.clean_content)
      if not stud:
        await dm.send('Email {0.clean_content} not found. Please try again.'.format(msg))
        retries += 1
        continue
      await dm.send('Welcome {0}! Enter the OTP sent your email'.format(stud['name']))
      endloop = True

  retries,endloop = 0, False
  while not endloop: # OTP loop
    try: msg = await bot.wait_for('message', check=check, timeout=60.0)
    except: asyncio.TimeoutError: await dm.send('m8 I cant w8')
    else:
      if retries > 3: 
        await mem.kick(reason='Max retries for OTP reached. Are you sure you\'re using your email?')
        return
      if msg.clean_content != stud.get('otp'):
        retries += 1
        await dm.send('Incorrect OTP! Please try again!')
        continue
      # Success
      stud['discord_uid'] = mem.id
      roles = []
      if stud.get('enrolled'): roles.append(discord.utils.get(mem.guild.roles, name='student'))
      if stud.get('year'): roles.append(discord.utils.get(mem.guild.roles, name=str(stud['year'])))
      if stud.get('batch'): roles.append(discord.utils.get(mem.guild.roles, name='eb0'+str(stud['batch'])))
      if stud.get('rep'): roles.append(discord.utils.get(mem.guild.roles, name=stud['rep']))
      if roles: await mem.add_roles(*roles)
      await dm.send('Welcome to the server! You have been assigned the following roles: ' + 
        ', '.join(role.name for role in roles))
      endloop = True
  data[index] = stud
  with open(STUD_FILE,'w') as f: json.dump(data,f)
  if WELCOME_CHANNEL: await dm.send('Head on over to <#{}> to get started!'.format(WELCOME_CHANNEL))

@bot.event
async def on_message(msg):
  # if isinstance(msg.channel,discord.DMChannel): pass
  author = msg.author
  print(author)
  print(msg.channel)
  # print(msg.channel.name)

''' Commands '''

@bot.command(pass_context=True)
async def add_channel(ctx, *args):
  pass
  
@bot.command(pass_context=True)
async def add_to_channel(ctx, *args):
  pass

@bot.command(pass_context=True)
async def make_representative(ctx, *args):
  pass

@bot.command(pass_context=True)
async def add_to_server(ctx, *args):
  pass


''' Helper Methods '''
def get_member(email=''):
  if not email: return None,None
  try: email = email[:email.index('@')].lower()
  except ValueError: email = email.lower()
  index = 0
  for stud in data:
    if stud.get('netID') == email: return stud,index
    index+=1
  return None,None

if __name__ == '__main__':
  if not os.environ.get('BU_MGMT'): exit('token not found')

  bot.self_bot = True # Will only listen for commands called by itself
  bot.run(os.environ['BU_MGMT'])