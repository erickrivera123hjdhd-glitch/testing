import discord
from discord import app_commands
import os

ROBLOX_SCRIPT = '''-- Roblox Control Bridge Client
local HttpService = game:GetService("HttpService")
local RunService = game:GetService("RunService")

local BRIDGE_HOST = "%s"
local BRIDGE_PORT = %d
local BRIDGE_SECRET = "%s"
local SESSION_TOKEN = nil

local function sendCommand(command, params)
    if not SESSION_TOKEN then return end
    local message = HttpService:JSONEncode({
        type = "command",
        command = command,
        params = params or {}
    })
    local success, err = pcall(function()
        HttpService:PostAsync(
            string.format("http://%%s:%%d/bridge", BRIDGE_HOST, BRIDGE_PORT),
            message
        )
    end)
end

local function authenticate()
    local authData = HttpService:JSONEncode({
        type = "auth",
        token = BRIDGE_SECRET,
        user_id = tostring(game.Players.LocalPlayer.UserId)
    })
    SESSION_TOKEN = "authenticated"
    print("Roblox client connected to bridge")
end

authenticate()

return {
    move = function(direction) sendCommand("move", {direction = direction}) end,
    jump = function() sendCommand("jump") end,
    sit = function() sendCommand("sit") end,
    stand = function() sendCommand("stand") end,
    reset = function() sendCommand("reset") end,
    executeScript = function(script) sendCommand("execute", {script = script}) end
}
'''

@app_commands.command(name='setup', description='Generate Roblox-side setup script')
async def setup_command(interaction: discord.Interaction):
    bridge_host = os.getenv('BRIDGE_HOST', 'localhost')
    bridge_port = int(os.getenv('BRIDGE_PORT', '3000'))
    bridge_secret = os.getenv('BRIDGE_SECRET', 'secret')

    script_content = ROBLOX_SCRIPT % (bridge_host, bridge_port, bridge_secret)

    # Discord embeds have a 1024-character field limit, so send the script as a file.
    embed = discord.Embed(title='Roblox Control Setup', color=0x5865F2)
    embed.add_field(
        name='Setup Instructions',
        value='1. Create a LocalScript in StarterPlayerScripts\n2. Paste the attached script\n3. Join your Roblox experience\n4. Run /panel to open the dashboard',
        inline=False
    )
    embed.add_field(
        name='Bridge Configuration',
        value=f'Host: `{bridge_host}`\nPort: `{bridge_port}`',
        inline=False
    )

    script_file = discord.File(
        fp=__import__('io').BytesIO(script_content.encode('utf-8')),
        filename='roblox_bridge.lua'
    )
    await interaction.response.send_message(embed=embed, file=script_file)
