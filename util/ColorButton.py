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

from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QAction, QColor, QPainter, QBrush, QPen
from PyQt6.QtCore import QRect, QMetaObject
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QGroupBox, QLineEdit, QComboBox, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QMenuBar, QMenu, QGridLayout, QApplication, QColorDialog


class ColorButton(QPushButton):
    def __init__(self, color=QColor("white"), parent=None):
        super().__init__(parent)
        self.setFixedSize(70, 20)  # We'll adjust this size later
        self.color = color
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color.name()};
                border: 2px solid gray;
            }}
            """
        )

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(QColor("white"), 3))
        painter.drawRect(3, 3, self.width() - 6, self.height() - 6)

    def set_color(self, color):
        self.color = color
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color.name()};
                border: 2px solid gray;
            }}
            """
        )
        self.update()
    def getcolor(self):
        return self.color