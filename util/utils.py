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

import os
import sys
import re
import io
import stat
import shutil
import time
from PyQt5.QtCore import QtMsgType
import util.LuxFilesGetter as LuxFilesGetter

cwd = os.path.dirname(os.path.abspath(sys.argv[0]))

JAR_FILE_DICT = {"bubbleSource1.png":"assets/bubbleSource1.png","bubbleSource3.png":"assets/bubbleSource3.png","bubbleSource5.png":"assets/bubbleSource5.png","Dirty Headline Custom Sillysoft.ttf":"assets/DirtyHeadline.ttf","guybw1.png":"assets/guybw1.png","guybw2.png":"assets/guybw2.png","guybw3.png":"assets/guybw3.png","guybw4.png":"assets/guybw4.png","LuxDeluxLogo.png":"assets/LuxDeluxLogo.png","not_available.jpg":"assets/not_available.jpg","texture_background.jpg":"assets/texture_background.jpg","texture_map.jpg":"assets/texture_map.jpg","texture_network.jpg":"assets/texture_network.jpg","texture_players.jpg":"assets/texture_players.jpg","black_00.png":"assets/explosions/black/black_00.png","black_01.png":"assets/explosions/black/black_01.png","black_02.png":"assets/explosions/black/black_02.png","black_03.png":"assets/explosions/black/black_03.png","black_04.png":"assets/explosions/black/black_04.png","black_05.png":"assets/explosions/black/black_05.png","black_06.png":"assets/explosions/black/black_06.png","black_07.png":"assets/explosions/black/black_07.png","black_08.png":"assets/explosions/black/black_08.png","black_09.png":"assets/explosions/black/black_09.png","black_10.png":"assets/explosions/black/black_10.png","black_11.png":"assets/explosions/black/black_11.png","black_12.png":"assets/explosions/black/black_12.png","black_13.png":"assets/explosions/black/black_13.png","black_14.png":"assets/explosions/black/black_14.png","black_15.png":"assets/explosions/black/black_15.png","black_16.png":"assets/explosions/black/black_16.png","black_17.png":"assets/explosions/black/black_17.png","black_18.png":"assets/explosions/black/black_18.png","black_19.png":"assets/explosions/black/black_19.png","black_20.png":"assets/explosions/black/black_20.png","black_21.png":"assets/explosions/black/black_21.png","black_22.png":"assets/explosions/black/black_22.png","black_23.png":"assets/explosions/black/black_23.png","black_24.png":"assets/explosions/black/black_24.png","black_25.png":"assets/explosions/black/black_25.png","black_26.png":"assets/explosions/black/black_26.png","explosion1_00.png":"assets/explosions/explosion1/explosion1_00.png","explosion1_01.png":"assets/explosions/explosion1/explosion1_01.png","explosion1_02.png":"assets/explosions/explosion1/explosion1_02.png","explosion1_03.png":"assets/explosions/explosion1/explosion1_03.png","explosion1_04.png":"assets/explosions/explosion1/explosion1_04.png","explosion1_05.png":"assets/explosions/explosion1/explosion1_05.png","explosion1_06.png":"assets/explosions/explosion1/explosion1_06.png","explosion1_07.png":"assets/explosions/explosion1/explosion1_07.png","explosion1_08.png":"assets/explosions/explosion1/explosion1_08.png","explosion1_09.png":"assets/explosions/explosion1/explosion1_09.png","explosion1_10.png":"assets/explosions/explosion1/explosion1_10.png","explosion1_11.png":"assets/explosions/explosion1/explosion1_11.png","explosion1_12.png":"assets/explosions/explosion1/explosion1_12.png","explosion1_13.png":"assets/explosions/explosion1/explosion1_13.png","explosion1_14.png":"assets/explosions/explosion1/explosion1_14.png","explosion1_15.png":"assets/explosions/explosion1/explosion1_15.png","explosion2_00.png":"assets/explosions/explosion2/explosion2_00.png","explosion2_01.png":"assets/explosions/explosion2/explosion2_01.png","explosion2_02.png":"assets/explosions/explosion2/explosion2_02.png","explosion2_03.png":"assets/explosions/explosion2/explosion2_03.png","explosion2_04.png":"assets/explosions/explosion2/explosion2_04.png","explosion2_05.png":"assets/explosions/explosion2/explosion2_05.png","explosion2_06.png":"assets/explosions/explosion2/explosion2_06.png","explosion2_07.png":"assets/explosions/explosion2/explosion2_07.png","explosion2_08.png":"assets/explosions/explosion2/explosion2_08.png","explosion2_09.png":"assets/explosions/explosion2/explosion2_09.png","explosion2_10.png":"assets/explosions/explosion2/explosion2_10.png","explosion2_11.png":"assets/explosions/explosion2/explosion2_11.png","explosion2_12.png":"assets/explosions/explosion2/explosion2_12.png","explosion2_13.png":"assets/explosions/explosion2/explosion2_13.png","explosion2_14.png":"assets/explosions/explosion2/explosion2_14.png","explosion2_15.png":"assets/explosions/explosion2/explosion2_15.png","explosion2_16.png":"assets/explosions/explosion2/explosion2_16.png","explosion2_17.png":"assets/explosions/explosion2/explosion2_17.png","explosion2_18.png":"assets/explosions/explosion2/explosion2_18.png","explosion2_19.png":"assets/explosions/explosion2/explosion2_19.png","explosion2_20.png":"assets/explosions/explosion2/explosion2_20.png","flash_00.png":"assets/explosions/flash/flash_00.png","flash_01.png":"assets/explosions/flash/flash_01.png","flash_02.png":"assets/explosions/flash/flash_02.png","flash_03.png":"assets/explosions/flash/flash_03.png","flash_04.png":"assets/explosions/flash/flash_04.png","flash_05.png":"assets/explosions/flash/flash_05.png","flash_06.png":"assets/explosions/flash/flash_06.png","flash_07.png":"assets/explosions/flash/flash_07.png","flash_08.png":"assets/explosions/flash/flash_08.png","flash_09.png":"assets/explosions/flash/flash_09.png","flash_10.png":"assets/explosions/flash/flash_10.png","flash_11.png":"assets/explosions/flash/flash_11.png","flash_12.png":"assets/explosions/flash/flash_12.png","flash_13.png":"assets/explosions/flash/flash_13.png","flash_14.png":"assets/explosions/flash/flash_14.png","flash_15.png":"assets/explosions/flash/flash_15.png","flash_16.png":"assets/explosions/flash/flash_16.png","flash_17.png":"assets/explosions/flash/flash_17.png","flash_18.png":"assets/explosions/flash/flash_18.png","flash_19.png":"assets/explosions/flash/flash_19.png","greenblack4_00.png":"assets/explosions/greenblack4/greenblack4_00.png","greenblack4_01.png":"assets/explosions/greenblack4/greenblack4_01.png","greenblack4_02.png":"assets/explosions/greenblack4/greenblack4_02.png","greenblack4_03.png":"assets/explosions/greenblack4/greenblack4_03.png","greenblack4_04.png":"assets/explosions/greenblack4/greenblack4_04.png","greenblack4_05.png":"assets/explosions/greenblack4/greenblack4_05.png","greenblack4_06.png":"assets/explosions/greenblack4/greenblack4_06.png","greenblack4_07.png":"assets/explosions/greenblack4/greenblack4_07.png","greenblack4_08.png":"assets/explosions/greenblack4/greenblack4_08.png","greenblack4_09.png":"assets/explosions/greenblack4/greenblack4_09.png","greenblack4_10.png":"assets/explosions/greenblack4/greenblack4_10.png","greenblack4_11.png":"assets/explosions/greenblack4/greenblack4_11.png","purple_00.png":"assets/explosions/purple/purple_00.png","purple_01.png":"assets/explosions/purple/purple_01.png","purple_02.png":"assets/explosions/purple/purple_02.png","purple_03.png":"assets/explosions/purple/purple_03.png","purple_04.png":"assets/explosions/purple/purple_04.png","purple_05.png":"assets/explosions/purple/purple_05.png","purple_06.png":"assets/explosions/purple/purple_06.png","purple_07.png":"assets/explosions/purple/purple_07.png","purple_08.png":"assets/explosions/purple/purple_08.png","purple_09.png":"assets/explosions/purple/purple_09.png","purple_10.png":"assets/explosions/purple/purple_10.png","purple_11.png":"assets/explosions/purple/purple_11.png","purple_12.png":"assets/explosions/purple/purple_12.png","purple_13.png":"assets/explosions/purple/purple_13.png","purple_14.png":"assets/explosions/purple/purple_14.png","purple_15.png":"assets/explosions/purple/purple_15.png","purple_16.png":"assets/explosions/purple/purple_16.png","purple_17.png":"assets/explosions/purple/purple_17.png","purple_18.png":"assets/explosions/purple/purple_18.png","purple_19.png":"assets/explosions/purple/purple_19.png","purple_20.png":"assets/explosions/purple/purple_20.png","purple_21.png":"assets/explosions/purple/purple_21.png","purple_22.png":"assets/explosions/purple/purple_22.png","purple_23.png":"assets/explosions/purple/purple_23.png","purple_24.png":"assets/explosions/purple/purple_24.png","purple_25.png":"assets/explosions/purple/purple_25.png","purple_26.png":"assets/explosions/purple/purple_26.png","redblack2_00.png":"assets/explosions/redblack2/redblack2_00.png","redblack2_01.png":"assets/explosions/redblack2/redblack2_01.png","redblack2_02.png":"assets/explosions/redblack2/redblack2_02.png","redblack2_03.png":"assets/explosions/redblack2/redblack2_03.png","redblack2_04.png":"assets/explosions/redblack2/redblack2_04.png","redblack2_05.png":"assets/explosions/redblack2/redblack2_05.png","redblack2_06.png":"assets/explosions/redblack2/redblack2_06.png","redblack2_07.png":"assets/explosions/redblack2/redblack2_07.png","redblack2_08.png":"assets/explosions/redblack2/redblack2_08.png","redblack2_09.png":"assets/explosions/redblack2/redblack2_09.png","redblack2_10.png":"assets/explosions/redblack2/redblack2_10.png","redblack2_11.png":"assets/explosions/redblack2/redblack2_11.png","redblack2_12.png":"assets/explosions/redblack2/redblack2_12.png","redblack2_13.png":"assets/explosions/redblack2/redblack2_13.png","redblack2_14.png":"assets/explosions/redblack2/redblack2_14.png","redblack2_15.png":"assets/explosions/redblack2/redblack2_15.png","redblack2_16.png":"assets/explosions/redblack2/redblack2_16.png","redblack2_17.png":"assets/explosions/redblack2/redblack2_17.png","redblack2_18.png":"assets/explosions/redblack2/redblack2_18.png","redblack2_19.png":"assets/explosions/redblack2/redblack2_19.png","redblack2_20.png":"assets/explosions/redblack2/redblack2_20.png","redblack2_21.png":"assets/explosions/redblack2/redblack2_21.png","redblack2_22.png":"assets/explosions/redblack2/redblack2_22.png","redblack2_23.png":"assets/explosions/redblack2/redblack2_23.png","redblack2_24.png":"assets/explosions/redblack2/redblack2_24.png","redblack2_25.png":"assets/explosions/redblack2/redblack2_25.png","redblack2_26.png":"assets/explosions/redblack2/redblack2_26.png","LuxBundle_cs.properties":"locales/cs.properties","LuxBundle_da.properties":"locales/da.properties","LuxBundle_de.properties":"locales/de.properties","LuxBundle_el.properties":"locales/el.properties","LuxBundle_en.properties":"locales/en.properties","LuxBundle_es.properties":"locales/es.properties","LuxBundle_et.properties":"locales/et.properties","LuxBundle_fi.properties":"locales/fi.properties","LuxBundle_fr.properties":"locales/fr.properties","LuxBundle_hr.properties":"locales/hr.properties","LuxBundle_it.properties":"locales/it.properties","LuxBundle_ja.properties":"locales/ja.properties","LuxBundle_ko.properties":"locales/ko.properties","LuxBundle_nl_BE.properties":"locales/nl_be.properties","LuxBundle_nl_NL.properties":"locales/nl_nl.properties","LuxBundle_pt_BR.properties":"locales/pt_br.properties","LuxBundle_pt_PT.properties":"locales/pt_pt.properties","LuxBundle_ro.properties":"locales/ro.properties","LuxBundle_ru.properties":"locales/ru.properties","LuxBundle_sl.properties":"locales/sl.properties","LuxBundle_sv.properties":"locales/sv.properties","LuxBundle_tr.properties":"locales/tr.properties","LuxBundle_vn.properties":"locales/vn.properties","LuxBundle_zh_CN.properties":"locales/zh_cn.properties","LuxBundle_zh_HK.properties":"locales/zh_hk.properties","MapEditorBundle_de.properties":"locales/editor/de.properties","MapEditorBundle_en.properties":"locales/editor/en.properties","MapEditorBundle_hr.properties":"locales/editor/hr.properties","MapEditorBundle_ko.properties":"locales/editor/ko.properties","MapEditorBundle_ru.properties":"locales/editor/ru.properties","MapEditorBundle_vn.properties":"locales/editor/vn.properties","MapEditorBundle_zh_CN.properties":"locales/editor/zh_cn.properties","MapEditorBundle_zh_HK.properties":"locales/editor/zh_hk.properties"}

