# How to dump FD image on macOS

* USB FDD を接続する

* `diskutil` コマンドで接続したUSB FDDのデバイス名を見つける

    diskutil list

* `dd` コマンドを実行する

    sudo dd if=/dev/rdiskX of=hogehoge.xdf