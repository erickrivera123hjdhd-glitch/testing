import discord
from discord import app_commands
from discord.ext import pages
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
            string.format("ws://%%s:%%d/bridge", BRIDGE_HOST, BRIDGE_PORT),
            message
        )
    end)
end

local function handleResponse(data)
    local decoded = HttpService:JSONDecode(data)
    if decoded.type == "response" then
        print("Command response:", decoded.command, decoded.success)
    end
end

-- Wait for authentication
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

-- Expose control functions
return {
    move = function(direction)
        sendCommand("move", {direction = direction})
    end,
    jump = function()
        sendCommand("jump")
    end,
    sit = function()
        sendCommand("sit")
    end,
    stand = function()
        sendCommand("stand")
    end,
    reset = function()
        sendCommand("reset")
    end,
    executeScript = function(script)
        sendCommand("execute", {script = script})
    end
}
'''

@app_commands.command(name='setup', description='Generate Roblox-side setup script')
async def setup_command(interaction: discord.Interaction):
    bridge_host = os.getenv('BRIDGE_HOST', 'localhost')
    bridge_port = os.getenv('BRIDGE_PORT', '3000')
    bridge_secret = os.getenv('BRIDGE_SECRET', 'secret')
    
    script_content = ROBLOX_SCRIPT % (bridge_host, bridge_port, bridge_secret)
    
    embed = discord.Embed(title='🔧 Roblox Control Setup', color=0x00ff00)
    embed.add_field(name='📋 Setup Instructions', value='1. Create a LocalScript in StarterPlayerScripts\n2. Paste the script below into the LocalScript\n3. Save the script\n4. Join your Roblox experience\n5. Run /panel to open the control dashboard', inline=False)
    embed.add_field(name='🌐 Bridge Configuration', value=f'Host: `{bridge_host}`\nPort: `{bridge_port}`\nSecret: `{bridge_secret}`', inline=False)
    embed.add_field(name='📝 LocalScript Content', value='```lua\n' + script_content + '\n```', inline=False)
    embed.add_field(name='✅ Connection Test', value='After pasting the script, join your experience and run `/panel` to verify connection.', inline=False)
    
    copy_button = discord.ui.Button(label='📋 Copy Script', style=discord.ButtonStyle.primary, custom_id='copy_script')
    
    class CopyView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(copy_button)
        
        @discord.ui.button(label='📋 Copy Script', style=discord.ButtonStyle.primary, custom_id='copy_script')
        async def copy_script(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(f'Here is the script to copy:\n```lua\n{script_content}\n```', ephemeral=True)
    
    await interaction.response.send_message(embed=embed, view=CopyView())
