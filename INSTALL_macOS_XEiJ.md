# macOS ユーザのための X680x0 エミュレータ XEiJ 導入ガイド (工事中)

2023.1 tantan

---

### 目次

* [はじめに](#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)
* [OpenJDK のダウンロードとインストール](#openjdk-%E3%81%AE%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89%E3%81%A8%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
* [XEiJ のダウンロードとインストール](#xeij-%E3%81%AE%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89%E3%81%A8%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
* [XEiJ の起動](#xeij-%E3%81%AE%E8%B5%B7%E5%8B%95)
* [起動用HDDイメージの作成](#%E8%B5%B7%E5%8B%95%E7%94%A8hdd%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E4%BD%9C%E6%88%90)
* [SHARP から無償提供されたソフトウェアイメージのダウンロード](#sharp-%E3%81%8B%E3%82%89%E7%84%A1%E5%84%9F%E6%8F%90%E4%BE%9B%E3%81%95%E3%82%8C%E3%81%9F%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)
* [起動HDDイメージ内に Human68k 3.02 のファイルをコピー](#%E8%B5%B7%E5%8B%95hdd%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E5%86%85%E3%81%AB-human68k-302-%E3%81%AE%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E3%82%B3%E3%83%94%E3%83%BC)

---

### はじめに

令和の今、X680x0 が再びの盛り上がりを見せています。ひとえに [瑞起(Zuiki,Inc.)によるX68000Zの発表](https://www.zuiki.co.jp/products/x68000z/) によるものが大きいと思いますが、様々な条件がうまく噛み合って、タイミングが良かったのだと思います。

そんな X68000Z は　"X68000初代 10MHz FDモデル 12MBメモリフル実装" をエミュレーションにて実現するというデザインになっているとのことです。
残念ながら HDDイメージには今のところ対応していないので、箱庭のような自分だけの X680x0 環境を育てていこうと思えば、別な形を探る必要があります。

具体的には、有志が開発・メンテナンスを継続してくださっているX680x0エミュレータの利用です。
種類は複数あるのですが、こと macOS を前提にすると、選択肢はほぼ一択で鎌田さんによる XEiJ です。

* [XEiJ (X68000 Emulator in Java)](https://stdkmd.net/xeij/)

XEiJの大きな特徴は、Javaで開発されているということです。すなわちmacOSを含めJavaが動く環境であればどこでも動作可能となります。
自分は ARMアーキテクチャの Apple silicon (M1) を搭載した MacBook Air で動かしていますが、動作も非常に軽快ですし、使っていて違和感がありません。

そして何よりX680x0のハードウェアの非常に細かいところまで詳細に分析・実装されています。

作者の鎌田さんは自分が現役でX68000XVIの実機を使っていた頃からお名前を随所でお見かけしていたレジェンドの一人でもあり、060turboを含めた多くの拡張ハードウェア用のドライバやアプリケーションなどを開発されておられました。まさにX680x0を知り尽くした一人によるエミュレータと言えます。

このドキュメントは XEiJファンの一人として、macOS にこの XEiJ を導入する際のいくつかのポイントを覚書として残しておくものです。

なお、これ以外に macOS で動作するものとして、X680x0のコマンドラインアプリケーションをエミュレーション実行できる run68 というソフトウェアがあります。
これはこれで非常に強力で、導入必須とも言えるのですが、このドキュメントでは割愛します。

---

### OpenJDK のダウンロードとインストール

XEiJを動作させるにはJava環境が必要です。
macOSにはもう標準でJavaが付属することはなくなったので、自分で導入する必要があります。
Javaの本家は Sun Microsystems → 買収されて Oracle となっていますが、Oracleの提供するOracle JDKは一度有料化されました。
その後再び無償化したのですが、今後も不透明なので、ここはオープン版のOpenJDKを導入するのが確実です。

macOS用のOpenJDKは以下からダウンロードできます。2022.10月版のXEiJを動かすにはOpenJDKバージョン19が必要です。

* [openjdk.org](https://jdk.java.net/19/)
* [adoptium.net](https://adoptium.net/)

2つあるサイトのうち、上は本家なのですが、バイナリ配布形態が素の `*.tar.gz` のみとなっています。
下のadoptiumの方は `*.pkg` でインストーラ導入できますので、個人的にはこちらをお勧めします。
Eclipse Foundationによる管理下にあるサイトで信頼できます。ちなみに以前は AdoptJDK というサイト名でしたがEclipseに移管されたそうです。

Apple silicon の Mac を使っている場合は aarch64 もしくは arm64 となっているパッケージを、intel CPU の Mac を使っている場合は x64 もしくは x86_64 のパッケージを導入します。

既に他のJDKを導入済みであっても、複数バージョンを同居させることが可能です。
adoptiumのパッケージから導入した場合は以下にインストールされます。

    /Library/Java/JavaVirtualMachines/temurin-19.jdk/

導入後、新しいターミナルを開いて `java -version` でバージョンを確認します。

    $ java -version
    openjdk version "19.0.1" 2022-10-18
    OpenJDK Runtime Environment Temurin-19.0.1+10 (build 19.0.1+10)
    OpenJDK 64-Bit Server VM Temurin-19.0.1+10 (build 19.0.1+10, mixed mode)
    
バージョン19が表示されればokです。

---

### XEiJ のダウンロードとインストール

XEiJの配布サイトよりZIP形式のファイルをダウンロードします。

* [XEiJ](https://stdkmd.net/xeij/)

この文章執筆時点では version 0.22.10.18 が最新です。

macOSネイティブアプリケーションではありませんので、導入する先のフォルダは自分で決めます。
ただし、今後新バージョンがリリースされた時に上書きインストールしなくても良いように、バージョン名を含めたフォルダに展開しておくのが無難です。

例えば

     /Users/(ユーザ名)/Documents/XEiJ/XEiJ_0221018/
    
などです。ちなみに自分が Documents (書類) フォルダの中に入れているのは iCloud でのバックアップ対象にしているからです。


---

### XEiJ の起動

XEiJを起動するには Finder から XEiJ.jar をダブルクリックします。XEiJのjarは起動用の情報が中に含まれているので、OpenJDKが正しく導入されていればこれだけで起動できます。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij2.png)
 

ただし、最初はこのようなセキュリティの警告が出て起動できません。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij3.png)


そこで、次のような操作を行います。

- Finder で XEiJ.jar を選択。
- Control キーを押しながらポップアップメニューを出す(右クリックもしくはダブルタップ)
- 「開く」を選択
- マルウェアかどうかの確認ダイアログが表示されるので、「開く」を選択

![](https://github.com/tantanGH/distribution/raw/main/images/xeij4.png)

![](https://github.com/tantanGH/distribution/raw/main/images/xeij5.png)

この操作が必要なのは最初の1回だけです。次回からはXEiJ.jarのダブルクリックのみで起動できます。


![](https://github.com/tantanGH/distribution/raw/main/images/xeij6.png)

このように起動できればokです。

[参照: Appleのサポート](https://support.apple.com/ja-jp/guide/mac-help/mh40616/mac)

---

### 起動用HDDイメージの作成

エミュレータ本体は起動できましたが、このままではOSが起動しないので何もできません。

引き続いて起動用のHDDイメージをここから作成していきます。

XEiJウィンドウ内のメニューから、ファイル → SCSI → 一番下の SCSIハードディスクのイメージファイルの新規作成 を選択します。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij7.png)


* ファイル名は自由。ただし拡張子は .HDS で。
* 容量は起動用なので100MBもあれば十分かと思います。実際にここで指定したサイズのファイルがmacOS上に作られます。
* セクタサイズはデフォルトの512バイト
* 領域確保はデフォルトでチェック済
* HUMAN.SYS と COMMAND.X もデフォルトでチェック済

これらを確認したのち 「フォーマットを開始する」 ボタンを押します。フォーマットは一瞬で完了します。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij8.png)


Finder で今指定した　HDSファイルが作成されていることを確認し、再び XEiJ の ファイル - SCSI メニューを開きます。
一番左上の "0" の部分をクリックすると SCSIデバイス0 が有効になりますので、その3つ右にある書類アイコンをクリックして先ほどのHDSファイルを指定します。
指定できたら 「ここから再起動」 ボタンを押してエミュレータ内のX68000を再起動します。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij9a.png)


このように Human68k version 3.02 が起動できればokです。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij10.png)


---

### SHARP から無償提供されたソフトウェアイメージのダウンロード

このままでは COMMAND.X が起動しただけで、再び何もできない状態ですので、その他の Human68k 標準ソフトウェアをHDDイメージ上に導入します。

まずは XEiJ と同じ鎌田さんのサイトで保守されているX68000 LIBRARYから、Human68k のFDディスクイメージをダウンロード

* [http://retropc.net/x68000/software/sharp/human302/](http://retropc.net/x68000/software/sharp/human302/)

このイメージは LZH 形式で圧縮されています。macOSのFinderでは LZH 形式はサポートされていないので、展開のためには別途ソフトウェアの導入が必要です。

具体的には macOS版の 7zip もしくは lha を導入する必要があります。

これらはいずれも macOS向け非公式パッケージ管理ツールである Homebrew を通して導入することができます。

* [Homebrew](https://brew.sh/)

Homebrew がまだ入っていないのであれば、先にHomebrew を導入します。上記サイトのトップページにあるワンライナーをコピーして、Terminalを開いて実行します。

続いて 7zip と lha を導入します。

    $ brew install p7zip
    $ brew install lha

これで LZH ファイルが展開できるようになりました。例えば 7zip を使って先ほどダウンロードした Human68k のLZHを展開するならば、

    $ 7z x HUMN302I.LZH 

または

    $ lha x HUMN302I.LZH

とすればokです。lha を使った方が日本語ファイル名の化けを防ぐことができます。

    $ ls HUMAN302.XDF

として HUMAN302.XDF イメージファイルが展開されたことを確認します。

X68000 LIBRARYでは無償公開された他の製品もディスクイメージ形式でダウンロードできますので、必要に応じて取得してください。

---

### 起動HDDイメージ内に Human68k 3.02 のファイルをコピー

XEiJ に戻り、ファイル → FD のメニューから、先ほど展開できた HUMAN302.XDF を選択します。

ここから再起動を選んでFDから再起動します。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij11.png)

このFDイメージにはCOMMAND.Xだけでなく、他の標準ファイル群も含まれていますので、各種デバイスドライバなどが登録されていく様子がわかります。

コマンドプロンプトで、

    drive

と打ち込んで現在のドライブの認識状況を確認します。A: と B: がFDDで、C:が先ほど作成した起動用のHDDイメージになります。


![](https://github.com/tantanGH/distribution/raw/main/images/xeij12.png)


この状態で、A:のFDの内容をC:のHDDにコピーします。コピーには `COPYALL` コマンドを使います。

    copyall *.* c:

これでA:のFDの内容がC:のHDDに丸ごとコピーされました。

ファイル → FD のメニューからイジェクトアイコンを選択し、FDイメージをアンマウントします。

続いて MPU → リセット を選択して、XEiJ 内の X68000 をリセットします。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij13.png)

HDDから再起動すると、今度はデバイスドライバなども登録されました。

`drive` コマンドを使ってドライブの状況を確認すると、起動ディスクとなったHDDが A:、FDDが B:とC: になったことが分かります。

Human68k はこのように起動したドライブを強制的に A: ドライブとしてしまうのでちょっと使い勝手が悪いことがあります。

特に Windows の経験が長いと C: ドライブが起動HDDドライブで、FDDはA:とB:に固定したいところです。

このためには先ほどからの `drive` コマンドを使うことができます。
このコマンドはドライブレターの入れ替えにも対応しています。

この入れ替えを自動的に行うために、OS起動時に自動実行される `AUTOEXEC.BAT` ファイルを更新します。

    ed AUTOEXEC.BAT

のコマンドで Human68k 標準のテキストエディタ ED が起動できます。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij14.png)

2行目にある PATH の行の頭に `C:\;C:\SYS;C:\BIN;`を挿入します。
カーソルキーで一番下まで移動し、3行加えます。

    \BIN\DRIVE.X B: C:
    \BIN\DRIVE.X C: A:

ESCを押してXキーを押すと、ファイルを保存してエディタを終了できます。

MPU メニューからリセットを行います。


![](https://github.com/tantanGH/distribution/raw/main/images/xeij15.png)

今度はいきなりコマンドプロンプトまで行かず、見慣れない画面になりました。
これは CONFIGED というデバイスドライバ登録用の CONFIG.SYS の内容を一つ一つ調整できるツールです。

CONFIG.SYSの最後に `EXCONFIG=\SYS\CONFIGED.X` として登録されていたためにこれが起動しました。

さしあたってここではESCキーを押して抜ければ、通常通り起動シーケンスが流れます。

![](https://github.com/tantanGH/distribution/raw/main/images/xeij16.png)


無事ドライブレターを固定することができました。

---

### HDS を使った macOS側とのファイルのやりとり

無事に起動用HDDも整備でき、ドライブレターも固定でき、環境は整いました。
とりあえず手元に昔実機で使っていたアプリケーションやデータがあればそれをエミュレータ内に持ち込みたいところです。
また、X68000 LIBRARY やベクターなどからX680x0用のフリーソフトがダウンロードできるサイトもあります。

ですが、これらを macOS 側で準備したとしても、現状ではそれをエミュレータ内の環境に持ち込むことができません。
なぜなら、X68000側からネットワークどころかホストである macOS 側がこのままでは見えないからです。

そこで使うのが XEiJ の HFS (Host File System) 機能です。

これは HDS(HDDイメージファイル)やXDF(FDイメージファイル)と異なり、ホスト側のファイルシステムをそのまま2GBの仮想ドライブとして
エミュレータのX68000から読み書きするための機能です。

ここではその使い方を説明します。

まずは準備として macOS 上で X68000 から読み書きさせたいフォルダを新しく作成します。

次に以下よりディスクイメージ版ではない方の LZH ファイルをダウンロードします。

[http://retropc.net/x68000/software/sharp/human302/](http://retropc.net/x68000/software/sharp/human302/)

先ほど新しく作成したフォルダにコピーし、ターミナルから 7z もしくは lha で展開します。


![](https://github.com/tantanGH/distribution/raw/main/images/xeij17.png)

XEiJ上で ファイル → HFS から今ファイルを展開したフォルダの中にある HUMAN.SYS を選択し、「ここから再起動」を押します。


![](https://github.com/tantanGH/distribution/raw/main/images/xeij18.png)

HFSから起動することができました。再びドライブレターが変わってしまいましたので、前回同様に `AUTOEXEC.BAT` を修正します。
macOS側からもファイルが見えているので、macOS上で編集することもできますが、安全のためにX68000側で編集しておきます。

その後、XEiJの 設定 → 起動デバイス メニューから HFS0 を起動ドライブとして選択しておきます。
この状態で再起動すれば、

    A: FDD#1
    B: FDD#2
    C: HFS
    D: HDD (以前起動用に作ったもの)

というドライブの並びになっています。

これで macOS側とのファイルのやり取りができるようになりました。
D: の HDDイメージについては ファイル → SCSI のメニューから外し、新しくデータ用にイメージファイルを作り直すのが良いと思います。

注意点として、Human68K用のソフトの一部には2GBのサイズのディスクでは正常に動作しないものもあり、中には暴走してディスク内容を壊してしまうものもあります。必ずホスト側のフォルダは新規に作成し、他に影響が出ないようにしてください。

また、起動はあくまでHDDイメージから行い、HFSは起動ディスクとしては使わずにファイルのやり取り目的だけに留めるやり方もあります。
自分はこの形態で使っています。理由は上記の通り、誤動作するソフトウェアが多かっためです(特にファイラーの類)。

ただ、これはXEiJで標準的にサポートされている方法ではないようなので、ここでは詳細は控えます。

---

