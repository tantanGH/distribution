## X68000Z と Raspberry Pi 3B+/4B で RS-MIDI再生を行う構成例

注意：内容については全くの無保証です。X68000Z, Raspberry Pi, MIDI機器などに致命的な損傷が出ても対応できませんので、試す場合は自己責任でお願いします。

2023.04.05 tantan

---

### 用意するもの

- X68000Z 本体
- X68000Z 本体付属のUARTケーブル
- ブレッドボード用ジャンパケーブル(オス-メス) 3本 (無くても良いが、純正UARTケーブルの延長と抜き差し回数を減らす意味合い)
- Raspberry Pi 3B+ または 4B (それ以外の機種は持ってないので不明)
- USB-MIDI アダプタ
- MIDI音源(SC55mkIIでのみ確認)

---

### Raspberry Pi のセットアップ

以下すべて OS は 32bit Lite (デスクトップ無し) の2023年4月時点の最新のもので確認した手順。


1. シリアルコンソール無効化とUART有効化

        sudo raspi-config

  Interface Options, Serial Port を選択して serial console -> no, uart -> yes を選択し、raspi-configを終了する。再起動。

        sudo reboot


2. Bluetooth 無効化

        sudo vi /boot/config.txt

  以下追加して再起動

        dtoverlay=disable-bt


3. Primary UART確認

        ls -alF /dev/serial*

  `/dev/serial0` が `ttyAMA0` へのシンボリックリンクになっていることを確認


4. ttymidiのインストール

        sudo apt-get install libasound2-dev
        wget http://www.varal.org/ttymidi/ttymidi.tar.gz
        tar zxvf ttymidi.tar.gz
        cd ttymidi/

  Makefile編集
        
        vi Makefile

  `-lpthread`を追加する

        gcc src/ttymidi.c -o ttymidi -lasound -lpthread

  ビルド＆インストール

        make 
        sudo make install


---

### X68000Z のセットアップ

1. 起動XDFの準備

- Human68k 3.02
- CONFIG.SYS の RSDRV.SYS をコメントアウト
- ZMUSIC.X 2.08 の RS-MIDI パッチ版
- MZP一式
- いくつかのMIDIサンプル曲(ZMS/RCP等)

2. Emulator Settings

電源投入後すぐに interrupt ボタンを押し、Setup utility を起動する。
RS232 ボーレートを 19200bps に設定する。

---

### ハードウェア接続

#### すべての電源OFF

X68000Z、Raspberry Pi、MIDI音源のすべての電源を切る。Raspberry Piは電源ケーブルを抜いておく。

#### UART結線

- X68000Z UART GND - (ジャンパケーブル) - Raspberry Pi 6番ピン
- X68000Z UART RX  - (ジャンパケーブル) - Raspberry Pi 8番ピン(GPIO14, UART_TXD0)
- X68000Z UART TX  - (ジャンパケーブル) - Raspberry Pi 10番ピン(GPIO15, UART_RDX0)

#### MIDI結線

USB-MIDIアダプタを Raspberry Piに接続。

- USB-MIDI アダプタ MIDI OUT - MIDI音源 MIDI IN
- USB-MIDI アダプタ MIDI IN - MIDI音源 MIDI OUT

MIDI音源側にserial(PC)/MIDIモードの切り替えがあれば、MIDIモードにしておく。

4. 電源ON

電源を入れ、煙や匂いが無いことを確認w


---

### RS-MIDI再生

1. ttymidi 開始

Raspberry Pi にログインし、ttymidi をバックグラウンドで起動する。

        ttymidi -s /dev/serial0 -b 38400 &

2. aconnect

現在の認識状況を確認し、ttymidi の out を USB MIDI の in に繋げる。

        $ aconnect -io
        client 0: 'System' [type=kernel]
            0 'Timer           '
            1 'Announce        '
        client 14: 'Midi Through' [type=kernel]
            0 'Midi Through Port-0'
        client 28: 'USB MIDI Interface' [type=kernel,card=3]
            0 'USB MIDI Interface MIDI 1'
        client 128: 'ttymidi' [type=user,pid=971]
            0 'MIDI out        '
            1 'MIDI in         '

        $ aconnect 128:0 28:0

3. Human起動

エミュレータモードでHuman68kを起動し、ZMUSICv2 RS-MIDI を常駐させる。

4. 曲の再生

- ZMSであれば `ZP.X`
- RCPであれば `RCtoZ.X`

を使って再生し、曲が流れることを確認する。

---

変更履歴

- 2023/04/05 ... 初版