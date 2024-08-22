from PyQt6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QPixmap, QPolygon, QPolygonF, QPainterPath, QRegion, QPen, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QPointF, QTimer, QRectF, QRect, QTime, pyqtSignal
import xml.etree.ElementTree as ET
import random
import json
import os
import sys

cwd = os.path.dirname(os.path.abspath(sys.argv[0]))

class GameBoardWidget(QWidget):
    attack_country = pyqtSignal(dict, dict)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.country_colors = {}  
        self.board_data = None
        self.background = None
        self.colors = []
        self.show_continents = False
        self.foreground = None
        self.overground = None
        self.winner = "QWERTZ"
        self.quote = "Take my hand, we'll make it, I swear Oh-oh, livin' on a Luxer"
        self.load_explosion_animations()
        self.continents = []
        self.conquered_continents = {}  # {continent_name: (conquer_time, opacity, conqueror)}
        self.fade_timer = QTimer(self)
        self.fade_timer.timeout.connect(self.update_fade)
        self.fade_timer.start(50)  # Update every 50ms
        self.countries = []
        self.selected_country = -1
        self.pulse_timer = QTimer(self)
        self.pulse_timer.timeout.connect(self.pulse_selected_country)
        self.pulse_brightness = 1.0
        self.pulse_direction = -0.1
        self.newly_conquered = {}
        # Load army backgrounds
        self.army_bg_low = QPixmap(f"{cwd}/assets/bubbleSource1.png")
        self.army_bg_medium = QPixmap(f"{cwd}/assets/bubbleSource3.png")
        self.army_bg_high = QPixmap(f"{cwd}/assets/bubbleSource5.png")

        # Load army sprites
        self.army_sprite_1to4 = QPixmap(f"{cwd}/assets/guybw1.png")
        self.army_sprite_5to9 = QPixmap(f"{cwd}/assets/guybw2.png")
        self.army_sprite_10to19 = QPixmap(f"{cwd}/assets/guybw3.png")
        self.army_sprite_20plus = QPixmap(f"{cwd}/assets/guybw4.png")

    def load_explosion_animations(self):
        self.explosions = []
        explosion_types = [('black',26), ("explosion1", 15), ("explosion2", 20), ("flash", 19), ("greenblack4", 11), ("purple", 26), ("redblack2", 26)]  # 6 different explosion types
        for i, a in explosion_types:  # 6 different explosion types
            animation = []
            for j in range(0, a):  # 15 frames per explosion
                if j < 10:
                    x = f"0{str(j)}"
                else:
                    x = str(j)
                for y in range(3):
                    frame = QPixmap(f"{cwd}/assets/explosions/{i}/{i}_{x}.png")
                    animation.append(frame)
            self.explosions.append(animation)

    def parse_point(self, point_string):
        x, y = map(float, point_string.split(','))
        return QPointF(x, self.boardheight - y)  # Flip the y-coordinate
    
    def load_board(self, board_file):
        tree = ET.parse(board_file)
        self.board_data = None
        self.board_data = tree.getroot()
        self.load_board_master()

    def load_board_from_str(self, boardstr):
        self.board_data = None
        self.board_data = ET.fromstring(boardstr)
        self.load_board_master()

    def load_board_master(self):
        # Load images
        theme = self.board_data.find('theme').text
        self.boardheight = int(self.board_data.find('height').text)
        self.boardwidth = int(self.board_data.find('width').text)
        self.background = QPixmap(f"{cwd}/themes/{theme}/background")
        if os.path.exists(f"{cwd}/themes/{theme}/foreground.png"):
            self.foreground = QPixmap(f"{cwd}/themes/{theme}/foreground")
        else:
            self.foreground = QPixmap(f"{cwd}/assets/foreground")
        self.overground = QPixmap(f"{cwd}/themes/{theme}/overground")
        self.continents = []
        # Parse continents and countries
        for continent in self.board_data.findall('.//continent'):
            continent_data = {
                'name': continent.find('continentname').text,
                'bonus': int(continent.find('bonus').text),
                'color': "ff00ff",
                'labellocation': QPointF(0,0),
                'countries': []
            }
            try:
                continent_data['color'] = self.parse_color(continent.find('color').text)
            except:
                pass
            try:
                continent_data['labellocation'] = self.parse_point(continent.find('labellocation').text)
            except:
                pass
            for country in continent.findall('country'):
                country_data = {
                    'id': int(country.find('id').text),
                    'name': "SuperCountry",
                    'polygons': self.parse_polygons(country.findall('polygon')),
                    'armylocation': QPointF(0,0),
                    'armies': 0  # Initialize with 0 armies
                }
                try:
                    country_data['name'] = country.find('name').text
                except:
                    pass
                try:
                    country_data['armylocation'] = self.parse_point(country.find('armylocation').text)
                except:
                    pass
                continent_data['countries'].append(country_data)
            
            self.continents.append(continent_data)
        colors = self.colors
        
        for continent in self.continents:
            for country in continent['countries']:
                a = random.randint(0, len(colors)-1)
                self.country_colors[country['id']] = colors[a]

        self.update()
        for continent in self.continents:
            for country in continent['countries']:
                country['original_polygons'] = country['polygons'].copy()
                country['original_armylocation'] = country['armylocation']

            continent['original_labellocation'] = continent['labellocation']

        self.scale_board()
    def parse_color(self, color_string):
        r, g, b = map(float, color_string.split('/'))
        return QColor.fromRgbF(r, g, b)

    def parse_polygon(self, polygon_string):
        points = []
        max_y = float('-inf')
        min_y = float('inf')
        for point in polygon_string.split():
            x, y = map(float, point.split(','))
            max_y = max(max_y, y)
            min_y = min(min_y, y)
            points.append(QPointF(x, y))
        
        # Flip the points vertically
        flipped_points = []
        for point in points:
            flipped_y = self.boardheight - point.y()
            flipped_points.append(QPointF(point.x(), flipped_y))
        
        return flipped_points
    def parse_polygons(self,polygons):
        polygonlist = []
        for polygon in polygons:
            polygonlist.append(self.parse_polygon(polygon.text))
        return polygonlist
    def paintEvent(self, event):
        if not self.continents:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.black)
        # Draw scaled background
        if self.scaled_background and not self.scaled_background.isNull():
            painter.drawPixmap(self.rect(), self.scaled_background)

        # Draw countries
        country_region = QRegion()
        colors = set()
        for continent in self.continents:
            for country in continent['countries']:
                path = QPainterPath()
                polygons = country['polygons']
                for polygon in polygons:
                    if polygon:
                        path.moveTo(polygon[0])
                        for point in polygon[1:]:
                            path.lineTo(point)
                        path.closeSubpath()
                self.update()
                if self.show_continents:
                    color = continent['color']
                else:
                    color = self.country_colors.get(country['id'], Qt.GlobalColor.white)

                colors.add(color.rgb())  # Add color to set
                if country["id"] == self.selected_country:
                    color = color.lighter(int(self.pulse_brightness * 100))
                painter.fillPath(path, color)
                border_color = QColor(continent["color"])
                border_pen = QPen(border_color)
                border_pen.setWidth(4)  # Set the width to 2 pixels (adjust as needed)

                # Set the pen and draw the border
                painter.setPen(border_pen)
                painter.drawPath(path)
                country_region += QRegion(path.toFillPolygon().toPolygon())
        if self.show_continents:
            for continent in self.continents:
                label_pos = continent['labellocation']
                
                # Create a semi-transparent overlay for the box
                overlay = QColor(continent['color'])
                overlay.setAlpha(170)
                
                # Calculate box size based on text
                font = QFont()
                font.setPointSize(10)
                fm = QFontMetrics(font)
                text = f"{continent['name']}\nBonus: {continent['bonus']}"
                text_rect = fm.boundingRect(QRect(0, 0, 1000, 1000), Qt.TextFlag.TextWordWrap, text)
                box_width = text_rect.width() + 20  # Add some padding
                box_height = text_rect.height() + 20
                
                # Create the box rect
                box_rect = QRectF(label_pos.x() - box_width/2, label_pos.y() - box_height/2, box_width, box_height)
                
                # Draw the semi-transparent box
                painter.fillRect(box_rect, overlay)
                
                # Draw border
                pen = QPen(Qt.GlobalColor.black, 2)
                painter.setPen(pen)
                painter.drawRect(box_rect)
                
                # Draw text
                painter.setFont(font)
                painter.setPen(Qt.GlobalColor.white)
                painter.drawText(box_rect, Qt.AlignmentFlag.AlignCenter, text)

        # Draw scaled foreground
        if self.scaled_foreground and not self.scaled_foreground.isNull():
            painter.setClipRegion(country_region)
            painter.setOpacity(0.3)
            painter.drawPixmap(self.rect(), self.scaled_foreground)
            painter.setClipRegion(QRegion())
            painter.setOpacity(1.0)
        del painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Draw overground (if needed)
        if self.scaled_overground and not self.scaled_overground.isNull():

            painter.drawPixmap(self.rect(), self.scaled_overground)
        painter.setFont(QFont('Arial', 16))
        current_time = QTime.currentTime()
        army_image = QPixmap(f"{cwd}/assets/army.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        painter.setFont(QFont('Arial', 10))


        # Draw army counts, backgrounds, and sprites
        for continent in self.continents:
            for country in continent['countries']:
                if int(country.get('armies', 0)) > 0:
                    armylocation_pos = country.get('armylocation', QPointF(0, 0))
                    
                    # Select background based on army count
                    if int(country['armies']) < 10:
                        bg = self.army_bg_low
                    elif int(country['armies']) < 100:
                        bg = self.army_bg_medium
                    else:
                        bg = self.army_bg_high

                    # Select sprite based on army count
                    if int(country['armies']) < 5:
                        sprite = self.army_sprite_1to4
                    elif int(country['armies']) < 10:
                        sprite = self.army_sprite_5to9
                    elif int(country['armies']) < 20:
                        sprite = self.army_sprite_10to19
                    else:
                        sprite = self.army_sprite_20plus

                    #if ### TODO: - BEI 3 SOLDATENVISIBLE MUSS BUBBEL NACH LINKS
                    # Draw sprite (army icon)
                    painter.drawPixmap(QPointF(armylocation_pos.x()-30,armylocation_pos.y()-20), sprite)

                    # Draw background (bubble)
                    painter.drawPixmap(QPointF(armylocation_pos.x()-10,armylocation_pos.y()-10), bg)

                    # Draw army count
                    painter.setFont(QFont('Arial', 10))
                    painter.setPen(Qt.GlobalColor.black)
                    text_rect = QRectF(armylocation_pos.x()-10,armylocation_pos.y()-10, bg.width(), bg.height())
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(int(country['armies'])))

        for continent, (conquer_time, opacity,conqueror) in list(self.newly_conquered.items()):
            # Only draw if conquered less than 2 seconds ago
            if conquer_time.msecsTo(current_time) <= 2000:
                label_pos = next((c['labellocation'] for c in self.continents if c['name'] == continent), None)
                if label_pos:
                    bonus = next((c['bonus'] for c in self.continents if c['name'] == continent), None)
                    text = f"{continent}: {bonus}"
                    
                    # Calculate text dimensions
                    fm = painter.fontMetrics()
                    text_width = fm.horizontalAdvance(text)
                    text_height = fm.height()
                    
                    # Adjust label position to center the text
                    centered_x = label_pos.x() - text_width / 2
                    centered_y = label_pos.y() - text_height / 2
                    
                    painter.setPen(QPen(QColor(255, 255, 255, int(255 * opacity))))
                    painter.drawText(QPointF(centered_x, centered_y), text)
        # Check if all countries have the same color
        if len(colors) == 1:
            winning_color = QColor(list(colors)[0])
            
            # Calculate the size and position of the message box
            box_width = self.width() * 0.6  # 60% of widget width
            box_height = self.height() * 0.4  # 40% of widget height
            box_x = (self.width() - box_width) / 2
            box_y = (self.height() - box_height) / 2
            box_rect = QRectF(box_x, box_y, box_width, box_height)
            
            # Create a semi-transparent overlay for the box
            overlay = QColor(winning_color)
            overlay.setAlpha(128)  # 50% transparency
            
            # Draw the semi-transparent box
            painter.fillRect(box_rect, overlay)
            
            # Draw border
            pen = QPen(winning_color, 5)
            painter.setPen(pen)
            painter.drawRect(box_rect)
            
            # Draw text
            font = QFont()
            font.setPointSize(18)  # Adjust font size as needed
            painter.setFont(font)
            painter.setPen(Qt.GlobalColor.black)
            
            text = f'{self.winner} wins!\n"{self.quote}"'
            painter.drawText(box_rect, Qt.AlignmentFlag.AlignCenter, text)
        for continent in self.continents:
            for country in continent['countries']:
                if 'explosion' in country:
                    explosion = country['explosion']
                    frame = explosion['frames'][explosion['current_frame']]
                    painter.drawPixmap(explosion['position'], frame)
                    
                    # Move to next frame
                    explosion['current_frame'] += 1
                    if explosion['current_frame'] >= len(explosion['frames']):
                        del country['explosion']
                    
        self.update()
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scale_board()

    def scale_board(self):
        if not self.board_data:
            return

        # Calculate scale factors
        if not self.background.isNull():
            original_width = self.background.width()
            original_height = self.background.height()
            self.scale_x = self.width() / original_width
            self.scale_y = self.height() / original_height
        elif not self.foreground.isNull():
            original_width = self.foreground.width()
            original_height = self.foreground.height()
            self.scale_x = self.width() / original_width
            self.scale_y = self.height() / original_height
        elif not self.overground.isNull():
            original_width = self.overground.width()
            original_height = self.overground.height()
            self.scale_x = self.width() / original_width
            self.scale_y = self.height() / original_height
        else:
            original_width = 1000
            original_height = 600
            self.scale_x = self.width() / original_width
            self.scale_y = self.height() / original_height

        # Scale background, foreground, and overground
        if not self.background.isNull():
            self.scaled_background = self.background.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)#
        else:
            self.scaled_background = QPixmap()
        if not self.foreground.isNull():
            self.scaled_foreground = self.foreground.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        else:
            self.scaled_foreground = QPixmap()
        if not self.overground.isNull():
            self.scaled_overground = self.overground.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        else:
            self.scaled_overground = QPixmap()
        # Scale country polygons
        for continent in self.continents:
            for country in continent['countries']:
                scaled_polygon = []
                polygonlist = []
                for polygon in country['original_polygons']:
                    for point in polygon:
                        scaled_x = point.x() * self.scale_x
                        scaled_y = point.y() * self.scale_y
                        scaled_polygon.append(QPointF(scaled_x, scaled_y))
                    polygonlist.append(scaled_polygon)
                country['polygons'] = polygonlist
                if 'original_armylocation' not in country:
                    country['original_armylocation'] = country['armylocation']
                country['armylocation'] = QPointF(
                country['original_armylocation'].x() * self.scale_x,
                country['original_armylocation'].y() * self.scale_y
                )
            if 'original_labellocation' not in continent:
                continent['original_labellocation'] = continent['labellocation']
            
            continent['labellocation'] = QPointF(
                continent['original_labellocation'].x() * self.scale_x,
                continent['original_labellocation'].y() * self.scale_y
            )
        self.update()
    def pulse_selected_country(self):
        self.pulse_brightness += self.pulse_direction
        if self.pulse_brightness <= 0.7 or self.pulse_brightness >= 1.3:
            self.pulse_direction *= -1
        self.update()
    def check_continent_conquest(self):
        self.newly_conquered = {}
        for continent in self.continents:
            first_country_color = None
            continent_conquered = True
            for country in continent['countries']:
                color = self.country_colors.get(country['id'])
                if first_country_color is None:
                    first_country_color = color
                elif color != first_country_color:
                    continent_conquered = False
                    break
            current_time = QTime.currentTime() 
            if continent_conquered:
                for cont, (conquer_time, opacity, conqueror) in list(self.conquered_continents.items()):
                    if conqueror not in self.conquered_continents[cont] or cont not in self.conquered_continents:
                        self.newly_conquered[continent['name']] = (current_time, 1.0, first_country_color)
                if not continent["name"] in self.conquered_continents:
                    self.newly_conquered[continent['name']] = (current_time, 1.0, first_country_color)

            else:
                try:
                    del self.conquered_continents[continent['name']]
                except:
                    pass
        # Update conquered_continents with only the newly conquered ones
        current_time = QTime.currentTime()
        for continent in self.newly_conquered:
            self.conquered_continents[continent] = (current_time, 1.0, first_country_color)

    def update_fade(self):
        current_time = QTime.currentTime()
        for continent, (conquer_time, opacity, conqueror) in list(self.conquered_continents.items()):
            elapsed = conquer_time.msecsTo(current_time)
            if elapsed > 2000:  # 2 seconds
                try:
                    del self.newly_conquered[continent]
                except:
                    pass
            else:
                new_opacity = 1.0 - (elapsed / 2000)  # Linear fade
                self.conquered_continents[continent] = (conquer_time, new_opacity, conqueror)
        self.update()
    def select_country(self, countryid):
        if not str(countryid) == "-1":
            for continent in self.continents:
                for country in continent['countries']:
                    if str(country['id']) == str(countryid):
                        # Select the new country
                        self.pulse_timer.start(50)
                        self.selected_country = country["id"]
                        break
        else:
            self.selected_country = -1
            self.pulse_timer.stop()
    def mousePressEvent(self, event):
        click_point = event.position()
        
        for continent in self.continents:
            for country in continent['countries']:
                path = QPainterPath()
                for polygon in country['polygons']:
                    if polygon:
                        path.moveTo(polygon[0])
                        for point in polygon[1:]:
                            path.lineTo(point)
                        path.closeSubpath()
                
                if path.contains(click_point):
                    print(self.selected_country )
                    if self.selected_country == -1:
                        # First country selection
                        self.select_country(country["id"])

                    elif self.selected_country == country["id"]:
                        # Deselect if clicking the same country
                        self.select_country(-1)

                    else:
                        # Clicking a different country while one is selected
                        acountry = {}
                        for continent in self.continents:
                            for xcountry in continent['countries']:
                                if str(xcountry['id']) == str(self.selected_country):
                                    acountry = xcountry
                        self.attack_country.emit(country,acountry)
                    self.update()
                    return
    def update_owner(self, countryid, owner):
        supercountry = {"id":"placeholder","name":"placeholder"}
        for continent in self.continents:
            for country in continent['countries']:
                if str(country['id']) == str(countryid):
                    supercountry = country
                    break
        new_color = self.colors[int(owner)]
        self.country_colors[supercountry['id']] = new_color
        self.check_continent_conquest()
        self.update()

    def update_army_count(self, country_id, count):
        for continent in self.continents:
            for country in continent['countries']:
                if str(country['id']) == str(country_id):
                    country['armies'] = count
                    self.update()
                    return
                
    def trigger_explosion(self, countryid):
        for continent in self.continents:
            for scountry in continent['countries']:
                if str(scountry['id']) == str(countryid):
                    country = scountry
        explosion_type = random.randint(0, len(self.explosions)-1)
        explosion_frames = self.explosions[explosion_type]
        
        # Get a random position within the country
        path = QPainterPath()
        for polygon in country['polygons']:
            if polygon:
                path.moveTo(polygon[0])
                for point in polygon[1:]:
                    path.lineTo(point)
                path.closeSubpath()
        
        bbox = path.boundingRect()
        
        x = random.uniform(bbox.center().x()-(bbox.center().x()-bbox.left())/5, bbox.center().x()+(bbox.right()-bbox.center().x())/5)-self.scale_x*40
        y = random.uniform(bbox.center().y()-(bbox.center().y()-bbox.top())/5, bbox.center().y()+(bbox.bottom()-bbox.center().y())/5)-self.scale_y*40
        
        country['explosion'] = {
            'frames': explosion_frames,
            'current_frame': 0,
            'position': QPointF(x, y)
        }
    def get_country_owner(self, countryid):
        for continent in self.continents:
            for country in continent['countries']:
                if str(country['id']) == str(countryid):
                    # The country color corresponds to the owner
                    color = self.country_colors.get(country['id'])
                    if color:
                        # Map the color to an owner number (1 to 5)
                        for i, player_color in enumerate(self.colors):
                            if color == player_color:
                                return i 
        # If the country is not found or has no owner
        return -1

    def mouseReleaseEvent(self, event):
        # Handle end of drag operations, attacks, etc.
        pass