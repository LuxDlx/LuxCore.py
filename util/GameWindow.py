from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QTextEdit, QLineEdit, QApplication
from PyQt6.QtGui import QColor, QPainter, QPixmap, QBrush, QPen
from PyQt6.QtCore import QTimer, Qt
from util.GameBoard import GameBoardWidget
from util.LuxClient import LuxClient
import util.utils as utils
import util.dice as dice
import json
import os
import sys
import struct
import webbrowser
import random

cwd = os.path.dirname(os.path.abspath(sys.argv[0]))

BOTTOM_BAR_STYLE = """
    background-color: black;
    color: white;
    padding: 5px;
"""

BUTTON_STYLE = """
    QPushButton {
        background-color: #4A4A4A;
        color: white;
        border: none;
        padding: 5px 10px;
    }
    QPushButton:hover {
        background-color: #5A5A5A;
    }
    QPushButton:pressed {
        background-color: #3A3A3A;
    }
"""

LABEL_STYLE = """
    color: white;
    font-family: 'Impact', sans-serif;
    font-size: 14px;
"""

class ColorBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setFixedWidth(350)
        self.colors = {}
        self.texture = self.load_texture()

    def setColors(self, colors):
        self.colors = colors
        self.update()

    def load_texture(self):
        texture = QPixmap(f"{cwd}/assets/colorbar.png")
        return texture

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the checkerboard texture
        painter.fillRect(self.rect(), QBrush(self.texture))
        total = sum(self.colors.values())
        x = 0
        for color in list(self.colors.keys()):
            if self.colors[color] < 0:
                del self.colors[color]
        for color, value in self.colors.items():
            width = int(self.width() * (value / total))
            
            # Draw the color with 30% opacity
            color_with_alpha = QColor(color)
            color_with_alpha.setAlpha(130)  #  of 255
            painter.fillRect(x, 0, width, self.height(), color_with_alpha)
            
            x += width
        
        # Draw the white border around the entire bar
        pen = QPen(Qt.GlobalColor.white, 2)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

