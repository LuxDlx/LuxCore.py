from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QAction, QColor
from PyQt6.QtCore import QRect, QMetaObject, qInstallMessageHandler
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QGroupBox, QLineEdit, QComboBox, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QMenuBar, QMenu, QGridLayout, QApplication, QColorDialog
import util.utils as utils
from util.ColorButton import ColorButton
from util.GameWindow import GameWindow
import os
import sys
import json
import webbrowser

cwd = os.path.dirname(os.path.abspath(sys.argv[0]))

qInstallMessageHandler(utils.qt_message_handler) # Comment out this line for debugging

if not os.path.exists(f"{cwd}/cache/config.json"):
    with open(f"{cwd}/cache/config.json","w") as f:
        json.dump({"Username": "YOUR_NAME", "RegKey": "YOUR_REGKEY", "Language":"en"}, f)

class LuxCore(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("LuxCore.py")
        self.setWindowTitle("LuxCore.py: The Game of Universal Domination")
        self.setFixedSize(600,430)
        self.font_id = QFontDatabase.addApplicationFont(f"{cwd}/assets/DirtyHeadline.ttf")
        font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.groupBoxFont = QFont(font_family)
        self.groupBoxFont.setPointSize(20)
        self.buttonFont = QFont(font_family)
        self.buttonFont.setPointSize(25)
        self.defaultFont = QFont("Calibri")
        self.defaultFont.setPointSize(10)
        self.chatFont = QFont("Calibri")
        self.chatFont.setPointSize(15)
        self.chatFont.setBold(True)
        self.smallChatFont = QFont("Calibri")
        self.smallChatFont.setPointSize(12)
        self.smallChatFont.setBold(True)

        ### USE_IN_PROD
        with open(f"{cwd}/cache/config.json","r") as f:
            a = json.load(f)
        self.username = a["Username"]
        lang = a["Language"]
        self.regcode = a["RegKey"]

        ### DO_NOT_USE_IN_PROD
        self.botlist = ["Angry", "Communist", "Reaper", "BotOfDoom"]
        ### END

        self.lang = lang
        self.centralwidget = QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QLabel(parent=self.centralwidget)
        self.label.setGeometry(QRect(0, -10, 221, 161))
        self.label.setText("")
        self.label.setPixmap(QPixmap("assets/LuxDeluxLogo.png"))
        self.label.setObjectName("label")
        
        self.label_2 = QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QRect(130, 140, 81, 21))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Sillysoft.net")   
        
        self.PlayerGroupBox = QGroupBox(parent=self.centralwidget)
        self.PlayerGroupBox.setGeometry(QRect(9, 165, 281, 211))
        self.PlayerGroupBox.setStyleSheet("")
        self.PlayerGroupBox.setObjectName("groupBox")
        self.PlayerGroupBox.setFont(self.groupBoxFont)
        self.PlayerGroupBox.setTitle(utils.get_locales(lang,"ChooseTheCombatants"))
        
        self.gridLayoutWidget = QWidget(parent=self.PlayerGroupBox)
        self.gridLayoutWidget.setGeometry(QRect(10, 30, 261, 181))
        self.gridLayoutWidget.setFont(self.defaultFont)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.color_buttons = []
        self.lineedits = []
        self.comboboxes = []
        for i in range(6):
            color_button = ColorButton(parent=self.gridLayoutWidget)
            color_button.clicked.connect(lambda checked, btn=color_button: self.open_color_dialog(btn))
            self.gridLayout_2.addWidget(color_button, i, 0, 1, 1)
            self.color_buttons.append(color_button)

            line_user = QLineEdit(parent=self.gridLayoutWidget)
            line_user.setObjectName(f"lineUser{i+1}")
            line_user.setText("Username")
            self.gridLayout_2.addWidget(line_user, i, 1, 1, 1)
            self.lineedits.append(line_user)

            combo_box = QComboBox(parent=self.gridLayoutWidget)
            combo_box.setObjectName(f"comboBox_{i+4}")
            combo_box.addItem(utils.get_locales(lang,"Human"), "Human")
            combo_box.addItem(utils.get_locales(lang,"random"), "random")
            combo_box.addItem(utils.get_locales(lang,"noplayer"), "noplayer")
            for bot in self.botlist:
                combo_box.addItem(bot,bot)
            self.gridLayout_2.addWidget(combo_box, i, 2, 1, 1)
            self.comboboxes.append(combo_box)

        self.pushButton = QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QRect(320, 350, 241, 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText(utils.get_locales(lang,"PlayAGame"))
        self.pushButton.clicked.connect(self.start_game)

        self.NetworkGroupBox = QGroupBox(parent=self.centralwidget)
        self.NetworkGroupBox.setGeometry(QRect(300, 165, 281, 171))
        self.NetworkGroupBox.setStyleSheet("")
        self.NetworkGroupBox.setObjectName("groupBox_2")
        self.NetworkGroupBox.setFont(self.groupBoxFont)
        self.NetworkGroupBox.setTitle(utils.get_locales(lang,"NetworkOptions"))
        
        self.verticalLayoutWidget = QWidget(parent=self.NetworkGroupBox)
        self.verticalLayoutWidget.setFont(self.defaultFont)
        self.verticalLayoutWidget.setGeometry(QRect(10, 30, 261, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.pushButton_2 = QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText(utils.get_locales(lang,"ShowNetworkGames"))
        self.verticalLayout.addWidget(self.pushButton_2)
        
        self.checkBox = QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setText(utils.get_locales(lang,"AllowNetworkPlayers"))
        self.verticalLayout.addWidget(self.checkBox)
        
        self.checkBox_2 = QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setText(utils.get_locales(lang,"InternetPublic"))
        self.verticalLayout.addWidget(self.checkBox_2)
        
        self.checkBox_3 = QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.setText(utils.get_locales(lang,"Fullscreen"))
        self.verticalLayout.addWidget(self.checkBox_3)
        
        self.pushButton_3 = QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText(utils.get_locales(lang,"MoreOptions"))
        self.verticalLayout.addWidget(self.pushButton_3)
        
        self.MapGroupBox = QGroupBox(parent=self.centralwidget)
        self.MapGroupBox.setGeometry(QRect(220, -4, 361, 175))
        self.MapGroupBox.setStyleSheet("")
        self.MapGroupBox.setObjectName("groupBox_3")
        self.MapGroupBox.setFont(self.groupBoxFont)
        # Set the stylesheet for the QGroupBox

        self.MapGroupBox.setTitle(utils.get_locales(lang,"ChooseTheWorld"))
        
        self.horizontalLayoutWidget = QWidget(parent=self.MapGroupBox)
        self.horizontalLayoutWidget.setGeometry(QRect(9, 30, 351, 141))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.MapComboBox = QComboBox(parent=self.horizontalLayoutWidget)
        self.MapComboBox.setFont(self.defaultFont)
        self.MapComboBox.setObjectName("comboBox")
        for map in os.scandir(f"{cwd}/maps"):
            if map.is_file() and map.name.endswith(".luxb"):
                self.MapComboBox.addItem(map.name.replace(".luxb",""))
        self.MapComboBox.currentTextChanged.connect(self.writeCache)
        self.verticalLayout_2.addWidget(self.MapComboBox)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton_4 = QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("<-")
        self.pushButton_4.setFont(self.defaultFont)
        self.horizontalLayout_2.addWidget(self.pushButton_4)

        self.pushButton_6 = QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setText("Plugins")
        self.pushButton_6.setFont(self.defaultFont)
        self.horizontalLayout_2.addWidget(self.pushButton_6)

        self.pushButton_5 = QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setText("->")
        self.pushButton_5.setFont(self.defaultFont)
        self.horizontalLayout_2.addWidget(self.pushButton_5)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.label_4 = QLabel(parent=self.horizontalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(self.defaultFont)
        self.label_4.setText(utils.get_locales(lang,"StartingPosition"))
        self.verticalLayout_2.addWidget(self.label_4)

        # Move the existing comboBox_2 setup after the label_4
        self.comboBox_2 = QComboBox(parent=self.horizontalLayoutWidget)
        self.comboBox_2.setFont(self.defaultFont)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("Map Starting Scene")
        self.comboBox_2.addItem("Random Countries / Equal Armies")
        self.comboBox_2.addItem("Random Countries / Place Armies")
        self.comboBox_2.addItem("Random Countries / Random Armies")
        self.comboBox_2.addItem("Select Countries / Equal Armies")
        self.comboBox_2.addItem("Select Countries / Place Armies")
        self.comboBox_2.addItem("Select Countries / Random Armies")
        self.verticalLayout_2.addWidget(self.comboBox_2)
        self.comboBox_3 = QComboBox(parent=self.horizontalLayoutWidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.setFont(self.defaultFont)
        self.comboBox_3.addItem("Biohazard - off")
        self.comboBox_3.addItem("Biohazard - light")
        self.comboBox_3.addItem("Biohazard - medium")
        self.comboBox_3.addItem("Biohazard - hard")
        self.comboBox_3.addItem("Biohazard - crisp")
        self.comboBox_3.addItem("Biohazard - extreme")
        self.verticalLayout_2.addWidget(self.comboBox_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        
        self.label_3 = QLabel(parent=self.horizontalLayoutWidget)
        self.label_3.setText("")
        self.label_3.setPixmap(QPixmap("assets/not_available.jpg"))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        
        self.setCentralWidget(self.centralwidget)
        
        self.menubar = QMenuBar(parent=self)
        self.menubar.setGeometry(QRect(0, 0, 594, 22))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle(utils.get_locales(lang,"File"))
        
        self.menuOnline = QMenu(self.menubar)
        self.menuOnline.setObjectName("menuOnline")
        self.menuOnline.setTitle(utils.get_locales(lang,"Online"))
        
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.setTitle(utils.get_locales(lang,"Help"))
        
        self.setMenuBar(self.menubar)
        
        self.actionChangeRegistry = QAction(self)
        self.actionChangeRegistry.setObjectName("actionChangeRegistry")
        self.actionChangeRegistry.setText("ChangeRegistry")
        

        
        self.actionSillysoftGames = QAction(self)
        self.actionSillysoftGames.setObjectName("actionSillysoftGames")
        self.actionSillysoftGames.setText("Sillysoft Games")
        
        self.actionForum = QAction(self)
        self.actionForum.setObjectName("actionForum")
        self.actionForum.setText(utils.get_locales(lang,"UserForums"))
        
        self.actionDocs = QAction(self)
        self.actionDocs.setObjectName("actionDocs")
        self.actionDocs.setText("Lux " + utils.get_locales(lang,"Documentation"))
        
        self.actionRankings_2 = QAction(self)
        self.actionRankings_2.setObjectName("actionRankings_2")
        self.actionRankings_2.setText(utils.get_locales(lang,"WorldWideRankings"))
        
        self.actionReportBug = QAction(self)
        self.actionReportBug.setObjectName("actionReportBug")
        self.actionReportBug.setText(utils.get_locales(lang,"ReportABug"))
        
        self.actionSuggestion = QAction(self)
        self.actionSuggestion.setObjectName("actionSuggestion")
        self.actionSuggestion.setText(utils.get_locales(lang,"RequestAFeature"))
        
        self.actionMakeOwnMap = QAction(self)
        self.actionMakeOwnMap.setObjectName("actionMakeOwnMap")
        self.actionMakeOwnMap.setText(utils.get_locales(lang,"MakeYourOwnMap"))
        
        self.actionMakeOwnAI = QAction(self)
        self.actionMakeOwnAI.setObjectName("actionMakeOwnAI")
        self.actionMakeOwnAI.setText(utils.get_locales(lang,"CodeYourOwnAI"))
        
        self.actionAboutLux = QAction(self)
        self.actionAboutLux.setObjectName("actionAboutLux")
        self.actionAboutLux.setText(utils.get_locales(lang,"AboutLux"))
        
        self.actionRules = QAction(self)
        self.actionRules.setObjectName("actionRules")
        self.actionRules.setText(utils.get_locales(lang,"TheRulesOfLux"))
        
        self.actionTutorial = QAction(self)
        self.actionTutorial.setObjectName("actionTutorial")
        self.actionTutorial.setText(utils.get_locales(lang,"LuxGuide"))
        
        self.actionShortcuts = QAction(self)
        self.actionShortcuts.setObjectName("actionShortcuts")
        self.actionShortcuts.setText(utils.get_locales(lang,"KeyboardShortcuts"))
        
        self.actionHostingTips = QAction(self)
        self.actionHostingTips.setObjectName("actionHostingTips")
        self.actionHostingTips.setText(utils.get_locales(lang,"HostingTips"))
        
        self.actionChangelog = QAction(self)
        self.actionChangelog.setObjectName("actionChangelog")
        self.actionChangelog.setText(utils.get_locales(lang,"Changelog"))
        
        self.actionNewGame = QAction(parent=self)
        self.actionNewGame.setObjectName("actionNewGame")
        self.actionNewGame.setText(utils.get_locales(lang,"NewGame"))

        self.actionLoadSavedGame = QAction(parent=self)
        self.actionLoadSavedGame.setObjectName("actionLoadSavedGame")
        self.actionLoadSavedGame.setText(utils.get_locales(lang,"OpenSavedGame"))

        self.actionSearchNetworkGame = QAction(parent=self)
        self.actionSearchNetworkGame.setObjectName("actionSearchNetworkGame")
        self.actionSearchNetworkGame.setText(utils.get_locales(lang,"JoinNetworkGame"))

        self.actionPluginManager = QAction(parent=self)
        self.actionPluginManager.setObjectName("actionPluginManager")
        self.actionPluginManager.setText(utils.get_locales(lang,"PluginManager"))

        self.actionSettings = QAction(parent=self)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.setText(utils.get_locales(lang,"Preferences"))

        self.actionMapEditor = QAction(parent=self)
        self.actionMapEditor.setObjectName("actionMapEditor")
        self.actionMapEditor.setText(utils.get_locales(lang,"MapEditor"))

        self.actionSteamKey = QAction(self)
        self.actionSteamKey.setObjectName("actionClose")
        self.actionSteamKey.setText(utils.get_locales(lang,"GetSteamKey"))
        
        self.actionEndLux = QAction(self)
        self.actionEndLux.setObjectName("actionEndLux")
        self.actionEndLux.setText(utils.get_locales(lang,"ExitLux"))

        # Now add these actions to the File menu
        self.menuFile.addAction(self.actionNewGame)
        self.menuFile.addAction(self.actionLoadSavedGame)
        self.menuFile.addAction(self.actionSearchNetworkGame)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPluginManager)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionMapEditor)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSteamKey)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionEndLux)
        
        self.menuOnline.addAction(self.actionSillysoftGames)
        self.menuOnline.addAction(self.actionForum)
        self.menuOnline.addAction(self.actionDocs)
        self.menuOnline.addAction(self.actionRankings_2)
        self.menuOnline.addSeparator()
        self.menuOnline.addAction(self.actionReportBug)
        self.menuOnline.addAction(self.actionSuggestion)
        self.menuOnline.addSeparator()
        self.menuOnline.addAction(self.actionMakeOwnMap)
        self.menuOnline.addAction(self.actionMakeOwnAI)
        
        self.menuHelp.addAction(self.actionAboutLux)
        self.menuHelp.addAction(self.actionRules)
        self.menuHelp.addAction(self.actionTutorial)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionShortcuts)
        self.menuHelp.addAction(self.actionHostingTips)
        self.menuHelp.addAction(self.actionChangelog)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOnline.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        QMetaObject.connectSlotsByName(self)

        self.loadCache()
        self.actionNewGame.triggered.connect(self.start_game)
        #self.actionLoadSavedGame.triggered.connect(self.load_saved_game)
        #self.actionSearchNetworkGame.triggered.connect(self.search_network_game)
        #self.actionPluginManager.triggered.connect(self.open_plugin_manager)
        #self.actionSettings.triggered.connect(self.open_settings)
        #self.actionMapEditor.triggered.connect(self.open_map_editor)
        self.actionSteamKey.triggered.connect(lambda: webbrowser.open("https://sillysoft.net/contact/steamkey.php"))
        self.actionEndLux.triggered.connect(self.close)
        #self.actionAboutLux.triggered.connect(self.about_lux)
        self.actionRules.triggered.connect(lambda: webbrowser.open(f"{cwd}/docs/rules_{lang}.html") if os.path.exists(f"{cwd}/docs/rules_{lang}.html") else webbrowser.open(f"{cwd}/docs/rules.html"))
        #self.actionTutorial.triggered.connect(self.open_tutorial)
        #self.actionShortcuts.triggered.connect(self.open_shortcuts)
        #self.actionHostingTips.triggered.connect(self.open_hosting_tips)
        #self.actionChangelog.triggered.connect(self.open_changelog)
        #self.actionReportBug.triggered.connect(self.open_bug_report)
        #self.actionSuggestion.triggered.connect(self.open_suggestion)
        #self.actionMakeOwnMap.triggered.connect(self.open_make_own_map)
        #self.actionMakeOwnAI.triggered.connect(self.open_make_own_ai)
        #self.actionSillysoftGames.triggered.connect(self.open_sillysoft_games)
        #self.actionForum.triggered.connect(self.open_forum)
        #self.actionDocs.triggered.connect(self.open_docs)
        #self.actionRankings_2.triggered.connect(self.open_rankings)

    def open_color_dialog(self, button):
        color = QColorDialog.getColor(button.color, self, "Choose Color")
        if color.isValid():
            button.set_color(color)
            self.writeCache()

    def loadCache(self):
        with open(f"{cwd}/cache/cache.json", "r") as f:
            cache = json.load(f)
        i=0
        for player in cache["players"].keys():
            self.color_buttons[i].set_color(QColor(cache["players"][player]["color"]))
            self.lineedits[i].setText(cache["players"][player]["name"])
            self.comboboxes[i].setCurrentText(cache["players"][player]["AI"])
            i+=1
        self.MapComboBox.setCurrentText(cache["map"])
    def writeCache(self):
        with open(f"{cwd}/cache/cache.json", "r") as f:
            cache = json.load(f)
        i=0
        for button in self.color_buttons:
            cache["players"][str(i)]["color"] = button.color.rgb()
            cache["players"][str(i)]["name"] = self.lineedits[i].text()
            cache["players"][str(i)]["AI"] = self.comboboxes[i].currentData()
            i+=1
        cache["map"] = self.MapComboBox.currentText()
        with open(f"{cwd}/cache/cache.json", "w") as f:
            json.dump(cache, f, indent=4)
    def start_game(self):
        self.game_window = GameWindow(self)
        self.game_window.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = LuxCore()
    MainWindow.show()
    sys.exit(app.exec())