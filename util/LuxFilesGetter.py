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

import sys
import os
import tarfile
import requests
import zipfile
from PyQt6.QtWidgets import QApplication, QProgressBar, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import shutil

class DownloadThread(QThread):
    progress_update = pyqtSignal(int)
    download_complete = pyqtSignal()

    def __init__(self, url, path):
        super().__init__()
        self.url = url
        self.path = path

    def run(self):
        response = requests.get(self.url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        written = 0

        with open(self.path, 'wb') as file:
            for data in response.iter_content(block_size):
                written += len(data)
                file.write(data)
                if total_size > 0:
                    progress = int((written / total_size) * 100)
                    self.progress_update.emit(progress)

        self.download_complete.emit()

class DownloadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LuxCore.py first startup... (1/3)')
        self.setGeometry(300, 300, 330, 100)
        layout = QVBoxLayout()
        self.holdon_label = QLabel()
        self.holdon_label.setText("Hold on, we are downloading Lux...")
        self.progress_bar = QProgressBar()
        layout.addWidget(self.holdon_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def close_window(self):
        self.close()


class ExtractThread(QThread):
    progress_update = pyqtSignal(int)
    extraction_complete = pyqtSignal()

    def __init__(self, tgz_path, output_path):
        super().__init__()
        self.tgz_path = tgz_path
        self.output_path = output_path

    def run(self):
        with tarfile.open(self.tgz_path, 'r:gz') as tar:
            total_members = len(tar.getmembers())
            for i, member in enumerate(tar.getmembers(), 1):
                tar.extract(member, path=self.output_path)
                progress = int((i / total_members) * 100)
                self.progress_update.emit(progress)
        
        self.extraction_complete.emit()

class ExtractionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LuxCore.py first startup... (2/3)')
        self.setGeometry(300, 300, 330, 100)
        layout = QVBoxLayout()
        self.holdon_label = QLabel()
        self.holdon_label.setText("Hold on, we are extracting Lux...")
        self.progress_bar = QProgressBar()
        layout.addWidget(self.holdon_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def close_window(self):
        self.close()

class ExtractJarThread(QThread):
    progress_update = pyqtSignal(int)
    extraction_complete = pyqtSignal()

    def __init__(self, jar_path, file_dict):
        super().__init__()
        self.jar_path = jar_path
        self.file_dict = file_dict

    def run(self):
        with zipfile.ZipFile(self.jar_path, 'r') as jar:
            total_files = len(self.file_dict)
            for i, (src, dest) in enumerate(self.file_dict.items(), 1):
                try:
                    jar.extract(src, path=os.path.dirname(dest))#
                    print(f"{os.path.dirname(dest)}/{src}")
                    os.rename(f"{os.path.dirname(dest)}/{src}", dest)
                except KeyError:
                    print(f"Warning: File {src} not found in the JAR.")
                except Exception as e:
                    print(f"Error extracting {src}: {e}")
                progress = int((i / total_files) * 100)
                self.progress_update.emit(progress)
        
        self.extraction_complete.emit()

class GetFromFolderThread(QThread):
    progress_update = pyqtSignal(int)
    extraction_complete = pyqtSignal()

    def __init__(self, folder_path, file_dict):
        super().__init__()
        self.folder_path = folder_path
        self.file_dict: dict = file_dict

    def run(self):
        total_files = len(self.file_dict)
        for i in range(total_files):
            try:
                shutil.copy(self.folder_path + "/" + list(self.file_dict.keys())[i], list(self.file_dict.values())[i])
            except Exception as e:
                print(f"Error refractoring {list(self.file_dict.keys())[i]}: {e}")
            progress = int((i / total_files) * 100)
            self.progress_update.emit(progress)
    
        self.extraction_complete.emit()

class ExtractionFromJarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LuxCore.py first startup... (3/3)')
        self.setGeometry(300, 300, 330, 100)
        layout = QVBoxLayout()
        self.holdon_label = QLabel()
        self.holdon_label.setText("Hold on, we are refractoring Lux... (1/2)")
        self.progress_bar = QProgressBar()
        layout.addWidget(self.holdon_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def close_window(self):
        self.close()


class GetFromFolderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LuxCore.py first startup... (3/3)')
        self.setGeometry(300, 300, 330, 100)
        layout = QVBoxLayout()
        self.holdon_label = QLabel()
        self.holdon_label.setText("Hold on, we are refractoring Lux... (2/2)")
        self.progress_bar = QProgressBar()
        layout.addWidget(self.holdon_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def close_window(self):
        self.close()

def get_from_folder(folder_path, file_dict):
    app = QApplication(sys.argv)
    app.setStyle("windowsvista")
    window = GetFromFolderWindow()
    window.show()

    extract_thread = GetFromFolderThread(folder_path, file_dict)
    extract_thread.progress_update.connect(window.update_progress)
    extract_thread.extraction_complete.connect(window.close_window)
    extract_thread.start()

    app.exec()

def extract_from_jar(jar_path, file_dict):
    app = QApplication(sys.argv)
    app.setStyle("windowsvista")
    window = ExtractionFromJarWindow()
    window.show()

    extract_thread = ExtractJarThread(jar_path, file_dict)
    extract_thread.progress_update.connect(window.update_progress)
    extract_thread.extraction_complete.connect(window.close_window)
    extract_thread.start()

    app.exec()

def extract_tgz(tgz_path, output_path):
    app = QApplication(sys.argv)
    app.setStyle("windowsvista")
    window = ExtractionWindow()
    window.show()

    extract_thread = ExtractThread(tgz_path, output_path)
    extract_thread.progress_update.connect(window.update_progress)
    extract_thread.extraction_complete.connect(window.close_window)
    extract_thread.start()

    app.exec()

def download_lux(path):
    app = QApplication(sys.argv)
    app.setStyle("windowsvista")
    window = DownloadWindow()
    window.show()

    url = "https://s3.amazonaws.com/sillysoft/LuxDelux-linux.tgz"  # Replace with actual URL
    download_thread = DownloadThread(url, path)
    download_thread.progress_update.connect(window.update_progress)
    download_thread.download_complete.connect(window.close_window)
    download_thread.start()

    app.exec()