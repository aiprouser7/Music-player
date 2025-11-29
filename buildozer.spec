[app]
title = TubeLoader
package.name = tubeloader
package.domain = org.example.tubeloader
source.dir = .
source.include_exts = py,kv,md,txt
version = 0.1.0
requirements = python3,kivy,yt-dlp
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 0

[app:source.exclude_dirs]
# Skip build caches if they exist
a.buildozer
.buildozer
bin
