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

JAR_FILE_DICT = {"bubbleSource1.png":"assets/bubbleSource1.png", "bubbleSource3.png":"assets/bubbleSource3.png",
"bubbleSource5.png":"assets/bubbleSource5.png", "Dirty Headline Custom Sillysoft.ttf":"assets/DirtyHeadline.ttf", "guybw1.png":"assets/guybw1.png",
"guybw2.png":"assets/guybw2.png", "guybw3.png":"assets/guybw3.png", "guybw4.png":"assets/guybw4.png", "LuxDeluxLogo.png":"assets/LuxDeluxLogo.png",
"not_available.jpg":"assets/not_available.jpg", "texture_background.jpg":"assets/texture_background.jpg", "texture_map.jpg":"assets/texture_map.jpg",
"texture_network.jpg":"assets/texture_network.jpg", "texture_players.jpg":"assets/texture_players.jpg"}

FILE_DICT = {"LuxCore.jar":"assets/LuxCore.jar"}

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
    try:
        LuxFilesGetter.download_lux("tmp/Lux.tgz")
        LuxFilesGetter.extract_tgz("tmp/Lux.tgz","tmp")
        LuxFilesGetter.extract_from_jar("tmp/LuxDelux/LuxCore.jar", JAR_FILE_DICT)
        LuxFilesGetter.get_from_folder("tmp/LuxDelux", FILE_DICT)
    except:
        sys.exit(1)
    _remove_dir_robustly("tmp")