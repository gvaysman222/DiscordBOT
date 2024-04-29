import discord
from discord.ext import commands
import discord.voice_client
import asyncio
from pytube import YouTube, Search
from bot_commands.MusicControl import MusicControls

GUILD = 'ЧУШПАН НЕМИРИЧ'
CHANNEL = 'НАХУЙ'
AUDIO_FILE = '23.mp3'
AUDIO_FILE2 = '24.mp3'
AUDIO_FILE3 = '25.mp3'

bot = commands.Bot(command_prefix='#', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def anton(ctx):
    channel = discord.utils.get(ctx.guild.voice_channels, name=CHANNEL)
    if channel:
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=AUDIO_FILE), after=lambda e: print('done', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

@bot.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def p_survival_stats(ctx):
    await ctx.send(f'ИДИ НАХУЙ')
@bot.command()
async def andrey(ctx):
    channel = discord.utils.get(ctx.guild.voice_channels, name=CHANNEL)
    if channel:
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=AUDIO_FILE2), after=lambda e: print('done', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

@bot.command()
async def otvet(ctx):
    channel = discord.utils.get(ctx.guild.voice_channels, name=CHANNEL)
    if channel:
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=AUDIO_FILE3), after=lambda e: print('done', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.message.author.voice:
        await ctx.send("Ты не в голосовом канале!")
        return

    channel = ctx.message.author.voice.channel
    if ctx.voice_client is None:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client

    # Проверяем, является ли это URL
    if "youtube.com/watch?" in search or "youtu.be/" in search:
        yt = YouTube(search)
    else:
        search_results = Search(search)
        yt = search_results.results[0] if search_results.results else None

    if yt is None:
        await ctx.send("Не удалось найти видео по запросу.")
        return

    stream = yt.streams.filter(only_audio=True).first()
    if stream is None:
        await ctx.send("Нет доступных аудио потоков для этого видео.")
        return

    audio_url = stream.url
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
    audio_source = discord.PCMVolumeTransformer(source)
    voice_client.play(audio_source, after=lambda e: print('Player error: %s' % e) if e else None)
    controls = MusicControls(voice_client, yt, ctx)
    await ctx.send(f'Now playing: **{yt.title}**', view=controls)

bot.run('MTA3OTM4NzYyODI0MTE3NDU2OA.GHbHvk.KkEd05mw98A0VMWl5ry5FtpgdO3o7aJQgumvWE')
