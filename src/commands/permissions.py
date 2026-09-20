import discord
from discord import app_commands
from src.database.database import Database

if not os.getenv('DISCORD_TOKEN'):
    import os

db = Database()

@app_commands.command(name='permissions', description='Manage permissions for the control panel')
async def permissions_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    is_admin = interaction.user.guild_permissions.administrator
    
    if not is_admin:
        await interaction.response.send_message('❌ Only administrators can manage permissions.', ephemeral=True)
        return
    
    embed = discord.Embed(title='🔐 Permissions Management', color=0xff9900)
    embed.add_field(name='👥 Allowed Users', value='Configure users who can control Roblox', inline=False)
    embed.add_field(name='🎭 Allowed Roles', value='Configure roles with control permissions', inline=False)
    embed.add_field(name='⚙️ Settings', value='[Add User] [Remove User] [Add Role] [Remove Role] [View Permissions]', inline=False)
    
    view = PermissionsView()
    await interaction.response.send_message(embed=embed, view=view)

class PermissionsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label='➕ Add User', style=discord.ButtonStyle.success, custom_id='add_user')
    async def add_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Add user functionality - implement user management', ephemeral=True)

    @discord.ui.button(label='➖ Remove User', style=discord.ButtonStyle.danger, custom_id='remove_user')
    async def remove_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Remove user functionality - implement user management', ephemeral=True)

    @discord.ui.button(label='➕ Add Role', style=discord.ButtonStyle.success, custom_id='add_role')
    async def add_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Add role functionality - implement role management', ephemeral=True)

    @discord.ui.button(label='➖ Remove Role', style=discord.ButtonStyle.danger, custom_id='remove_role')
    async def remove_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Remove role functionality - implement role management', ephemeral=True)
