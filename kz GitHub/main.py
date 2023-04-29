
import discord
import config
import asyncio 
import random
import disnake
import operator
import datetime
import re
import os
import httpx
import functools
import itertools
import math
import youtube_dl
import ytdl
import voice
import json
import music
import yt_dlp as youtube_dl

from async_timeout import timeout
from disnake.ext import commands
from discord.ext import commands
from youtube_dl import YoutubeDL
from webbrowser import get
from asyncio import sleep
from typing import Optional
from discord.ui.item import Item # Подключаем библиотеку
from distutils.sysconfig import PREFIX
from sys import prefix
from bs4 import BeautifulSoup
from Cybernator import Paginator



bot = commands.Bot(command_prefix='<', intents=discord.Intents.all(), case_insensitive=True, first_guilds=[936981306372395078]) #intents=intents help_command=None guilds=[936981306372395078]
bot.remove_command("help")
CENSORED_WORDS = ["may", "bay", "vay"]
# YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'} #worst
# FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


#______________________________ CLASS ______________________________

# Party
class Confirm(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=10)
        self.value = Optional[bool]

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="👨🏻")
    async def confirm(self, button: discord.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message("Чичас буит ссылка")
        self.value = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="👨🏿")
    async def cancel(self, button: discord.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message("Нет так гей")
        self.value = False
        self.stop()

    @discord.ui.button(label="I'll think", style=discord.ButtonStyle.blurple, emoji="🌈") #, row=1
    async def think(self, button: discord.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message("Думай быстро")
        self.value = False
        self.stop()

class LinkToParty(discord.ui.View):
     def __init__(self):
          super().__init__()
          self.add_item(discord.ui.Button(label="Го с нами!", url="https://discord.gg/NWXZBgQ5"))

# Dropdown
class Dropdown(disnake.ui.StringSelect):
     
    def __init__(self):
        options = [
            disnake.SelectOption(label="DildoL", description="Вери биг", emoji="🍆"),
            disnake.SelectOption(label="DildoM", description="Медиуи", emoji="🥒"),
            disnake.SelectOption(label="DildoS", description="Смол", emoji="🖍")
        ]

        super().__init__(
            placeholder="MENU",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, inter: disnake.MessageInteraction):
         await inter.response.send_message(f"Тебя будут долбить {self.values[0]}. Жди блять")

class DropdownView(disnake.ui.View):   
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())


#______________________________ EVENTS ______________________________

# Ready
@bot.event
async def on_ready():
        print('Бля запустился!')
        bot.add_cog(music.Music(bot)) #####
        
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('очке'))

# Join
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles,  id=1101280141822394468)   # 1-й = await guild_id=member.guild.id    member.guild.roles
    channel = bot.get_channel(1101280635403894946) #member.guild.system_channel 2-й

    embed = discord.Embed(
         title="New Gay!",
         description=f"{member.name}#{member.discriminator}",
         color=0x6efdff
    )
    await member.add_roles(role)
    await channel.send(embed=embed)

# Censored
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    for content in message.content.split():
        for censored_word in CENSORED_WORDS:
            if content.lower() == censored_word:
                   await message.delete()
                   await message.channel.send(f"{message.author.mention}, ещё раз и получишь в ебучку")

# Error
@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error,commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, недостаточно лев")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=discord.Embed(description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"))

#______________________________ COMMANDS ______________________________

# Music
# @bot.command()
# async def play(ctx, url ):
#     vc = await ctx.message.author.voice.channel.connect()
#     with YoutubeDL(YDL_OPTIONS) as ydl:
#         if 'https://' in url:
#             info = ydl.extract_info(url, download=False)
#         else:
#             info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]

#     link = info['formats'][0]['url']

#     vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=link, **FFMPEG_OPTIONS))


# @bot.command()
# async def play(ctx, url):
#     global vc

#     try:
#         voice_channel = ctx.message.author.voice.channel
#         vc = await voice_channel.connect()
#     except:
#         print('Уже подключен или не удалось подключиться')

