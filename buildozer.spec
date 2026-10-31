[app]
title = Apprentissage Pyromax
package.name = apprentissagepyromax
package.domain = org.pyromax
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.accept_sdk_license = True
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
# Commentez ou supprimez les lignes android.sdk et android.ndk en ajoutant un '#' devant pour laisser Buildozer choisir les versions compatibles automatiquement :
# android.sdk = 30
# android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

