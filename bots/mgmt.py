''' Bot only as an API '''

import os, json, datetime, base64

import discord
from discord.ext import commands
import asyncio

from .helper import STUD_FILE, CONFIG_FILE, LOG_FILE

# TODO Shift to pymongo
with open(CONFIG_FILE) as f: CONFIG = json.load(f)
with open(STUD_FILE) as f: DATA = json.load(f)

''' Constants '''
PREFIX = ';'
SERVER_NAME = CONFIG['guild']
WELCOME_CHANNEL = None
PERSONAL = None
# NO_PERMS = discord.Permissions.none()
# ALL_PERMS = discord.Permissions.all()

OTPs = []

bot = commands.Bot(command_prefix=PREFIX)


''' Events '''

@bot.event
async def on_ready():
  global SERVER_NAME, WELCOME_CHANNEL
  
  activity = discord.Activity(
    type = discord.ActivityType.watching,
    name = 'your every move'
  ); await bot.change_presence(activity=activity)
  pm = None
  for guild in bot.guilds:
    if guild.name == SERVER_NAME:
      only_bot = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
      }
      for channel in guild.channels:
        if channel.name == 'welcome': WELCOME_CHANNEL = channel.id
        if channel.name == 'bot-chan': pm = channel
      if not pm: pm = await guild.create_text_channel('bot-chan',overwrites=only_bot)
      if not pm.topic: pm.topic = 'Channel for BU_MGMT to manage the server. Use the webapp to manipulate bot or type ;help for list of commands'
      await pm.send('The time of bots is now!')
  PERSONAL = pm
  print('Beep boop, boop beep!')

@bot.event
async def on_member_join(mem):
  global DATA
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
  DATA[index] = stud
  with open(STUD_FILE,'w') as f: json.dump(DATA,f)
  if WELCOME_CHANNEL: await dm.send('Head on over to <#{}> to get started!'.format(WELCOME_CHANNEL))

@bot.event
async def on_message(msg):
  if msg.author != bot.user: return
  global LOG_FILE
  log = '[' + str(datetime.datetime.now()) + '] ' + msg.clean_content 
  with open(LOG_FILE,'a') as f: f.write(log)
  await bot.process_commands(msg)

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

def get_member(email):
  if not email: return None,None
  try: email = email[:email.index('@')].lower()
  except ValueError: email = email.lower()
  index = 0
  for stud in DATA:
    if stud.get('netID') == email: return stud,index
    index+=1
  return None,None

def generate_otp(netID):
  global OTPs
  seed = netID + str(datetime.datetime.now())
  b64 = base64.b64encode(seed.encode())
  otp = hash(b64)[-6:]
  while otp in OTPs: otp = hash(b64)[-6:]
  OTPs.append(otp)
  return otp

async def run_command(command):
  global PERSONAL
  if not os.environ.get('BU_MGMT'): exit('token not found')
  bot.run(os.environ['BU_MGMT'])
  if command not in bot.commands: return False
  await PERSONAL.send(';'+command)
  # await bot.logout()
  return True

if __name__ == '__main__':
  if not os.environ.get('BU_MGMT'): exit('token not found')
  bot.run(os.environ['BU_MGMT'])