#     if vc.is_playing():
#         await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')

#     else:
#         with YoutubeDL(YDL_OPTIONS) as ydl:
#             info = ydl.extract_info(url, download=False)

#         URL = info['formats'][0]['url']

#         vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))
                
#         while vc.is_playing():
#             await sleep(1)
#         if not vc.is_paused():
#             await vc.disconnect()


# Clear
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, count: int):
        await ctx.channel.purge(limit=count+1)
        await ctx.send(f"Удаленно {count} сообщений")

# Random
@bot.command()
async def rand(ctx, *arg):
    await ctx.reply(random.randint(0, 100))


# Help
@bot.command( pass_context = True )
async def test(ctx):
    #await ctx.send("ЭЭЭЭта каманды")

    emb = discord.Embed(title = 'Ready Commands:	*count	@member	#reasone')
    emb.add_field(name='<clear *', value='Очистка чата')
    emb.add_field(name='<ban @ * #', value='ban')
    emb.add_field(name='<kick @ #', value='kick')
    emb.add_field(name='<rand', value='Rand 1-100')
    emb.add_field(name='<party', value='Party')
    emb.add_field(name='/calc', value='Calc')
    await ctx.send(embed=emb)

# Test
@bot.command()
async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title="Основные команды help", description='Ready Commands:	*count	@member	#reasone', color=0x0050FF)
    emb.add_field(name='<rand', value='Rand 1-100')
    emb.add_field(name='<party', value='Party')
    emb.add_field(name='<invite', value='invite')
    emb.add_field(name='/calc', value='Calc')
    embed2 = discord.Embed(title="Admin command help", description='Ready Commands:	*count	@member	#reasone', color=0xFF0000)
    embed2.add_field(name='<clear *', value='Очистка чата')
    embed2.add_field(name='<ban @ * #', value='ban')
    embed2.add_field(name='<kick @ #', value='kick')
    embed2.add_field(name='<unban id #', value='unban')
    embed2.add_field(name='<mute', value='mute')
    embed3 = discord.Embed(title="Music", description='name or url', color=0x4DFF00)
    embed3.add_field(name='<join', value='')
    embed3.add_field(name='<summon', value='')
    embed3.add_field(name='<disconnect', value='<leave')
    embed3.add_field(name='<play', value='<p')
    embed3.add_field(name='<stop', value='')
    embed3.add_field(name='<pause', value='<pa')
    embed3.add_field(name='<resume', value='<re <res')
    embed3.add_field(name='<skip', value='<s')
    embed3.add_field(name='<now', value='<current <playing <np <nowplaying')
    embed3.add_field(name='<queue', value='')
    embed3.add_field(name='<history', value='')
    embed3.add_field(name='<volume', value='')
    embed3.add_field(name='<shuffle', value='')
    embed3.add_field(name='<remove', value='')
    embed3.add_field(name='<loop', value='')
    embed3.add_field(name='<autoplay', value='')
    embed3.add_field(name='<search', value='')
    embed4 = discord.Embed(title="Вак", description='гей')
    embeds = [emb, embed2, embed3, embed4]
    message = await ctx.send(embed=emb)
    page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=embeds)
    await page.start()