FILE_DICT = {"LuxCore.jar":"assets/LuxCore.jar","docs/changelog.html":"docs/changelog.html","docs/hosting.html":"docs/hosting.html","docs/preferences.html":"docs/preferences.html","docs/rules.html":"docs/rules.html","docs/shortcuts.html":"docs/shortcuts.html","Support/Boards/Saved/Castle Lux MP.luxb":"maps/Castle Lux MP.luxb","Support/Boards/Saved/Classic Widescreen.luxb":"maps/Classic Widescreen.luxb","Support/Boards/Saved/Imperium Romanum Expletus.luxb":"maps/Imperium Romanum Expletus.luxb","Support/Boards/Saved/Napoleonic Wars HD.luxb":"maps/Napoleonic Wars HD.luxb","Support/Boards/Saved/Roman Empire II.luxb":"maps/Roman Empire II.luxb","Support/Boards/Saved/Siege Lux.luxb":"maps/Siege Lux.luxb","Support/Boards/Saved/Silicon Valley HD.luxb":"maps/Silicon Valley HD.luxb","Support/Boards/Saved/Solar System.luxb":"maps/Solar System.luxb","Support/Boards/Saved/U.S.A. War Zone.luxb":"maps/U.S.A. War Zone.luxb","Support/Boards/Saved/WWII Europe Redux.luxb":"maps/WWII Europe Redux.luxb","Support/Boards/Saved/WWII Pacific Redux.luxb":"maps/WWII Pacific Redux.luxb","Support/Themes/Air/background.jpg":"themes/Air/background.jpg","Support/Themes/Air/black.color":"themes/Air/black.color","Support/Themes/Air/sky01.png":"themes/Air/sky01.png","Support/Themes/Air/sky02.png":"themes/Air/sky02.png","Support/Themes/Air/sky03.png":"themes/Air/sky03.png","Support/Themes/Air/sky04.png":"themes/Air/sky04.png","Support/Themes/Air/sky05.png":"themes/Air/sky05.png","Support/Themes/Air/sky06.png":"themes/Air/sky06.png","Support/Themes/Air/sky07.png":"themes/Air/sky07.png","Support/Themes/Air/sky08.png":"themes/Air/sky08.png","Support/Themes/Biohazard Deux/background.jpg":"themes/Biohazard Deux/background.jpg","Support/Themes/Castle MP/background.jpg":"themes/Castle MP/background.jpg","Support/Themes/Castle MP/foreground.jpg":"themes/Castle MP/foreground.jpg","Support/Themes/Castle MP/overground.png":"themes/Castle MP/overground.png","Support/Themes/Classic/background.jpg":"themes/Classic/background.jpg","Support/Themes/Classic WS/background.png":"themes/Classic WS/background.png","Support/Themes/Classic WS/foreground.jpg":"themes/Classic WS/foreground.jpg","Support/Themes/IRexp/foreground.jpg":"themes/IRexp/foreground.jpg","Support/Themes/IRexp/overground.png":"themes/IRexp/overground.png","Support/Themes/MB Napoleon/foreground.jpg":"themes/MB Napoleon/foreground.jpg","Support/Themes/MB Napoleon/overground.png":"themes/MB Napoleon/overground.png","Support/Themes/MB Pacific Redux/foregound.jpg":"themes/MB Pacific Redux/foregound.jpg","Support/Themes/MB Pacific Redux/foreground.jpg":"themes/MB Pacific Redux/foreground.jpg","Support/Themes/MB Pacific Redux/overground.png":"themes/MB Pacific Redux/overground.png","Support/Themes/MB Silicon Valley HD/foreground.jpg":"themes/MB Silicon Valley HD/foreground.jpg","Support/Themes/MB Silicon Valley HD/foreground@2x.jpg":"themes/MB Silicon Valley HD/foreground@2x.jpg","Support/Themes/MB Silicon Valley HD/overground.png":"themes/MB Silicon Valley HD/overground.png","Support/Themes/MB Silicon Valley HD/overground@2x.png":"themes/MB Silicon Valley HD/overground@2x.png","Support/Themes/MB WWII Europe Redux/foreground.jpg":"themes/MB WWII Europe Redux/foreground.jpg","Support/Themes/MB WWII Europe Redux/overground.png":"themes/MB WWII Europe Redux/overground.png","Support/Themes/Ocean/background.jpg":"themes/Ocean/background.jpg","Support/Themes/Ocean/sea_battleship.png":"themes/Ocean/sea_battleship.png","Support/Themes/Ocean/sea_dragon.png":"themes/Ocean/sea_dragon.png","Support/Themes/Ocean/sea_rig.png":"themes/Ocean/sea_rig.png","Support/Themes/Ocean/sea_sail.png":"themes/Ocean/sea_sail.png","Support/Themes/Ocean/sea_sub.png":"themes/Ocean/sea_sub.png","Support/Themes/Roman Empire II/foreground.png":"themes/Roman Empire II/foreground.png","Support/Themes/Roman Empire II/overground.png":"themes/Roman Empire II/overground.png","Support/Themes/Siege/background.jpg":"themes/Siege/background.jpg","Support/Themes/Siege/foreground.jpg":"themes/Siege/foreground.jpg","Support/Themes/Siege/overground.png":"themes/Siege/overground.png","Support/Themes/Solar System/background.jpg":"themes/Solar System/background.jpg","Support/Themes/Solar System/foreground.jpg":"themes/Solar System/foreground.jpg","Support/Themes/Solar System/overground.png":"themes/Solar System/overground.png","Support/Themes/Space/background.png":"themes/Space/background.png","Support/Themes/Space/space01.png":"themes/Space/space01.png","Support/Themes/Space/space02.png":"themes/Space/space02.png","Support/Themes/Space/space03.png":"themes/Space/space03.png","Support/Themes/Space/space04.png":"themes/Space/space04.png","Support/Themes/Space/space05.png":"themes/Space/space05.png","Support/Themes/Space/space06.png":"themes/Space/space06.png","Support/Themes/Space/space07.png":"themes/Space/space07.png","Support/Themes/USA War Zone/background.jpg":"themes/USA War Zone/background.jpg","Support/Themes/USA War Zone/overground.png":"themes/USA War Zone/overground.png"}

