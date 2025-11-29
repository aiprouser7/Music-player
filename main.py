import os
import threading
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

import yt_dlp


KV = """
<RootWidget>:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(12)

    Label:
        text: "YouTube Downloader"
        font_size: "24sp"
        bold: True
        size_hint_y: None
        height: self.texture_size[1]

    Label:
        text: "Paste a YouTube URL and choose the format."
        size_hint_y: None
        height: self.texture_size[1]
        color: 0.7, 0.7, 0.7, 1

    TextInput:
        id: url_input
        hint_text: "https://youtube.com/watch?v=..."
        size_hint_y: None
        height: dp(48)
        multiline: False

    Spinner:
        id: format_spinner
        text: "MP4 (video)"
        values: ["MP4 (video)", "MP3 (audio)"]
        size_hint_y: None
        height: dp(48)

    Button:
        id: download_button
        text: "Download"
        size_hint_y: None
        height: dp(48)
        on_press: app.start_download()
        disabled: app.is_downloading

    ScrollView:
        size_hint_y: 1
        do_scroll_x: False

        Label:
            id: status_label
            text: app.status_text
            text_size: self.width, None
            size_hint_y: None
            padding: dp(4), dp(4)
            halign: "left"
            valign: "top"
            height: self.texture_size[1]
"""


class RootWidget(BoxLayout):
    pass


class DownloaderApp(App):
    is_downloading = BooleanProperty(False)
    status_text = StringProperty("Idle.")

    def build(self):
        Builder.load_string(KV)
        self.title = "TubeLoader"
        return RootWidget()

    def start_download(self):
        if self.is_downloading:
            return

        url_input = self.root.ids.url_input
        format_spinner = self.root.ids.format_spinner
        url = (url_input.text or "").strip()

        if not url:
            self._update_status("Please provide a valid YouTube URL.")
            return

        self.is_downloading = True
        self._update_status("Starting download...\n")

        thread = threading.Thread(
            target=self._download_media,
            args=(url, format_spinner.text),
            daemon=True,
        )
        thread.start()

    def _download_media(self, url: str, format_choice: str):
        download_dir = Path(self.user_data_dir) / "downloads"
        download_dir.mkdir(parents=True, exist_ok=True)

        is_audio = "MP3" in format_choice
        format_option = "bestaudio/best" if is_audio else "bv*+ba/best"
        postprocessors = []
        if is_audio:
            postprocessors.append(
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            )

        ydl_opts = {
            "format": format_option,
            "outtmpl": os.fspath(download_dir / "%(title)s.%(ext)s"),
            "progress_hooks": [self._progress_hook],
            "postprocessors": postprocessors,
            "quiet": True,
            "no_warnings": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self._update_status("\nDownload complete! Files saved to:\n" f"{download_dir}")
        except Exception as exc:  # noqa: BLE001
            self._update_status(f"\nError: {exc}")
        finally:
            Clock.schedule_once(lambda *_: self._set_downloading(False))

    def _progress_hook(self, data):
        if data.get("status") == "downloading":
            percent = data.get("_percent_str", "0.0%").strip()
            speed = data.get("_speed_str", "0 B/s").strip()
            eta = data.get("_eta_str", "?")
            status = f"Downloading: {percent} at {speed}, ETA {eta}"
            self._update_status(status)
        elif data.get("status") == "finished":
            self._update_status("Download finished. Converting if needed...")

    def _update_status(self, message: str):
        def update_text(dt):  # noqa: ARG001
            self.status_text = message

        Clock.schedule_once(update_text, 0)

    def _set_downloading(self, value: bool):
        self.is_downloading = value


if __name__ == "__main__":
    DownloaderApp().run()
