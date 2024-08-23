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

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QByteArray
from PyQt6.QtNetwork import QTcpSocket

class LuxClient(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    error_occurred = pyqtSignal(str)
    message_received = pyqtSignal([str],[bytes])
    binary_data_received = pyqtSignal(bytes)

    def __init__(self, host, port, username, regcode):
        super().__init__()
        self.host = host
        self.port = port
        self.username = username
        self.regcode = regcode
        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)
        self.socket.errorOccurred.connect(self.on_error)
        self.socket.readyRead.connect(self.on_ready_read)
        self.buffer = QByteArray()
        self.expecting_binary = False
        self.binary_size = 0

    def connect_to_server(self):
        print(f"Connecting to {self.host}:{self.port}")
        self.socket.connectToHost(self.host, self.port)

    def send_message(self, message):
        print(f"Sending: {message.strip()}")
        self.socket.write((message).encode('utf-8'))
        self.socket.flush()

    @pyqtSlot()
    def on_connected(self):
        print("Connected to server")
        self.connected.emit()
        self.handshake()

    @pyqtSlot()
    def on_disconnected(self):
        print("Disconnected from server")
        self.disconnected.emit()

    @pyqtSlot(QTcpSocket.SocketError)
    def on_error(self, error):
        error_string = self.socket.errorString()
        print(f"Socket error: {error_string}")
        self.error_occurred.emit(error_string)

    @pyqtSlot()
    def on_ready_read(self):
        self.buffer.append(self.socket.readAll())
        self.process_buffer()

    def process_buffer(self):
        while self.buffer.size() > 0:
            if self.expecting_binary:
                if self.buffer.size() >= self.binary_size:
                    binary_data = self.buffer.left(self.binary_size)
                    self.buffer.remove(0, self.binary_size)
                    self.process_binary_data(binary_data.data())
                    self.expecting_binary = False
                else:
                    break  # Not enough data yet
            else:
                index = self.buffer.indexOf(b'\n')
                if index != -1:
                    line = self.buffer.left(index).data()
                    self.buffer.remove(0, index + 1)
                    try:
                        text = line
                        if type(text) == str:
                            self.message_received[str].emit(text)
                        elif type(text) == bytes:
                            self.message_received[bytes].emit(text)
                    except UnicodeDecodeError:
                        print(f"Failed to decode: {line}")
                else:
                    break  # No complete line in buffer

    def handshake(self):
        self.send_message(f"LUXCONNECT-6.4:{self.username}\n")
        self.authenticate(self.regcode)
        self.send_message("guestOnly: true")
        self.send_version("6.64")
        self.send_id2("8CF8C50D8671")
        self.send_newline()

    def authenticate(self, user_key):
        self.send_message(f"userKey: {user_key}\n")

    def send_version(self, version):
        self.send_message(f"remote-version: {version}\nid: 404773\n")

    def send_id2(self, id2):
        self.send_message(f"id2: {id2}\n")

    def send_newline(self):
        self.send_message("\n")

    def process_binary_data(self, data):
        print(f"Processing binary data of length: {len(data)}")
        self.binary_data_received.emit(data)