# Ban Kick
def str_time_to_seconds(str_time, language='ru'):
    conv_dict = {
        'w': 'weeks',
        'week': 'weeks',
        'weeks': 'weeks',
        'н': 'weeks',
        'нед': 'weeks',
        'неделя': 'weeks',
        'недели': 'weeks',
        'недель': 'weeks',
        'неделю': 'weeks',

        'd': 'days',
        'day': 'days',
        'days': 'days',
        'д': 'days',
        'день': 'days',
        'дня': 'days',
        'дней': 'days',

        'h': 'hours',
        'h': 'hours',
        'hour': 'hours',
        'hours': 'hours',
        'ч': 'hours',
        'час': 'hours',
        'часа': 'hours',
        'часов': 'hours',

        'm': 'minutes',
        'min': 'minutes',
        'mins': 'minutes',
        'minute': 'minutes',
        'minutes': 'minutes',
        'мин': 'minutes',
        'минута': 'minutes',
        'минуту': 'minutes',
        'минуты': 'minutes',
        'минут': 'minutes',

        's': 'seconds',
        'sec': 'seconds',
        'secs': 'seconds',
        'second': 'seconds',
        'seconds': 'seconds',
        'сек': 'seconds',
        'секунда': 'seconds',
        'секунду': 'seconds',
        'секунды': 'seconds',
        'секунд': 'seconds'
    }

    pat = r'[0-9]+[w|week|weeks|н|нед|неделя|недели|недель|неделю|d|day|days|д|день|дня|дней|h|hour|hours|ч|час|часа|часов|min|mins|minute|minutes|мин|минута|минуту|минуты|минут|s|sec|secs|second|seconds|c|сек|секунда|секунду|секунды|секунд]{1}'
    def timestr_to_dict(tstr):
        #convert 1d2h3m4s to {"d": 1, "h": 2, "m": 3, "s": 4}
        return {conv_dict[p[-1]]: int(p[:-1]) for p in re.findall(pat, str_time)}

    def timestr_to_seconds(tstr):
        return datetime.timedelta(**timestr_to_dict(tstr)).total_seconds()

    def plural(n, arg):
        days = []
        if language == "ru":
            if arg == 'weeks':
                days = ['неделя', 'недели', 'недель']
            elif arg == 'days':
                days = ['день', 'дня', 'дней']
            elif arg == 'hours':
                days = ['час', 'часа', 'часов']
            elif arg == 'minutes':
                days = ['минута', 'минуты', 'минут']
            elif arg == 'seconds':
                days = ['секунда', 'секунды', 'секунд']
        elif language == "en":
            if arg == 'weeks':
                days = ['week', 'weeks', 'weeks']        
            elif arg == 'days':
                days = ['day', 'day', 'days']
            elif arg == 'hours':
                days = ['hour', 'hour', 'hours']
            elif arg == 'minutes':
                days = ['minute', 'minute', 'minutes']
            elif arg == 'seconds':
                days = ['second', 'second', 'seconds']

        if n % 10 == 1 and n % 100 != 11:
            p = 0
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            p = 1
        else:
            p = 2
        return str(n) + ' ' + days[p]

    counter_in_str = ""
    for i in timestr_to_dict(str_time).items():
        counter_in_str += f"{plural(i[1], i[0])} "

    return int(timestr_to_seconds(str_time)), counter_in_str

@bot.command(name="!бан", aliases=["ban", "бан", "вбаню", "спатьнахуй"]) #
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, time, reason=" Еблан"):
    await ctx.send(f'{member.mention} **забанен** \n Продолжительность бана: *{time}h* \n Причина бана: {reason}')
    await member.send(f'Тебя забанили на сервере {ctx.guild.name} по причине {reason}')
    await member.ban(reason=reason)
    seconds, str_time = str_time_to_seconds(time)
    await asyncio.sleep(seconds)
    await member.unban()
    await ctx.send(f'*У {member.mention} закончился бан*')
    link = await ctx.channel.create_invite(max_age=300)
    await member.send(f'У тебя закончился бан на сервере "{ctx.guild.name}"! {link}')

@bot.command()
async def invite(ctx):
    link = await ctx.channel.create_invite(max_age = 300, max_uses=1) # all of these default to 0, aka forever
    await ctx.send(f"Приглашение для {ctx.author.mention}: {link}")

# async def ban(ctx, member: discord.Member = None, time = None, *, reason: str = None):
#     async def unb(member):
#         users = await ctx.guild.bans()
#         for ban_user in users:
#             if ban_user.user == member:
#                 await ctx.guild.unban(ban_user.user)
 
