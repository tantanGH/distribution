# X68000Z と Raspberry Pi 3B+ で UART クロス接続を使ってファイルの送受信を行う

### はじめに

2023年3月31日よりクラウドファンディング支援者への提供が始まったZUIKI製[X68000Z](https://www.zuiki.co.jp/products/x68000z/) Early Access Kit ですが、2023年4月現在 HDD イメージの扱いに対応しておらず、物理SDカード上に入れた 1.2MB FDイメージを使って外部とファイルのやり取りを行う必要があります。

しかしながら、1.2MBを超えるファイルのやり取りを行う場合、以下のような課題があります。

- メディア抜き差しの手間
- ファイル群を1.2MB単位に分割する手間
- 1.2MBを超えるファイルは split などで分割してRAMDISKに置いた後に連結しなくてはならない
- 最終保存先をRAMDISKとした場合、連結のためにスペースが2倍必要になる

この覚書は、HDDイメージが公式にサポートされるまでの繋ぎとして、X68000Z のUART端子を使って Raspberry Pi と直結し、シリアル通信を使ったファイル転送を行うためのセットアップ例を紹介するものです。

注意：全くの無保証であり、この手順により X68000Z や Raspberry Pi に致命的なダメージを与えても当方はどうにもできませんので、こういうことも可能なんだな、くらいに捉えて頂ければと思います。

### 必要なもの

- X68000Z および付属の UART ケーブル
- Raspberry Pi
- オス-メス ジャンパケーブル (必須ではないがあった方が良い)

X68000Z のUART端子・ケーブルの仕様は X68000Z 添付の説明書に記載されています。
ケーブルの色などは出荷時期によって異なる可能性も考えられますので、必ず添付の説明書で確認してください。

### X68000Z 側の準備

- 通信速度を19200bpsに変更する

RESET → INTERRUPT で Setup Utility を起動し、Emulator Settings で 19200bps に変更する。
8bit、パリティなし、ストップビット1 はそのまま。ただし現状 9600bps までしか当方の環境では通信できていません。

- ソフトウェアのダウンロード

大容量バッファを確保できる通信ドライバ TMSIO.X を X68000 LIBRARY からダウンロードし、自身の起動用XDFに入れておく。

[TMSIO.X](http://retropc.net/x68000/software/system/rs232c/tmsio/)

拙作RS232Cファイル送受信用ツール RSRX.X / RSTX.X をダウンロードし、TMSIO 同様に起動用XDFに入れておく。

[RSRX.X](https://github.com/tantanGH/rsrx)
[RSTX.X](https://github.com/tantanGH/rstx)

X68000Z側では受信しかしないのであれば、RSRX.X のみでokです。

もちろん標準的な Z-MODEM などを使っても良いのでしょうが、自分は使っていないので分かりません。


なお、起動用XDFを作る際は不要なファイルを入れないだけでなく、実行ファイル圧縮ツール LZX.X を使って実行ファイルそのもののサイズを減らすのも効果的です。

[LZX.X](http://retropc.net/x68000/software/tools/archiver/italzx/)


- UART ケーブルの準備

X68000Z 本体付属の UART ケーブルを使用します。自分の本体の場合は、

- 緑 (GND)
- 赤 (RX)
- 青 (TX)

の配線色となっており、信号レベルは TX:3V, RX:3~5V と記載されていました。


### Raspberry Pi 側の準備

以下はすべて自分の環境においての記録です。

- Raspberry Pi 3B+
- Raspberry Pi OS Lite 32bit (GUIなし)

Raspberry Pi 4B からは追加のUARTが使えるようになっていたり、Raspberry Pi 2以前はデフォルトが違っていたりと、機種ごとにかなり違いがある部分ですので、ネットの検索なりを利用して適宜対応してください。

- 使うGPIOピンを確認する

6番 : GND
8番 : GPIO14(TXD)
10番 : GPIP15(RXD)

GPIP番号とピン番号の割り当ては一致していないので注意

- UARTを有効にする

    sudo raspi-config

Interface Options -> Serial Port

Would you like a login shell to be accessible over serial? --> No

Would you like the serial port hardware to be enabled? --> Yes

設定変更後、Raspberry Piをrebootする。

- デバイス名の確認

    $ ls -alF /dev/serial*
    lrwxrwxrwx 1 root root 5 Apr  1 22:53 /dev/serial0 -> ttyS0
    lrwxrwxrwx 1 root root 7 Apr  1 22:53 /dev/serial1 -> ttyAMA0

serial0 (Primary UART) が miniUART、serial1 (Secondary UART) が ARM UART (PL011) になりました。

- Primary UART を PL011 に変更する。

miniUARTよりも性能の良い PL011を使いたいので、これを入れ替えます。この状態だとPL011はBluetoothに使われています。
`sudo vi /boot/config.txt` で以下の記述を追記する。

    [all]
    enable_uart=1
    dtoverlay=pi3-miniuart-bt
    core_freq=250

設定変更後、Rasberry Piをrebootする。

- デバイス名の確認

    $ ls -alF /dev/serial*
    lrwxrwxrwx 1 root root 7 Apr  2 06:55 /dev/serial0 -> ttyAMA0
    lrwxrwxrwx 1 root root 5 Apr  2 06:55 /dev/serial1 -> ttyS0

serial0 (Primary UART) が ARM UART (PL011)、serial1 (Secondary UART) が miniUARTになりました。
BluetoothはminiUARTが担当し、シリアルコンソールも無効化してあるのでPL011はフリーになりました。

- ソフトウェアの導入

pip3 が入っていなければ導入

    sudo apt-get -y install python3-dev
    sudo apt-get -y install python3-pip

git が入っていなければ導入

    sudo apt-get -y install git

拙作 rstx/rsrx の Pythonバージョンを導入

    pip3 install git+https://github.com/tantanGH/rstx.git
    pip3 install git+https://github.com/tantanGH/rsrx.git

注意：繰り返しになりますが、ファイル送受信はZ-MODEM等に対応したツールでも代用できると思いますが、自分は使っていないので分かりません。


### ケーブル接続

X68000Z と Raspberry Pi 両方の電源が落ちていることを確認し、以下のように接続します。

    X68000Z UART GND (緑) - Raspberry Pi 6番ピン (GND)
    X68000Z UART RX (赤) - Raspberry Pi 8番ピン (TXD)
    X68000Z UART TX (青) - Raspberry Pi 10番ピン (RXD)

何度も抜き差しすると端子がヘタってくるので、自分の場合は本体付属のUARTケーブルの先にジャンパケーブル(オス-メス)を介してRaspberry Piと接続しています。


### 通信確認 (Raspberry Pi -> X68000Z)

X68000Z と Raspberry Pi の電源を入れ、バチっとショートしたり、煙を吹いたり、変な匂いがしていないことを確認（ぉ

X68000Z はエミュレータモードで起動。この時 CONFIG.SYS で以下を設定しておきます。

- \SYS\RSDRV.SYS は組み込まない
- \SYS\RAMDISK.SYS #M6144 でRAMDISKを6MB確保する

今回ファイル転送先となるのは RAMDISK (C:) です。

COMMAND.X が起動したら TMSIO.X を常駐します。バッファは多めに確保しておきます。

    tmsio -b1024

rsrx を起動します。

    c:
    rsrx -s 9600

    RSRX.X - RS232C File Receiver for X680x0 0.3.0 2023 by tantan
    --
    Download Path: .\
    Baud Rate: 9600 bps
    Timeout: 120 sec
    Buffer Size: 32768 KB

Raspberry Pi にログインして、何かファイルを指定して rstx を起動します。
この時指定するデバイス名は primary UART (今回は miniUART)のものになります。

    $ echo "Hello, X68000Z!!!" > hello.txt
    $ cat hello.txt
    Hello, X68000Z!!!

    $ rstx --device /dev/ttyS0 -s 9600 hello.txt

9600bps での通信に問題がなければ 19200bps を試します。rsrx/rstx のデフォルトは 19200bps なので、その場合は -s オプションを双方省略できます。


### 通信確認 (X68000Z -> Raspberry Pi)

今のところこのケースは少ないかもしれませんが、基本的にやり方は同じです。

Raspberry Pi にログインして、rsrx を起動します。

    rsrx -s 9600

X68000Z 上で

    rstx -s 9600 hoge.txt

です。

9600bps での通信に問題がなければ 19200bps を試します。


### X68000Z Human68k に Raspberry Pi からコンソールアクセスする

Raspberry Pi に gtkterm が入ってなければ導入

    sudo apt-get -y install gtkterm



以上