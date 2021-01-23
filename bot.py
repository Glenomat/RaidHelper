import discord
from discord.ext import commands
import os
import sqlite3

bot = commands.Bot(command_prefix = '.', help_command=None)
with open('auth.txt', 'r') as f:
    token = f.read()


@bot.event
async def on_ready():
    print('Bot is Online!')


@bot.command()
async def help(ctx):
        help = discord.Embed(
            title = 'Help',
            description = 'Liste aller Commands.',
            colour = discord.Colour.red()
        )
        help.add_field(name='help', value='.help', inline=False)
        help.add_field(name='raid', value='.raid <datum> <zeit> <name>\nErstellt einen Raid', inline=False)
        help.add_field(name='raids', value='.raids\nZeigt alle Raids an', inline=False)
        help.add_field(name='delRaid', value='.delRaids <index>\nLöscht einen Bestimmten raid basierend auf der Nummer bei .raids', inline=False)
        help.add_field(name='clearRaids', value='.clearRaids\nLöscht alle Raids')
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()
        await ctx.send(embed=help)

@bot.command()
@commands.has_role('Raid Leiter')
async def raid(ctx, date, time, *, name):
    if(os.path.isfile('Raids.db') == False):
        conn = sqlite3.connect('Raids.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE Raids
                    ("index" INTEGER NOT NULL UNIQUE,
                    "date" TEXT,
                    "time" TEXT,
                    "name" TEXT,
                    PRIMARY KEY("index" AUTOINCREMENT))''')
    if(os.path.isfile('Raids.db') == True):
        conn = sqlite3.connect('Raids.db')
        c = conn.cursor()
        c.execute(f'''INSERT INTO Raids (date, time, name) VALUES
                    ("{date}", "{time}", "{name}")''')
    conn.commit()
    conn.close()

    raid = discord.Embed(
        title = name,
        description = f'Raiding {name}',
        colour = discord.Colour.blue()
    )
    raid.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    raid.add_field(name='Datum', value=date, inline=True)
    raid.add_field(name='Zeit', value=time, inline=True)

    msg = await ctx.channel.fetch_message(ctx.message.id)
    await msg.delete()
    await ctx.send(embed=raid)


@bot.command()
async def raids(ctx):
    if(os.path.isfile('Raids.db') == False):
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()
        await ctx.send('No Raids in Database!')
    if(os.path.isfile('Raids.db') == True):
        conn = sqlite3.connect('Raids.db')
        c = conn.cursor()
        raids = discord.Embed(
            title='Raids',
            colour=discord.Colour.red()
        )
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()
        for row in c.execute('SELECT * FROM Raids'):
            raids.add_field(name=f'{row[0]}. {row[3]}', value=f'Datum: {row[1]}\nZeit: {row[2]}', inline=False)
        await ctx.send(embed=raids)
        conn.close()


@bot.command()
@commands.has_role('Raid Leiter')
async def delRaid(ctx, index):
    if(os.path.isfile('Raids.db') == False):
        await ctx.send('No Raids in Database!')
    if(os.path.isfile('Raids.db') == True):
        conn = sqlite3.connect('Raids.db')
        c = conn.cursor()
        c.execute(f'''DELETE FROM Raids
                    WHERE "index"={index};''')
        c.execute(f'''UPDATE Raids
                    SET "index" = "index" - 1 WHERE "index" > {index}''')
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()
        await ctx.send(f'Raid Nr {index} wurde gelöscht!')
        conn.commit()
        conn.close()

@bot.command()
@commands.has_role('Raid Leiter')
async def clearRaids(ctx):
    if(os.path.isfile('Raids.db') == False):
        await ctx.send('No Raids to Delete')
    if(os.path.isfile('Raids.db') == True):
        os.remove('Raids.db')
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()
        await ctx.send('Alle Raids wurden Gelöscht!')
bot.run(token)