def get_locales(language: str, string: str, editor: bool = False):
    if editor:
        editorstr = "editor/"
    else:
        editorstr = ""
    if os.path.exists(f"{cwd}/locales/{editorstr}{language}.properties"):
        with open(f"{cwd}/locales/{editorstr}{language}.properties", "r", encoding='utf-8') as f:
            lines = f.read().splitlines()
    else:
        lines= []
    result = None
    for line in lines:
        if line.split("=")[0].strip() == string:
            result = line.split("=")[1].strip().encode('utf-8').decode('unicode-escape')
    if not result == None:
        return result
    else:
        if os.path.exists(f"{cwd}/locales/{editorstr}en.properties"):
            with open(f"{cwd}/locales/{editorstr}en.properties", "r", encoding='utf-8') as f:
                lines = f.read().splitlines()
        else:
            lines = []
        for line in lines:
            if line.split("=")[0].strip() == string:
                result = line.split("=")[1].strip().encode('utf-8').decode('unicode-escape')
        if not result == None:
            return result
        else:
            return f"No translation found"

def get_colors(data_string: str):
    if isinstance(data_string, bytes):
        data_string = data_string.decode('utf-8', errors='ignore')

    # Updated pattern to match color values with varying decimal places
    color_pattern = r't\x00\x0b([\d.]+/[\d.]+/[\d.]+)|t\x00\r([\d.]+/[\d.]+/[\d.]+)'
    
    matches = re.findall(color_pattern, data_string)
    # 5 is orange
    # 4 is white
    # 3 is black
    # 2 is green
    # 1 is red
    # 0 is 
    colors = []
    matches = [matches[1], matches[2], matches[3], matches[4], matches[5], matches[0]]
    for match in matches:
        color_str = match[0] if match[0] else match[1]  # Choose non-empty group
        r, g, b = map(float, color_str.split('/'))
        colors.append((int(r * 255), int(g * 255), int(b * 255)))
    
    return colors

