import os
import json
import random
import typing
import asyncio
import discord

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

name = 'Worker Bot'
version = '1.0'
prefix = '$'

path = os.path.dirname(os.path.abspath(__file__))
client = commands.Bot(command_prefix=prefix)
slash = SlashCommand(client, sync_commands=True)

logs_channel = 827560186020626443

### ERROR HANDLING

@client.event
async def on_command_error(ctx, error):
    await ctx.message.delete()
    err = await ctx.channel.send(f'{ctx.author.mention} ``{error}``')
    await asyncio.sleep(3)
    await err.delete()

## START MESSAGE

@client.event
async def on_ready():
    await client.get_channel(logs_channel).send('Ready')

### HELP COMMAND

client.remove_command('help')
@slash.slash(name="help", description=f"See a list of {name}\'s commands")
@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour=0x00ff2a,
        title=f'{name} {version}',
    )

    embed.add_field(name='Careers :briefcase:', value='apply\nfindjob\nwork\nquit')
    embed.add_field(name='Crime :knife:', value ='pickpocket\nbankrobbery\nhack\nsteal')
    embed.add_field(name='Stats :notepad_spiral:', value ='stats\nworkout\nlibary')

    await ctx.send(embed=embed)

### CURRENCY COMMANDS  ###

cashier_employers = ['Lidl', 'Aldi', 'Sainsbury\'s', 'Morrison\'s', 'Tesco', 'Premier', 'Londis']
fastfood_employers = ['KFC', 'McDonalds', 'Subway', 'Taco Bell']
stocker_employers = ['Halford\'s', 'B&Q', 'Ikea', 'The Range', 'Home Bargain\'s']

victims = ['a blind woman', 'a blind man', 'a dog', 'a business person', 'a furry', 'Jeff Bezos', 'Patrick Gaming']
sucess_phrases = ['got away with the cash', 'ran away with the cash', 'ran away with the money', 'got away with the money']
fail_phrases = ['was beaten up', 'got sucker punched', 'was knocked out', 'was stabbed', 'was caught']

hacking_status = ['breaching mainframe', 'accessing CPU pins', 'a couple gigabytes of RAM']

async def initialise(author):
    with open(path+r'/resources/user_data.json', 'r') as f:
            user_info = json.load(f)

    if not str(author.id) in user_info:
        user_info[author.id] = {}
        user_info[author.id]['balance'] = 0
        user_info[author.id]['career'] = 'None'
        user_info[author.id]['rank'] = 'None'

        with open(path+r'/resources/user_data.json', 'w') as f:
            json.dump(user_info, f)

async def add_money(author, amount):
        with open(path+r'/resources/user_data.json', 'r') as f:
            user_info = json.load(f)

        user_info[str(author.id)]['balance'] += amount

        with open(path+r'/resources/user_data.json', 'w') as f:
            json.dump(user_info, f)


## FREELANCE COMMANDS  ##

@slash.slash(name="pickpocket", description="Steal from a strangers pocket - 600s cooldown")
@client.command()
@commands.cooldown(1, 600, commands.BucketType.user)
async def pickpocket(ctx: SlashContext):
    await initialise(ctx.author)

    victim = random.choice(victims)
    value = random.randint(5,25)

    sucess = random.randint(1,100)
    if sucess >= 10:
        await add_money(ctx.author, value)
        await ctx.channel.send(f'``You attempted to pickpocket {victim} for £{value} and {random.choice(sucess_phrases)}.``')
    else:
        await add_money(ctx.author, -value)
        await ctx.channel.send(f'``You attempted to pickpocket {victim} and {random.choice(fail_phrases)}. You lost £{value} in the process.``')

@client.command()
@commands.cooldown(1, 1200, commands.BucketType.user)
async def hack(ctx):
    await initialise(ctx.author)

    first = random.choice(hacking_status)
    second = random.choice(hacking_status)

    while first == second:
        first = random.choice(hacking_status)

    embed = discord.Embed(colour=0x00ff55, title=f"{first}...",)
    message = await ctx.channel.send(embed=embed)
    await asyncio.sleep(1)
    embed = discord.Embed(colour=0x00ff55, title=f"{second}...",)
    await message.edit(embed=embed)

## JOB COMMANDS  ## 

