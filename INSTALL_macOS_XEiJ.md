# macOS ユーザのための X680x0 エミュレータ XEiJ 導入ガイド (工事中)

2023.1 tantan

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

このドキュメントは macOS にこの XEiJ を導入する際のいくつかのポイントを覚書として残しておくものです。

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

まずは XEiJ と同じ鎌田さんのサイトで保守されているライブラリから、Human68k のFDディスクイメージをダウンロード

* [http://retropc.net/x68000/software/sharp/human302/](http://retropc.net/x68000/software/sharp/human302/)

このイメージは LZH 形式で圧縮されています。macOSのFinderでは