def qt_message_handler(mode, context, message):
    if "Pixmap is a null pixmap" not in message:
        if mode == QtMsgType.QtWarningMsg:
            print(f"Qt Warning: {message}", file=sys.stderr)
        elif mode == QtMsgType.QtCriticalMsg:
            print(f"Qt Critical: {message}", file=sys.stderr)
        elif mode == QtMsgType.QtFatalMsg:
            print(f"Qt Fatal: {message}", file=sys.stderr)
        elif mode == QtMsgType.QtInfoMsg:
            print(f"Qt Info: {message}", file=sys.stderr)

def get_name_and_quote(input_string):
    # Decode the byte string to a regular string
    decoded_string = input_string.decode('latin-1')
    
    # Extract the name (handling variable character after 't')
    name_match = re.search(r't\x00.([\w]+)', decoded_string)
    name = name_match.group(1) if name_match else None

    # Extract the quote
    quote_match = re.search(r'"([^"]*)"', decoded_string)
    quote = quote_match.group(1) if quote_match else None

    return name, quote

def analyze_strings(str1, str2):
    def get_basic_info(s):
        return {
            'length': len(s),
            'is_alpha': s.isalpha(),
            'is_digit': s.isdigit(),
            'is_alnum': s.isalnum(),
            'is_lower': s.islower(),
            'is_upper': s.isupper(),
            'is_title': s.istitle(),
            'contains_spaces': ' ' in s,
            'contains_digits': any(char.isdigit() for char in s),
            'contains_special_chars': bool(re.search(r'\W', s)),
        }
    
    def compare_strings(s1, s2):
        return {
            'equal': s1 == s2,
            'case_insensitive_equal': s1.lower() == s2.lower(),
            's1_in_s2': s1 in s2,
            's2_in_s1': s2 in s1,
            'common_substrings': set(s1.split()).intersection(s2.split()),
        }
    
    info_str1 = get_basic_info(str1)
    info_str2 = get_basic_info(str2)
    comparison = compare_strings(str1, str2)
    
    return {
        'string1_info': info_str1,
        'string2_info': info_str2,
        'comparison': comparison,
    }

