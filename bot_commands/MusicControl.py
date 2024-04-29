import discord
from discord.ext import commands

class MusicControls(discord.ui.View):
    def __init__(self, voice_client, yt, ctx):
        super().__init__(timeout=None)
        self.voice_client = voice_client
        self.yt = yt
        self.ctx = ctx

    @discord.ui.button(label="Play", style=discord.ButtonStyle.green)
    async def play(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.voice_client.is_paused():
            self.voice_client.resume()
            await interaction.response.edit_message(content=f'Resumed: **{self.yt.title}**', view=self)

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.red)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.voice_client.is_playing():
            self.voice_client.pause()
            await interaction.response.edit_message(content=f'Paused: **{self.yt.title}**', view=self)

    @discord.ui.button(label="Volume +", style=discord.ButtonStyle.blurple)
    async def volume_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.voice_client.source:
            volume = self.voice_client.source.volume + 0.2
            if volume > 2.0:
                volume = 2.0
            self.voice_client.source.volume = volume
            await interaction.response.edit_message(content=f'Volume Increased for **{self.yt.title}**', view=self)

    @discord.ui.button(label="Volume -", style=discord.ButtonStyle.blurple)
    async def volume_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.voice_client.source:
            volume = self.voice_client.source.volume - 0.2
            if volume < 0:
                volume = 0
            self.voice_client.source.volume = volume
            await interaction.response.edit_message(content=f'Volume Decreased for **{self.yt.title}**', view=self)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.grey)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.voice_client.is_playing() or self.voice_client.is_paused():
            self.voice_client.stop()
            await self.voice_client.disconnect()
            await interaction.response.edit_message(content=f'Stopped: **{self.yt.title}**', view=None)