import discord
from discord import app_commands

@app_commands.command(name='help', description='Show available commands')
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title='❓ Help - Roblox Control Bot', color=0x00ff00)
    embed.add_field(name='📋 Available Commands', value='''/setup - Generate Roblox-side LocalScript
/panel - Open the main control dashboard
/status - Check connection status
/bridge - View bridge server information
/permissions - Manage user/role permissions (admin only)
/disconnect - Disconnect from Roblox client
/help - Show this help message''', inline=False)
    embed.add_field(name='🚀 Getting Started', value='1. Run /setup to get the Roblox script\n2. Create a LocalScript in StarterPlayerScripts\n3. Paste the script and save\n4. Join your Roblox experience\n5. Run /panel to open the control dashboard', inline=False)
    embed.set_footer(text='Roblox Remote Control Dashboard')
    await interaction.response.send_message(embed=embed)