def _remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

def _remove_dir_robustly(path, max_retries=5, delay=1):
    """Remove a directory and all its contents, with retry mechanism."""
    for _ in range(max_retries):
        try:
            shutil.rmtree(path, onerror=_remove_readonly)
            return  # If successful, exit the function
        except PermissionError as e:
            print(f"Permission error: {e}. Retrying...")
            time.sleep(delay)  # Wait before retrying
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying...")
            time.sleep(delay)  # Wait before retrying
    
    print(f"Failed to remove directory after {max_retries} attempts.")

def firststartup():
    if os.path.exists("tmp"):
        _remove_dir_robustly("tmp")
    os.makedirs("tmp",exist_ok=True)
    os.makedirs("assets/explosions/black",exist_ok=True)
    os.makedirs("assets/explosions/explosion1",exist_ok=True)
    os.makedirs("assets/explosions/explosion2",exist_ok=True)
    os.makedirs("assets/explosions/flash",exist_ok=True)
    os.makedirs("assets/explosions/greenblack4",exist_ok=True)
    os.makedirs("assets/explosions/purple",exist_ok=True)
    os.makedirs("assets/explosions/redblack2",exist_ok=True)
    os.makedirs("locales/editor",exist_ok=True)
    os.makedirs("maps",exist_ok=True)
    os.makedirs("themes/Air",exist_ok=True)
    os.makedirs("themes/Biohazard Deux",exist_ok=True)
    os.makedirs("themes/Castle MP",exist_ok=True)
    os.makedirs("themes/Classic",exist_ok=True)
    os.makedirs("themes/Classic WS",exist_ok=True)
    os.makedirs("themes/IRexp",exist_ok=True)
    os.makedirs("themes/MB Napoleon",exist_ok=True)
    os.makedirs("themes/MB Pacific Redux",exist_ok=True)
    os.makedirs("themes/MB Silicon Valley HD",exist_ok=True)
    os.makedirs("themes/MB WWII Europe Redux",exist_ok=True)
    os.makedirs("themes/Ocean",exist_ok=True)
    os.makedirs("themes/Roman Empire II",exist_ok=True)
    os.makedirs("themes/Siege",exist_ok=True)
    os.makedirs("themes/Solar System",exist_ok=True)
    os.makedirs("themes/Space",exist_ok=True)
    os.makedirs("themes/USA War Zone",exist_ok=True)
    try:
        LuxFilesGetter.download_lux("tmp/Lux.tgz")
        LuxFilesGetter.extract_tgz("tmp/Lux.tgz","tmp")
        LuxFilesGetter.extract_from_jar("tmp/LuxDelux/LuxCore.jar", JAR_FILE_DICT)
        LuxFilesGetter.get_from_folder("tmp/LuxDelux", FILE_DICT)
    except:
        sys.exit(1)
    _remove_dir_robustly("tmp")