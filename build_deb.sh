#!/bin/bash

set -e

APP_NAME="oakd-uvc"
VERSION="1.0.0"
ARCH="amd64"
BUILD_DIR="./${APP_NAME}_${VERSION}"
BIN_NAME="oakd-uvc-gui"
BIN_PATH="./dist/${BIN_NAME}"
ICON_SRC="./oakd-uvc.png"
DESKTOP_SRC="./desktop/oakd-uvc.desktop"

echo "🧹 Cleaning previous build..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/usr/local/bin"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/64x64/apps"

echo "📦 Creating control file..."
cat <<EOF > "$BUILD_DIR/DEBIAN/control"
Package: $APP_NAME
Version: $VERSION
Architecture: $ARCH
Maintainer: Sri Chakra
Depends: libc6 (>= 2.31), libglib2.0-0, libgtk-3-0
Description: GUI app to toggle OAK-D UVC mode for Zoom/Meet
 A friendly Tkinter GUI that allows you to activate and deactivate webcam mode on your Luxonis OAK-D device with one click.
EOF

echo "📁 Copying app binary..."
cp "$BIN_PATH" "$BUILD_DIR/usr/local/bin/$BIN_NAME"
chmod +x "$BUILD_DIR/usr/local/bin/$BIN_NAME"

echo "📁 Copying .desktop launcher..."
cp "$DESKTOP_SRC" "$BUILD_DIR/usr/share/applications/oakd-uvc.desktop"

echo "🖼️  Copying icon..."
cp "$ICON_SRC" "$BUILD_DIR/usr/share/icons/hicolor/64x64/apps/oakd-uvc.png"

echo "📦 Building .deb package..."
dpkg-deb --build "$BUILD_DIR"

echo "✅ Done. Built: ${BUILD_DIR}.deb"
