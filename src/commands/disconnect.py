import discord
from discord import app_commands
from src.database.database import Database

db = Database()


@app_commands.command(
    name="disconnect",
    description="Disconnect the Roblox client",
)
async def disconnect_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    conn = db.get_connection(user_id)

    if conn:
        db.disconnect(user_id)
        embed = discord.Embed(
            title="🔌 Disconnected",
            color=0xFF9900,
        )
        embed.add_field(
            name="Status",
            value="Successfully disconnected from Roblox client",
            inline=False,
        )
        embed.add_field(
            name="Next Steps",
            value="Run /setup to regenerate the script and /panel to reconnect",
            inline=False,
        )
    else:
        embed = discord.Embed(
            title="🔌 Disconnect",
            color=0xFF9900,
        )
        embed.add_field(
            name="Status",
            value="No active connection found",
            inline=False,
        )

    await interaction.response.send_message(embed=embed)
