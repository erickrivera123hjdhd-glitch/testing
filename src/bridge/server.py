import asyncio
import websockets
import json
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BridgeServer:
    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.connections = {}
        self.running = False

    async def start(self):
        self.running = True
        async with websockets.serve(self.handle_client, self.config.bridge_host, self.config.bridge_port):
            logger.info(f'Bridge server listening on {self.config.bridge_host}:{self.config.bridge_port}')
            await asyncio.Future()

    async def handle_client(self, websocket, path):
        session_token = str(uuid.uuid4())
        client_id = None
        try:
            async for message in websocket:
                data = json.loads(message)
                if data.get('type') == 'auth':
                    if data.get('token') == self.config.bridge_secret:
                        client_id = data.get('user_id')
                        self.connections[client_id] = {
                            'websocket': websocket,
                            'session_token': session_token,
                            'connected_at': datetime.now()
                        }
                        self.db.add_connection(client_id, session_token)
                        await websocket.send(json.dumps({'type': 'auth_success', 'session_token': session_token}))
                        logger.info(f'Client {client_id} authenticated')
                    else:
                        await websocket.send(json.dumps({'type': 'auth_error', 'message': 'Invalid token'}))
                elif data.get('type') == 'command' and client_id:
                    await self.handle_command(client_id, data)
                elif data.get('type') == 'disconnect':
                    break
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            if client_id and client_id in self.connections:
                del self.connections[client_id]
                self.db.disconnect(client_id)
                logger.info(f'Client {client_id} disconnected')

    async def handle_command(self, client_id, data):
        command = data.get('command')
        params = data.get('params', {})
        self.db.update_connection(client_id, last_command=command)
        response = {'type': 'response', 'command': command, 'success': True, 'data': params}
        try:
            await self.connections[client_id]['websocket'].send(json.dumps(response))
            self.db.update_connection(client_id, last_response='OK')
        except Exception as e:
            self.db.update_connection(client_id, last_response=f'Error: {str(e)}')
            logger.error(f'Error sending response to {client_id}: {e}')

    async def send_command(self, client_id, command, params=None):
        if client_id not in self.connections:
            return {'success': False, 'error': 'Client not connected'}
        params = params or {}
        message = json.dumps({'type': 'command', 'command': command, 'params': params})
        try:
            await self.connections[client_id]['websocket'].send(message)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_connection_info(self, client_id):
        if client_id in self.connections:
            conn = self.connections[client_id]
            return {
                'session_token': conn['session_token'],
                'connected_at': conn['connected_at'],
                'uptime': (datetime.now() - conn['connected_at']).total_seconds()
            }
        return None

    def is_connected(self, client_id):
        return client_id in self.connections