#     if member:
#         if time: 
#             time_letter = time[-1:] 
#             time_numbers = int(time[:-1]) 
 
#             def t(time_letter): 
#                 if time_letter == 's':
#                     return 1
#                 if time_letter == 'm':
#                     return 60
#                 if time_letter == 'h':
#                     return 60*60
#                 if time_letter == 'd':
#                     return 60*60*24
#             if reason:
#                 await member.ban(reason=reason)
#                 await ctx.send(embed=discord.Embed(description=f'Пользователь {member.mention} был забанен \nВремя: {time} \nПричина: {reason}' ))
 
#                 await asyncio.sleep(time_numbers*t(time_letter))
 
#                 await unb(member)
#                 await ctx.send(f'Польнзователь {member.mention} разбанен')
#             else:
#                 await member.ban()
#                 await ctx.send(embed=discord.Embed(description=f'Пользователь {member.mention} был забанен \nВремя: {time}'))
 
#                 await asyncio.sleep(time_numbers*t(time_letter))
 
#                 await unb(member)
#                 await ctx.send(f'Польнзователь {member.mention} разбанен')
#         else:
#             await member.ban()
#             await ctx.send(embed=discord.Embed(description=f'Пользователь {member.mention} был забанен'))
#     else: 
#         await ctx.send('Введите имя пользователя')
 
 
@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def unban(ctx, member: int, *, reason="Отсосал"):
    try:
        banned_user = await ctx.guild.fetch_ban(disnake.Object(member))
    except disnake.NotFound:
        await ctx.send(f'Пользователь с ID {member} не забанен на сервере', delete_after=10)
        return

    user = banned_user.user
    embed = disnake.Embed(
        title=f"Вы были разбанены на сервере {ctx.guild.name}",
        description=f'Вас разбанил администратор {ctx.author} по причине: "{reason}"',
        color=0x3aed24
    )
    try:
        await user.send(embed=embed)
    except:
        print(f"Can't send embed to {user}, skiping")
        pass
    try:
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f'Администратор {ctx.author.mention} разбанил пользователя {user.mention} по причине: "{reason}"', delete_after=10)
    except:
        await ctx.send(f'Не удалось разбанить пользователя {user.mention}', delete_after=10)

@bot.command(name="!кик", aliases=["кик", "kick"])
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member = None, *, reason=" Еблан"): #reason:str = None reason="Еблан"
        if member:
                
                if reason:
                    await member.kick(reason=reason)
                    await ctx.send(embed=discord.Embed(description=f'Пользователь {member.mention} был кикнут \nПричина:{reason}'))
                else:
                    await member.kick()
                    await ctx.send(embed=discord.Embed(description=f'Пользователь {member.mention} был кикнут'))
        else:
            await ctx.send('Введите имя пользователя')

# Party
@bot.command(name="party")
async def ask_party(ctx):
    view = Confirm()

    await ctx.send("Го на пати?", view=view)
    await view.wait()

    if view.value is None:
         await ctx.send("Проебал возможность")
    elif view.value:
         await ctx.send("Ну шо, погнали", view=LinkToParty())
    else:
         await ctx.send("Ля мудила")

# Order
# @bot.command()
# async def order(ctx):
#     view=DropdownView()
#     await ctx.send("Чем тебя долбить?", view=DropdownView())

# Mute
@bot.command(name="!мут", aliases=["mute", "мут"])
@commands.has_permissions(administrator=True)
async def user_mute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')

    await member.add_roles(mute_role)
    await ctx.send(f'{member.mention} не надолго завалил ебало')
#______________________________ SLASH ______________________________

# Calc
@bot.slash_command(description="+ - * /")
async def calc(inter, a: int, oper: str, b: int):
    if oper == "+":
         result = a + b
    elif oper == "-":
         result = a - b
    elif oper == "*":
         result = a * b
    elif oper == "/":
         result = a / b
    else:
         result = "Не верный оператор"
    await inter.send(str(result))




bot.run(config.token)