@client.command(aliases=['job'])
async def findjob(ctx):
    await initialise(ctx.author)

    job_menu = discord.Embed(title='The Job Centre :money_with_wings:', color=0xd400ff)
    job_menu.add_field(name='Cashier', value=f'Wage - £1 Per Work\nEmployer - {random.choice(cashier_employers)}', inline=True)
    job_menu.add_field(name='Fastfood Cook', value=f'Wage - £3 Per Work\nEmployer - {random.choice(fastfood_employers)}', inline=True)
    job_menu.add_field(name='Shelf Stocker', value=f'Wage - £2 Per Work\nEmployer - {random.choice(stocker_employers)}', inline=True)
    job_menu.set_footer(text=f'Type {prefix}apply followed by the job title to get started.')

    await ctx.send(embed=job_menu)

@slash.slash(name="apply", description="Apply for a specific job", options=[
               create_option(
                 name="title",
                 description="Enter a job title",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="cashier",
                    value="cashier"
                  ),
                  create_choice(
                    name="fastfood cook",
                    value="fastfood cook"
                  ),
                  create_choice(
                    name="shelf stocker",
                    value="shelf stocker"
                  ),
                ]
               )
             ])
@client.command()
async def apply(ctx: SlashContext, *, title: str):
    await initialise(ctx.author)

    with open(path+r'/resources/user_data.json', 'r') as f:
            user_info = json.load(f)

    if title.lower() == 'cashier':
        title = 'Cashier'
    elif title.lower() == 'fastfood cook' or title.lower() == 'cook':
        title = 'Fastfood Cook'
    elif title.lower() == 'stocker' or title.lower() == 'shelf stocker':
        title = 'Shelf Stocker'
    else: # job not found
        title = ''
    
    if title != '':
        user_info[str(ctx.author.id)]['career'] = title
        await ctx.send(embed=discord.Embed(title='Interview Passed :money_with_wings:', description=f'{ctx.author.name} started a job as a {title}. Type {prefix}work to begin.', color=0xd400ff))

        with open(path+r'/resources/user_data.json', 'w') as f:
            json.dump(user_info, f)

async def work_embed(ctx, action, value):
    embed = discord.Embed(
        colour=0xd400ff,
        title=f"{action} :money_with_wings:",
    )

    embed.add_field(name="Pay", value=f"``£{value}``")
    embed.add_field(name="Recognition", value=f"``{random.randint(1,100)}%``")

    await add_money(ctx.author, value)
    await ctx.channel.send(embed=embed)

@slash.slash(name="work", description="Complete a shift - 20s cooldown")
@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def work(ctx: SlashContext):
    await initialise(ctx.author)

    with open(path+r'/resources/user_data.json', 'r') as f:
            user_info = json.load(f)

    if user_info[str(ctx.author.id)]['career'] == 'Fastfood Cook':
        await work_embed(ctx, 'Burger Flipped', 3)
    elif user_info[str(ctx.author.id)]['career'] == 'Cashier':
        await work_embed(ctx, 'Shopping Scanned', 1)
    elif user_info[str(ctx.author.id)]['career'] == 'Shelf Stocker':
        await work_embed(ctx, 'Shelf Stacked', 2)

## STAT COMMANDS  ##

@client.command()
async def stats(message, member: typing.Union[discord.Member, str] = None):
    await initialise(message.author)

    with open(path+r'/resources/user_data.json', 'r') as f:
            user_info = json.load(f)

    if type(member) == discord.Member: # if a user is mentioned
        user = member
        await initialise(user)
    else:
        user = message.author

    bal = int((user_info[str(user.id)]['balance']))
    job = str(user_info[str(user.id)]['career'])
    rank = str(user_info[str(user.id)]['rank'])

    stats = discord.Embed(
        colour=0xd400ff,
        title=f'{user.name}\'s Stats :money_with_wings:',
    )

    stats.add_field(name='Balance', value=f'``£{bal:,d}``')
    stats.add_field(name='Career', value=f'``{job}``')
    stats.add_field(name='Rank', value=f'``{rank}``')

    await message.channel.send(embed=stats)

@slash.slash(name="ket", description="randy command")
@client.command()
async def ket(ctx: SlashContext):
    await ctx.channel.send("Hello")

client.run(os.environ['DISCORD_TOKEN'])
