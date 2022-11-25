build() {
    if [ "$1" = "linux" ]; then
        echo "Building for linux"
    elif [ "$1" = "windows" ]; then
      # call windows function
        windows
    else
        echo "Building for linux"
        echo "Building for windows"
    fi
}

windows() {
    echo "Building for windows"
    cp install/win/installer.cfg win-build.tmp
    pynsist.exe win-build.tmp
    mkdir dist/win
    # make dist win directory if not exit
    if [ ! -d dist/win ]; then
        mkdir dist/win
    fi
    cp build/nsis/*.exe dist/win
    # calculate aes256 hash of exe file
    openssl dgst -sha256 dist/win/*.exe > dist/win/sha256sum.txt
    rm win-build.tmp
}

linux() {
  pyinstaller --onefile aimm.py --name aimm --distpath .
}

macos() {
  pyinstaller --onefile aimm.py --name aimm-macos --distpath .
}

macos_dmg() {
  pyinstaller --onefile aimm.py --name aimm-macos --distpath .
}

build $1