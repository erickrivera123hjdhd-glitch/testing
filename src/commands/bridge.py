import discord
from discord import app_commands
from src.database.database import Database

db = Database()

@app_commands.command(name='bridge', description='Bridge server information and controls')
async def bridge_command(interaction: discord.Interaction):
    embed = discord.Embed(title='🌐 Bridge Server', color=0x00ff00)
    embed.add_field(name='📍 Configuration', value='Host: `0.0.0.0`\nPort: `3000`', inline=False)
    embed.add_field(name='📊 Status', value='🟢 Online\nAuthenticated: Yes\nConnected Clients: 1', inline=False)
    embed.add_field(name='🛠️ Actions', value='[Test Bridge] [Reconnect] [Disconnect Client] [Refresh]', inline=False)
    embed.set_footer(text='Bridge server running')
    
    view = BridgeView()
    await interaction.response.send_message(embed=embed, view=view)

class BridgeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label='🔄 Refresh', style=discord.ButtonStyle.secondary, custom_id='bridge_refresh')
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title='🌐 Bridge Server', color=0x00ff00)
        embed.add_field(name='📍 Configuration', value='Host: `0.0.0.0`\nPort: `3000`', inline=False)
        embed.add_field(name='📊 Status', value='🟢 Online\nAuthenticated: Yes\nConnected Clients: 1', inline=False)
        embed.add_field(name='🛠️ Actions', value='[Test Bridge] [Reconnect] [Disconnect Client] [Refresh]', inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='🧪 Test Bridge', style=discord.ButtonStyle.primary, custom_id='test_bridge')
    async def test(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Bridge test initiated...', ephemeral=True)
