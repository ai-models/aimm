#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Copy the app bundle to the dmg folder.
cp -r "dist/aimm.app" dist/dmg
# If the DMG already exists, delete it.
create-dmg \
  --volname "aimm" \
  --volicon "aimm.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "aimm.app" 175 120 \
  --hide-extension "aimm.app" \
  --app-drop-link 425 120 \
  "dist/aimm.dmg" \
  "dist/dmg/"