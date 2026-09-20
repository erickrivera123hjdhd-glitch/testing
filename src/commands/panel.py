import discord
from discord import app_commands
from src.database.database import Database
import os

db = Database()

@app_commands.command(name='panel', description='Open the Roblox Control Dashboard')
async def panel_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    role_allowed = bool(interaction.user.roles) and db.is_role_allowed(str(interaction.user.roles[0].id))
    is_allowed = db.is_user_allowed(user_id) or role_allowed

    if not is_allowed:
        await interaction.response.send_message('You do not have permission to use the control panel.', ephemeral=True)
        return

    embed = build_panel_embed()
    await interaction.response.send_message(embed=embed, view=ControlPanelView())


def build_panel_embed():
    embed = discord.Embed(title='ROBLOX CONTROL DASHBOARD', color=0x00FF00)
    embed.add_field(
        name='CONNECTION',
        value='Connected\nPlayer: Loading...\nSession: Authenticating...',
        inline=False,
    )
    embed.add_field(
        name='CHARACTER CONTROL',
        value='Forward • Backward • Left • Right\nJump • Stop • Reset',
        inline=False,
    )
    embed.add_field(
        name='ACTIONS',
        value='Sit • Stand • Jump • Reset',
        inline=False,
    )
    embed.add_field(
        name='SCRIPTS',
        value='Execute Lua scripts on the connected client',
        inline=False,
    )
    embed.add_field(
        name='ROBLOX INFO',
        value='Username: --\nUser ID: --\nPlace ID: --\nPosition: --',
        inline=False,
    )
    embed.add_field(
        name='BRIDGE',
        value=(
            f'Host: `{os.getenv("BRIDGE_HOST", "localhost")}`\n'
            f'Port: `{os.getenv("BRIDGE_PORT", "3000")}`\n'
            'Status: Online'
        ),
        inline=False,
    )
    embed.set_footer(text='Use the buttons below to control your Roblox client')
    return embed


class ControlPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label='Refresh', style=discord.ButtonStyle.secondary, custom_id='panel_refresh')
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=build_panel_embed(), view=self)

    @discord.ui.button(label='Disconnect', style=discord.ButtonStyle.danger, custom_id='panel_disconnect')
    async def disconnect(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Disconnect requested.', ephemeral=True)

    @discord.ui.button(label='Forward', style=discord.ButtonStyle.success, custom_id='panel_forward')
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Forward requested.', ephemeral=True)

    @discord.ui.button(label='Stop', style=discord.ButtonStyle.secondary, custom_id='panel_stop')
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Stop requested.', ephemeral=True)

    @discord.ui.button(label='Jump', style=discord.ButtonStyle.success, custom_id='panel_jump')
    async def jump(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Jump requested.', ephemeral=True)

    @discord.ui.button(label='Execute Script', style=discord.ButtonStyle.primary, custom_id='panel_execute')
    async def execute_script(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ScriptModal())


class ScriptModal(discord.ui.Modal, title='Execute Lua Script'):
    script_input = discord.ui.TextInput(
        label='Lua Script',
        style=discord.TextStyle.paragraph,
        placeholder='print("Hello World")',
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        script = self.script_input.value
        await interaction.response.send_message(
            f'Executing script...\n```lua\n{script}\n```',
            ephemeral=True,
        )
