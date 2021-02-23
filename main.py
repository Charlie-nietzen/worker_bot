import os
import json
import random
import typing
import discord

from discord.ext import commands

name = 'Worker Bot'
version = '1.0'
prefix = '$'

path = os.path.dirname(os.path.abspath(__file__))
settings = json.load(open(os.path.join(path, 'config.json')))
token = settings['token']

client = commands.Bot(command_prefix=prefix)

### CURRENCY COMMANDS START ###

cashier_employers = ['Lidl', 'Aldi', 'Sainsbury\'s', 'Morrison\'s', 'Tesco', 'Premier', 'Londis']
fastfood_employers = ['KFC', 'McDonalds', 'Subway', 'Taco Bell']
stocker_employers = ['Halford\'s', 'B&Q', 'Ikea', 'The Range']

## JOB COMMANDS START ## 

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

@client.command()
async def findjob(ctx):
    await initialise(ctx.author)

    job_menu = discord.Embed(title='The Job Centre :money_with_wings:', color=0xd400ff)
    job_menu.add_field(name='Cashier', value=f'Wage - £1.50 Per Work\nEmployer - {random.choice(cashier_employers)}', inline=True)
    job_menu.add_field(name='Fastfood Cook', value=f'Wage - £3 Per Work\nEmployer - {random.choice(fastfood_employers)}', inline=True)
    job_menu.add_field(name='Shelf Stocker', value=f'Wage - £2 Per Work\nEmployer - {random.choice(stocker_employers)}', inline=True)
    job_menu.set_footer(text=f'Type {prefix}apply followed by the job title to get started.')

    await ctx.send(embed=job_menu)

@client.command()
async def apply(ctx, *, choice):
    await initialise(ctx.author)

    with open(path+r'/resources/user_data.json', 'r') as f:
            user_info = json.load(f)

    if choice.lower() == 'cashier':
        title = 'Cashier'
    elif choice.lower() == 'fastfood cook' or choice.lower() == 'cook':
        title = 'Fastfood Cook'
    elif choice.lower() == 'stocker' or choice.lower() == 'shelf stocker':
        title = 'Shelf Stocker'
    else: # job not found
        title = ''
    
    if title != '':
        user_info[str(ctx.author.id)]['career'] = title
        await ctx.send(embed=discord.Embed(title='Interview Passed :money_with_wings:', description=f'{ctx.author.name} started a job as a {title}. Type {prefix}work to begin.', color=0xd400ff))

        with open(path+r'/resources/user_data.json', 'w') as f:
            json.dump(user_info, f)


## JOB COMMANDS END ## 

## STAT COMMANDS START ##

@client.command()
async def stats(message, member: typing.Union[discord.Member, str] = None):
    await initialise(message.author)

    with open(path+r'/resources/user_data.json', 'r') as f:
            user_info = json.load(f)

    if type(member) == discord.Member: ## if a user is mentioned
        user = member
        await initialise(user)
    else:
        user = message.author

    bal = int((user_info[str(user.id)]['balance']))
    job = str(user_info[str(user.id)]['career'])
    rank = str(user_info[str(user.id)]['rank'])

    stats = discord.Embed(
        colour=0x00ff55,
        title=f"{user.name}\'s Balance :money_with_wings:",
    )

    stats.add_field(name="Balance", value=f'``{bal:,d} coins``')
    stats.add_field(name='Career', value=f'``{job}``')
    stats.add_field(name='Rank', value=f'``{rank}``')

    await message.channel.send(embed=stats)

## STAT COMMANDS END ##

client.run(token)