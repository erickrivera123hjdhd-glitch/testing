import discord
from discord import app_commands
from src.database.database import Database
from datetime import datetime

db = Database()

@app_commands.command(name='status', description='Check the current connection status')
async def status_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    conn = db.get_connection(user_id)
    
    if conn:
        connected_at = datetime.fromisoformat(str(conn[6])) if conn[6] else datetime.now()
        uptime = datetime.now() - connected_at
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        
        embed = discord.Embed(title='📊 Connection Status', color=0x00ff00)
        embed.add_field(name='🟢 Status', value='Connected', inline=True)
        embed.add_field(name='👤 Player', value=conn[1], inline=True)
        embed.add_field(name='​', value='​', inline=True)
        embed.add_field(name='🕒 Uptime', value=uptime_str, inline=True)
        embed.add_field(name='⚡ Last Command', value=conn[4] or 'None', inline=True)
        embed.add_field(name='✅ Last Response', value=conn[5] or 'None', inline=True)
        embed.set_footer(text='Session active')
    else:
        embed = discord.Embed(title='📊 Connection Status', color=0xff0000)
        embed.add_field(name='🔴 Status', value='Not Connected', inline=False)
        embed.add_field(name='ℹ️', value='Run /setup to generate the Roblox script and /panel to connect', inline=False)
    
    await interaction.response.send_message(embed=embed)
