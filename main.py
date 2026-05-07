import sys
import os
import threading
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QPushButton, QLineEdit, QComboBox, QWidget, 
                             QLabel, QMessageBox, QProgressBar, QHBoxLayout, QMenu)
from PySide6.QtCore import Qt, Signal, QObject, QPoint
from PySide6.QtGui import QAction
import yt_dlp

DATA_MAP = {
    "Azərbaycan": {"ready": "Yükləmək üçün URL daxil edin", "start": "YÜKLƏMƏYƏ BAŞLA", "down": "Yüklənir", "done": "Tamamlandı!"},
    "Deutsch": {"ready": "URL zum Herunterladen eingeben", "start": "DOWNLOAD STARTEN", "down": "Laden", "done": "Abgeschlossen!"},
    "English": {"ready": "Enter URL to download", "start": "START DOWNLOAD", "down": "Downloading", "done": "Finished!"},
    "Español": {"ready": "Introducir URL para descargar", "start": "DESCARGAR", "down": "Descargando", "done": "¡Completado!"},
    "Français": {"ready": "Entrez l'URL à télécharger", "start": "TÉLÉCHARGER", "down": "Téléchargement", "done": "Terminé!"},
    "Italiano": {"ready": "Inserisci l'URL da scaricare", "start": "SCARICA", "down": "Download", "done": "Completato!"},
    "Nederlands": {"ready": "Voer URL in om te downloaden", "start": "DOWNLOAD STARTEN", "down": "Downloaden", "done": "Voltooid!"},
    "Polski": {"ready": "Wprowadź adres URL", "start": "POBIERZ", "down": "Pobieranie", "done": "Zakończono!"},
    "Português": {"ready": "Insira o URL para baixar", "start": "BAIXAR", "down": "Baixando", "done": "Concluído!"},
    "Русский": {"ready": "Введите URL для скачивания", "start": "СКАЧАТЬ", "down": "Загрузка", "done": "Завершено!"},
    "Türkçe": {"ready": "İndirmek için URL girin", "start": "İNDİRMEYİ BAŞLAT", "down": "İndiriliyor", "done": "Tamamlandı!"},
    "اردو": {"ready": "ڈاؤن لوڈ کرنے کے لیے یو آر ایل درج کریں", "start": "ڈاؤن لوڈ شروع کریں", "down": "ڈاؤن لوڈ ہو رہا ہے", "done": "مکمل ہو گیا!"},
    "العربية": {"ready": "أدخل رابط التحميل", "start": "بدء التحميل", "down": "جاري التحميل", "done": "تم بنجاح!"},
    "فارسی": {"ready": "برای دانلود یو آر ال را وارد کنید", "start": "شروع دانلود", "down": "در حال دانلود", "done": "انجام شد!"},
    "हिन्दी": {"ready": "डाउनलोड करने के लिए URL दर्ज करें", "start": "डाउनलोड शुरू करें", "down": "डाउनलोड हो रहा है", "done": "पूरा हुआ!"},
    "中文": {"ready": "输入要下载的 URL", "start": "开始下载", "down": "正在下载", "done": "下载完成！"},
    "日本語": {"ready": "ダウンロードするURLを入力してください", "start": "ダウンロード開始", "down": "ダウンロード中", "done": "完了しました！"},
    "한국어": {"ready": "다운로드할 URL을 입력하세요", "start": "다운로드 시작", "down": "다운로드 중", "done": "완료되었습니다!"}
}

class NetBridge(QObject):
    finish = Signal()
    fail = Signal(str)
    load = Signal(dict)

class YDMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_view = "English"
        self.build_frame()
        
    def build_frame(self):
        self.setWindowTitle("YDM")
        self.setMinimumSize(560, 440)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QLabel { color: #cdd6f4; font-family: sans-serif; }
            QLineEdit { background-color: #313244; color: #cdd6f4; border: 1px solid #45475a; padding: 10px; border-radius: 6px; }
            QComboBox { background-color: #313244; color: #cdd6f4; border: 1px solid #45475a; padding: 6px; border-radius: 6px; }
            QPushButton#actionTrigger { background-color: #89b4fa; color: #11111b; font-weight: bold; padding: 10px; border-radius: 6px; }
            QPushButton#langTrigger { background-color: #45475a; color: #cdd6f4; border-radius: 4px; padding: 8px; font-size: 12px; font-weight: bold; }
            QProgressBar { border: 1px solid #45475a; border-radius: 6px; text-align: center; color: white; background-color: #313244; }
            QProgressBar::chunk { background-color: #a6e3a1; }
            QMenu { background-color: #313244; color: #cdd6f4; border: 1px solid #45475a; }
            QMenu::item:selected { background-color: #45475a; }
        """)

        container = QWidget()
        self.setCentralWidget(container)
        main_box = QVBoxLayout(container)

        nav = QHBoxLayout()
        self.lang_switch = QPushButton("🌐 Language")
        self.lang_switch.setObjectName("langTrigger")
        self.lang_switch.setFixedWidth(140)
        self.lang_switch.clicked.connect(self.show_lang_menu)
        
        nav.addStretch()
        nav.addWidget(self.lang_switch)
        main_box.addLayout(nav)

        self.head = QLabel("YDM")
        self.head.setStyleSheet("font-size: 30px; font-weight: bold; color: #89b4fa;")
        self.head.setAlignment(Qt.AlignCenter)
        main_box.addWidget(self.head)

        self.hint = QLabel("")
        self.hint.setAlignment(Qt.AlignCenter)
        main_box.addWidget(self.hint)

        self.input_url = QLineEdit()
        main_box.addWidget(self.input_url)
        
        self.quality_list = QComboBox()
        main_box.addWidget(self.quality_list)

        self.bar = QProgressBar()
        main_box.addWidget(self.bar)
        
        self.run_btn = QPushButton("")
        self.run_btn.setObjectName("actionTrigger")
        self.run_btn.clicked.connect(self.initiate)
        main_box.addWidget(self.run_btn)

        self.dev_mark = QLabel("Made By: Lenvora")
        self.dev_mark.setStyleSheet("font-size: 10px; color: #585b70; margin-top: 12px;")
        self.dev_mark.setAlignment(Qt.AlignRight)
        main_box.addWidget(self.dev_mark)

        self.event_bus = NetBridge()
        self.event_bus.finish.connect(self.success_pop)
        self.event_bus.fail.connect(self.error_pop)
        self.event_bus.load.connect(self.refresh_bar)
        self.update_locale("English")

    def show_lang_menu(self):
        pop = QMenu(self)
        sorted_keys = sorted(DATA_MAP.keys())
        for k in sorted_keys:
            action = QAction(k, self)
            action.triggered.connect(lambda checked=False, t=k: self.update_locale(t))
            pop.addAction(action)
        pop.exec(self.lang_switch.mapToGlobal(QPoint(0, self.lang_switch.height())))

    def update_locale(self, key):
        self.current_view = key
        set = DATA_MAP[key]
        self.hint.setText(set["ready"])
        self.run_btn.setText(set["start"])
        self.input_url.setPlaceholderText("https://...")
        self.quality_list.clear()
        self.quality_list.addItems(["Maximum", "1080p", "720p", "480p", "MP3 Audio"])

    def refresh_bar(self, data):
        try:
            val = 0
            if data.get('total_bytes'): 
                val = int((data['downloaded_bytes']/data['total_bytes'])*100)
            elif data.get('total_bytes_estimate'): 
                val = int((data['downloaded_bytes']/data['total_bytes_estimate'])*100)
            
            self.bar.setValue(val)
            text = DATA_MAP[self.current_view]["down"]
            self.hint.setText(f"{text} %{val}")
        except: pass

    def core_task(self, link, q):
        try:
            if os.name == 'nt':
                import ctypes
                from ctypes import wintypes
                CSIDL_DOWNLOADS = 37
                buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetSpecialFolderPathW(None, buf, CSIDL_DOWNLOADS, False)
                download_path = buf.value
            else:
                try:
                    xdg_path = subprocess.check_output(['xdg-user-dir', 'DOWNLOAD'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
                    if os.path.exists(xdg_path):
                        download_path = xdg_path
                    else:
                        download_path = str(Path.home() / "Downloads")
                except:
                    download_path = str(Path.home() / "Downloads")

            if not os.path.exists(download_path):
                download_path = os.getcwd()

            target_loc = os.path.join(download_path, "%(title)s.%(ext)s")
            
            params = {
                'outtmpl': target_loc, 
                'progress_hooks': [lambda d: self.event_bus.load.emit(d)], 
                'noplaylist': True, 
                'quiet': True,
                'nocheckcertificate': True
            }
            
            if "MP3" in q:
                params.update({
                    'format': 'bestaudio/best', 
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                    }]
                })
            else:
                v_res = "".join(filter(str.isdigit, q))
                params['format'] = f'bestvideo[height<={v_res}]+bestaudio/best' if v_res else 'bestvideo+bestaudio/best'
            
            with yt_dlp.YoutubeDL(params) as engine:
                engine.download([link])
            
            self.event_bus.finish.emit()
            
        except Exception as e:
            self.event_bus.fail.emit(str(e))

    def initiate(self):
        target = self.input_url.text().strip()
        if not target: return
        self.run_btn.setEnabled(False)
        threading.Thread(target=self.core_task, args=(target, self.quality_list.currentText()), daemon=True).start()

    def success_pop(self):
        self.run_btn.setEnabled(True)
        QMessageBox.information(self, "Status", DATA_MAP[self.current_view]["done"])

    def error_pop(self, info):
        self.run_btn.setEnabled(True)
        QMessageBox.critical(self, "Alert", info)

if __name__ == "__main__":
    proc = QApplication(sys.argv)
    view = YDMApp()
    view.show()
    sys.exit(proc.exec())
