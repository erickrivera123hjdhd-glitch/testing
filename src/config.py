import os
from dataclasses import dataclass

@dataclass
class Config:
    discord_token: str = os.getenv('DISCORD_TOKEN', '')
    bridge_host: str = os.getenv('BRIDGE_HOST', '0.0.0.0')
    bridge_port: int = int(os.getenv('BRIDGE_PORT', '3000'))
    bridge_secret: str = os.getenv('BRIDGE_SECRET', 'secret')
    database_path: str = os.getenv('DATABASE_PATH', 'data/bot.db')
    session_timeout: int = int(os.getenv('SESSION_TIMEOUT', '300'))
    max_connections: int = int(os.getenv('MAX_CONNECTIONS', '1'))
