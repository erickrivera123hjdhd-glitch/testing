import discord
from discord import app_commands
from src.database.database import Database
from src.bridge.server import BridgeServer
import os

db = Database()

@app_commands.command(name='panel', description='Open the Roblox Control Dashboard')
async def panel_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    is_allowed = db.is_user_allowed(user_id) or db.is_role_allowed(str(interaction.user.roles[0].id)) if interaction.user.roles else False
    
    if not is_allowed:
        await interaction.response.send_message('❌ You do not have permission to use the control panel.', ephemeral=True)
        return
    
    embed = discord.Embed(title='🎮 ROBLOX CONTROL DASHBOARD', color=0x00ff00)
    embed.add_field(name='🔗 CONNECTION', value='🟢 Connected\nPlayer: Loading...\nSession: Authenticating...', inline=False)
    embed.add_field(name='🕹️ CHARACTER CONTROL', value='[Forward] [Backward] [Left] [Right]\n[Jump] [Stop] [Reset]', inline=False)
    embed.add_field(name='⚡ ACTIONS', value='[Sit] [Stand] [Jump] [Reset]', inline=False)
    embed.add_field(name='📜 SCRIPTS', value='Execute Lua scripts on the connected client', inline=False)
    embed.add_field(name='ℹ️ ROBLOX INFO', value='Username: --\nUser ID: --\nPlace ID: --\nPosition: --', inline=False)
    embed.add_field(name='🌐 BRIDGE', value=f'Host: `{os.getenv("BRIDGE_HOST", "localhost")}`\nPort: `{os.getenv("BRIDGE_PORT", "3000")}`\nStatus: 🟢 Online', inline=False)
    embed.set_footer(text='Use the buttons below to control your Roblox client')\n    
    view = ControlPanelView()
    await interaction.response.send_message(embed=embed, view=view)

class ControlPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label='🔄 Refresh', style=discord.ButtonStyle.secondary, custom_id='refresh')
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.build_embed(), view=self)

    @discord.ui.button(label='🔌 Disconnect', style=discord.ButtonStyle.danger, custom_id='disconnect')
    async def disconnect(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Disconnect functionality - implement bridge disconnect', ephemeral=True)

    @discord.ui.button(label='▶️ Forward', style=discord.ButtonStyle.success, custom_id='forward')
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Moving forward...', ephemeral=True)

    @discord.ui.button(label='⏹️ Stop', style=discord.ButtonStyle.secondary, custom_id='stop')
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Stopping movement...', ephemeral=True)

    @discord.ui.button(label='🦘 Jump', style=discord.ButtonStyle.success, custom_id='jump')
    async def jump(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Jumping...', ephemeral=True)

    @discord.ui.button(label='📜 Execute Script', style=discord.ButtonStyle.primary, custom_id='execute')
    async def execute_script(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ScriptModal()
        await interaction.response.send_modal(modal)

    def build_embed(self):
        embed = discord.Embed(title='🎮 ROBLOX CONTROL DASHBOARD', color=0x00ff00)
        embed.add_field(name='🔗 CONNECTION', value='🟢 Connected\nPlayer: RobloxUser\nSession: Authenticated', inline=False)
        embed.add_field(name='🕹️ CHARACTER CONTROL', value='[Forward] [Backward] [Left] [Right]\n[Jump] [Stop] [Reset]', inline=False)
        embed.add_field(name='⚡ ACTIONS', value='[Sit] [Stand] [Jump] [Reset]', inline=False)
        embed.add_field(name='📜 SCRIPTS', value='Execute Lua scripts on the connected client', inline=False)
        embed.add_field(name='ℹ️ ROBLOX INFO', value='Username: RobloxUser\nUser ID: 12345\nPosition: (0, 5, 0)', inline=False)
        embed.add_field(name='🌐 BRIDGE', value=f'Host: `{os.getenv("BRIDGE_HOST", "localhost")}`\nPort: `{os.getenv("BRIDGE_PORT", "3000")}`\nStatus: 🟢 Online', inline=False)
        embed.set_footer(text='Use the buttons below to control your Roblox client')
        return embed

class ScriptModal(discord.ui.Modal, title='Execute Lua Script'):
    script_input = discord.ui.TextInput(label='Lua Script', style=discord.TextStyle.paragraph, placeholder='print("Hello World")', max_length=2000)
    
    async def on_submit(self, interaction: discord.Interaction):
        script = self.script_input.value
        await interaction.response.send_message(f'Executing script...\n```lua\n{script}\n```', ephemeral=True)