class GameWindow(QMainWindow):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.username = self.main.username
        self.regcode = self.main.regcode
        self.client = LuxClient("87.106.167.115", 6619, self.username, self.regcode)
        self.client.connected.connect(self.on_connected)
        self.client.disconnected.connect(self.on_disconnected)
        self.client.message_received[str].connect(self.on_message_received)
        self.client.message_received[bytes].connect(self.on_message_received)
        self.client.binary_data_received.connect(self.on_binary_data_received)
        self.client.error_occurred.connect(self.on_error)
        self.gameboardstr = ""
        self.gastringcache = ""
        self.ingameboard = False
        self.ingastring = False
        self.setStyleSheet("background-color: black;")
        self.client.connect_to_server()
        

        self.setWindowTitle("Lux Delux Game")
        self.setGeometry(100, 100, 800, 600)  # Adjust size as needed

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Game board
        self.game_board = GameBoardWidget()
        self.game_board.colors = []
        self.game_board.attack_country.connect(self.on_attack_country)
        main_layout.addWidget(self.game_board)
        with open(f"{cwd}/cache/cache.json","r") as f:
            cache = json.load(f)
        board = cache["map"]
        self.players = cache["players"]
        for i in range(6):
            self.game_board.colors.append(QColor(self.players[str(i)]["color"]))
  #      self.game_board.load_board(f"{cwd}/maps/{board}.luxb")

        # Bottom bar
        bottom_bar = QWidget()
        bottom_bar.setFixedHeight(60)
        bottom_bar.setContentsMargins(bottom_bar.contentsMargins().left(),2,bottom_bar.contentsMargins().right(),2)
        bottom_bar.setStyleSheet(BOTTOM_BAR_STYLE)
        bottom_layout = QHBoxLayout(bottom_bar)

        # Timer
        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet(LABEL_STYLE)
        bottom_layout.addWidget(self.timer_label)

        # Color bar
        self.color_bar = ColorBar()
        bottom_layout.addWidget(self.color_bar)

        # Continents button
        self.conts_button = QPushButton(utils.get_locales(self.main.lang,"Bonuses").upper())
        self.conts_button.setStyleSheet(BUTTON_STYLE)
        self.conts_button.setFont(self.main.buttonFont)
        self.button_style = """
            QPushButton {
                color: blue;
                background-color: grey;
                border-radius: 10px;  /* Adjust this value to control the roundness */
                padding: 5px;  /* Add some padding to prevent text from touching the edges */
            }
            QPushButton:hover {
                color: red;
            }
        """
        self.conts_button.setStyleSheet(self.button_style)
        self.conts_button.clicked.connect(self.toggle_continents)
        bottom_layout.addWidget(self.conts_button)

        # Spacer
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Armies to place / End turn / Fortify
        self.armies_label = QLabel("Armies: 0")
        self.armies_label.setStyleSheet(LABEL_STYLE)
        bottom_layout.addWidget(self.armies_label)

        self.end_turn_button = QPushButton("End Turn")
        self.end_turn_button.setStyleSheet(BUTTON_STYLE)
        self.end_turn_button.clicked.connect(self.end_turn)
        bottom_layout.addWidget(self.end_turn_button)

        self.fortify_button = QPushButton("Fortify")
        self.fortify_button.setStyleSheet(BUTTON_STYLE)
        self.fortify_button.clicked.connect(self.fortify)
        bottom_layout.addWidget(self.fortify_button)

        main_layout.addWidget(bottom_bar)

        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_input = QLineEdit()
        self.chat_input.returnPressed.connect(self.send_chat_message)
        self.chat_display.setStyleSheet("background-color: white;") 
        self.chat_input.setStyleSheet("background-color: white;") 
        self.chat_input.setFont(self.main.chatFont)
        self.chat_display.setFont(self.main.smallChatFont)
        chat_layout.addWidget(self.chat_display)
        chat_layout.addWidget(self.chat_input)
        chat_widget.setFixedHeight(150)  # Set a fixed height for the chat box
        main_layout.addWidget(chat_widget)
        # Initialize timer
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_timer)
        self.game_time = 0
        self.game_timer.start(1000)  # Update every second

        # Initialize game state
        self.update_color_bar()
        self.update_armies_label()

    def end_turn(self):
        # Implement end turn logic
        pass

    def fortify(self):
        # Implement fortify logic
        pass

    def send_chat_message(self):
        message = self.chat_input.text()
        if not message.startswith("!"):
            if message:
                self.client.send_message(f"CHAT: {self.username}: {message}\n")
        else:
            command = message[1:]
            if command == "g":
                self.client.send_message(f"guestOnly:\n")
            elif command == "gi":
                self.client.send_message(f"guestIn:\n")
            elif command == "go":
                self.client.send_message(f"guestOut:\n")
            elif command.startswith("love "):
                self.client.send_message(f"HMOTE: {self.username} {message[6:]}\n")
            elif command.startswith("re "):
                self.client.send_message(f"ZMOTE: {self.username} {message[4:]}\n")
            elif command.startswith("sing "):
                self.client.send_message(f"SMOTE: {self.username} {message[6:]}\n")
            elif command.startswith("me "):
                self.client.send_message(f"EMOTE: {self.username} {message[4:]}\n")
            elif command.startswith("help"):
                webbrowser.open("https://sillysoft.net/wiki/?Chat%20Commands")
            elif command.startswith("raw "):
                self.client.send_message(f"{command[4:]}\n")

            elif command.startswith("explode"):
                for i in range(0, 100):
                    self.client.send_message(f"ex: {i}\n")
            else:
                self.client.send_message(f"clientCommand: {command}\n")
        self.chat_input.clear()
        
    def add_chat_message(self, message, system=False, emote=None):
        if not system:
            if not emote:
                self.chat_display.append(f"<span style='color: black;'>{message}</span>")   
            if emote =="EMOTE":
                self.chat_display.append(f"<span style='color: black;'><i>\u221e {message} \u221e</i></span>")
            elif emote =="HMOTE":
                self.chat_display.append(f"<span style='color: maroon;'>\u2665\u2665\u2665 {message} \u2665\u2665\u2665</span>")
            elif emote =="ZMOTE":
                self.chat_display.append(f"<span style='color: blue;'>\u25c6\u25c6\u25c6\u25c6 {message} \u25c6\u25c6\u25c6\u25c6</span>")
            elif emote =="SMOTE":
                self.chat_display.append(f"<span style='color: green;'>\u266a\u266b {message} \u266a\u266b</span>")
        else:
            message_localised = self.localise(message, self.main.lang)
            self.chat_display.append(f"<span style='color: red;'>{message_localised}</span>")
        

    def toggle_continents(self):
        self.game_board.show_continents = not self.game_board.show_continents
        self.game_board.update()
        
        if self.game_board.show_continents:
            # Change background color to light blue when showing continents
            self.conts_button.setStyleSheet(self.button_style + "QPushButton { background-color: lightblue; }")
        else:
            # Reset to original style when showing countries
            self.conts_button.setStyleSheet(self.button_style)
    def update_color_bar(self):
        colors = {}
        colorpower = {}
        for color in self.game_board.colors:
            colors[color.name()] = 0
        for continent in self.game_board.continents:
            for country in continent['countries']:
                color = self.game_board.country_colors[country['id']].name()
                if not colorpower.get(color):
                    colorpower[color] = 1 + int(country["armies"])
                else:
                    colorpower[color] = colorpower[color]+1+int(country["armies"])
        try:
            for color in self.game_board.colors:
                colors[color.name()] = colorpower[color.name()]
            self.color_bar.setColors(colors)
        except:
            pass
    def update_armies_label(self):
        # Example - replace with actual game logic
        armies_to_place = 5
        if armies_to_place > 0:
            self.armies_label.setText(f"Armies: {armies_to_place}")
            self.end_turn_button.setVisible(False)
            self.fortify_button.setVisible(False)
        else:
            self.armies_label.setVisible(False)
            self.end_turn_button.setVisible(True)
            self.fortify_button.setVisible(True)
    def update_timer(self):
        self.game_time += 1
        minutes = self.game_time // 60
        seconds = self.game_time % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def on_connected(self):
        print("Connected to server")

    def on_disconnected(self):
        print("Disconnected from server")

    def on_message_received(self, message):
        messageraw = message if type(message) == str else message.decode("utf-8",errors="ignore")
        if type(message) == str:
            print("Received: " + messageraw) 
        if not self.ingameboard:
            if "<luxboard>" in messageraw:
                self.ingameboard = True
                self.gameboardstr = messageraw
            elif "ga:" in messageraw:
                self.ingastring = True
                self.gastringcache = message
            elif not self.ingastring:
                if messageraw.startswith("CHAT: "):
                    self.add_chat_message(messageraw[6:])  
                elif messageraw.startswith("tra: "):
                    self.add_chat_message(messageraw[5:], system=True)
                elif messageraw.startswith("EMOTE: "):
                    self.add_chat_message(messageraw[7:], emote="EMOTE")
                elif messageraw.startswith("SMOTE: "):
                    self.add_chat_message(messageraw[7:], emote="SMOTE")
                elif messageraw.startswith("HMOTE: "):
                    self.add_chat_message(messageraw[7:], emote="HMOTE")
                elif messageraw.startswith("ZMOTE: "):
                    self.add_chat_message(messageraw[7:], emote="ZMOTE")
                elif messageraw.startswith("sco:"):
                    messageraw = messageraw.replace("sco: ", "")
                    countryid = messageraw.split(" ")[0]
                    countryowner = messageraw.split(" ")[1]
                    self.game_board.update_owner(countryid, str(int(countryowner)-1))
                    self.update_color_bar()
                elif "sco: " in messageraw:
                    messageraw = messageraw.split("sco: ")[1]
                    countryid = int(messageraw.split(" ")[0])
                    countryowner = messageraw.split(" ")[1]
                    self.game_board.update_owner(countryid, str(int(countryowner)-1))
                    self.update_color_bar()
                elif "sc: " in messageraw:
                    messageraw = messageraw.replace("sc: ", "")
                    countryid = int(messageraw)
                    self.game_board.select_country(countryid)
                elif messageraw.startswith("sca: "):
                    messageraw = messageraw.replace("sca: ", "")
                    countryid = messageraw.split(" ")[0]
                    armycount = messageraw.split(" ")[1]
                    self.game_board.update_army_count(countryid, str(int(armycount)-1))
                    self.update_color_bar()
                elif messageraw.startswith("ex: "):
                    messageraw = messageraw.replace("ex: ", "")
                    countryid = int(messageraw)
                    self.game_board.trigger_explosion(countryid)
                elif messageraw.startswith("gt: "):
                    messageraw = messageraw.replace("gt: ", "")
                    playerid = int(messageraw)
                    bgc = self.game_board.colors[playerid-1].name()
                    self.setStyleSheet(f"background-color: {bgc};")
                    # self.game_board.set_turn(playerid)
                    # self.set_turn(playerid)
                if "java.lang.String;" in messageraw:
                        print("GOT COLORS")
                        colors = utils.get_colors(messageraw)
                        for i, color in enumerate(colors):
                            self.game_board.colors[i] = QColor(*color)
                print(messageraw)
            else:
                if not "-1" in messageraw:
                    self.gastringcache += message
                else:
                    self.gastringcache += message
                    self.ingastring = False
                    winner, quote = utils.get_name_and_quote(self.gastringcache)
                    self.game_board.winner = winner
                    self.game_board.quote = quote
                    print(self.gastringcache)
                    print(winner, quote)
                    self.update_color_bar()
                    self.update_armies_label()
    
        else:
            if not "</luxboard>" in messageraw:
                self.gameboardstr += messageraw
            else:
                self.gameboardstr += messageraw
                self.gameboardstr = self.gameboardstr.replace("&", "and")
                self.ingameboard = False
                self.game_board.load_board_from_str(self.gameboardstr)
                self.update_color_bar()
                self.update_armies_label()

    def on_binary_data_received(self, data):
        print(f"Received binary data of length: {len(data)}")
        if len(data) >= 4:
            value = struct.unpack('>I', data[:4])[0]
            print(f"First 4 bytes as int: {value}")

    def on_error(self, error_string):
        print(f"Error occurred: {error_string}")

    def localise(self, message, lang):
        pairs = [(":Validatingnickname:","Validatingnickname"),(":hasjoinedasguestonly:","hasjoinedasguestonly"),("OnlyServerStart","OnlyServerStart")]
        for replacor, replacement in pairs:
            message = message.replace(replacor, utils.get_locales(lang,replacement))
        return message

    def on_attack_country(self, defendercountry, attackercountry, itera=0):
        attackerarmies = attackercountry["armies"]
        ctrl_pressed = QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier
        defenderarmies = defendercountry["armies"]
        defenderid = defendercountry["id"]
        attackerid = attackercountry["id"]
        if ctrl_pressed and itera == 0:
            while int(attackerarmies) > 0:
                attackerarmies, defenderarmies = self.on_attack_country(defendercountry, attackercountry, itera=1)
            return attackerarmies, defenderarmies
        else:
            attackerresult, defenderresult = dice.simulate(int(attackerarmies), int(defenderarmies)+1)
            if defenderresult <= 0:

                self.game_board.update_owner(defendercountry["id"], self.game_board.get_country_owner(attackercountry["id"]))
                self.client.send_message(f"sco: {defenderid} {str(self.game_board.get_country_owner(attackerid)+1)}\n")
                self.game_board.update_army_count(defendercountry["id"], attackerresult-1)
                self.client.send_message(f"sca: {defenderid} {attackerresult}\n")
                self.game_board.update_army_count(attackercountry["id"], 0)
                self.client.send_message(f"sca: {attackerid} 0\n")
                self.game_board.select_country(defendercountry["id"])
                self.client.send_message(f"sc: {defenderid}\n")
            else:
                print(defenderresult)
                self.game_board.update_army_count(defendercountry["id"], defenderresult-1)
                self.client.send_message(f"sca: {defenderid} {defenderresult}\n")
                self.game_board.update_army_count(attackercountry["id"], attackerresult)
                self.client.send_message(f"sca: {attackerid} {attackerresult}\n")
            return attackerresult, defenderresult