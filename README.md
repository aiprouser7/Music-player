# TubeLoader (YouTube Downloader)

A Kivy-based Android downloader that uses [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) with a simple, touch-friendly UI. Paste a YouTube link, choose MP4 (video) or MP3 (audio), and grab the file directly on your device. The included GitHub Actions workflow builds a release APK via Buildozer.

## Features
- Clean Kivy interface optimized for Android touch controls
- MP4 video or MP3 audio downloads using `yt-dlp`
- Background download thread with live status updates
- Files saved inside the app's `downloads` directory

## Local development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Kivy app (desktop simulation):
   ```bash
   python main.py
   ```

## Android build (GitHub Actions)
The workflow **Build Android APK** uses the official `kivy/buildozer` Docker image:
1. Trigger the workflow manually from the Actions tab (`workflow_dispatch`).
2. The pipeline runs `buildozer android release` and uploads the generated APK from `bin/` as an artifact named `tubeloader-apk`.

## Buildozer configuration
Key settings in `buildozer.spec`:
- `requirements = python3,kivy,yt-dlp`
- Permissions: `INTERNET`, `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`
- Architectures: `arm64-v8a`, `armeabi-v7a`

## Notes
- Ensure the device has network access and sufficient storage when downloading.
- The release APK produced by the workflow is unsigned; sign it before publishing to stores.
