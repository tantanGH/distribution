# xdev68k install guide for M1 Mac

### xdev68k

[xdev68k](https://github.com/yosshin4004/xdev68k)はよっしんさんが構築されているX680x0対応クロス開発環境です。

- VSCodeをはじめ、普段使い慣れた最新の開発環境のエディタを使える
- 最新の性能のCPUでコンパイル・リンクまで行い、.X形式の実行ファイルまで作成できる

など非常に多くのメリットがあります。

自分がこれを M1 MacBook に導入した際(2022.12)、いくつかの手作業が必要だったので、覚書として記録しておきます。

### 自分の環境

- MacBook Air (M1,2020)
- macOS 13.1 (Ventura)
- Memory 8GB

### 手順ごとのポイント

1. Unix 互換環境のインストールと環境構築

Xcode command line tool が入ってなければ導入。

    xcode-select --install

[Homebrew](https://brew.sh/) が入ってなければ導入。

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brewでいくつか必要なものを導入

    brew install cmake
    brew install libiconv
    brew install wget
    brew install realpath
    brew install coreutils
    brew install automake
    brew install p7zip


2. xdev68k gitリポジトリのclone

特にひっかかることはない


3. クロスコンパイラのビルド (./build_m68k-toolchain.sh)

3.1 未定義変数のチェック

macOS の bash は未定義変数チェックの -v が使えないので、239行目付近を以下のように修正する。

    #if [ ! -v newlib_cflags ]; then
	    newlib_cflags=""
    #fi

3.2 gccのバージョン

gcc 10.x.0 は M1 Mac に対応できていないので 12.2.0 に変更する。60行目付近を以下のように修正する。

    GCC_VERSION="12.2.0"
    GCC_ARCHIVE="gcc-${GCC_VERSION}.tar.gz"
    GCC_SHA512SUM="36ab2267540f205b148037763b3806558e796d564ca7831799c88abcf03393c6dc2cdc9d53e8f094f6dc1245e47a406e1782604eb9d119410d406032f59c1544"

どうしても 10.2.0 のままで行く場合は以下の2ファイルの一部を書き換える。

    gcc/config/aarch64/aarch64.h
    gcc/config/host-darwin.c

修正の仕方は [https://dev.haiku-os.org/attachment/ticket/17191/apple_silicon.patch](https://dev.haiku-os.org/attachment/ticket/17191/apple_silicon.patch) の通りにやればok。

具体的には一度 `./build_m68k-toolchain.sh` を流し error で途中終了したら、上記の2ファイルをカレントディレクトリにコピーし、エディタで修正。
さらに `./build_m68k-toolchain.sh` の以下の部分に2行追加して、gccの本家アーカイブの展開直後に2ファイルを差し替えるようにする。
コピー元のパスは適宜修正。絶対パスが確実。

    cd ${DOWNLOAD_DIR}
    if ! [ -f "${GCC_ARCHIVE}" ]; then
        wget ${GCC_URL}
    fi
    if [ $(sha512sum ${GCC_ARCHIVE} | awk '{print $1}') != ${GCC_SHA512SUM} ]; then
      echo "SHA512SUM verification of ${GCC_ARCHIVE} failed!"
      exit
    fi
    tar xvf ${GCC_ARCHIVE} -C ${SRC_DIR}

    cp -p ~/xdev68k/aarch64.h ${SRC_DIR}/${GCC_DIR}/gcc/config/aarch64/aarch64.h
    cp -p ~/xdev68k/host-darwin.c ${SRC_DIR}/${GCC_DIR}/gcc/config/host-darwin.c

    cd ${SRC_DIR}/${GCC_DIR}
    ./contrib/download_prerequisites



4. ユーティリティのインストール (./install_xdev68k-utils.sh)

4.1 --preserve-timestamp

macOS 付属の cp は `--preserve-timestamps` をサポートしていないので、`./build_m68k-toolchain.sh` の中にある
`cp` コマンドの `--preserve-timestamps` をすべて `-p` に書き換える。


4.2 LHA 展開

名前にSJIS文字の含まれたファイルをrun68経由のlhaで展開しようとすると失敗するので、103行目のLHA=の行を以下のように変更して、LZHの展開に7zを使うようにする。

    LHA=7z

4.3 ヘッダファイル変換

SJIS文字を含む .h ファイルの変換に失敗し、EOFが最後に残ってしまうものがあるので手で修正します。



5. 環境変数設定

あまり長いと HAS/HLKがエラーとなってしまう場合があるので、シンボリックリンクなどを使って適宜短縮します。

6. Hello World

やはり SJIS の入ったファイルがうまくいかないようです。とりあえず手で修正し、`-finput-charset=cp932` のコンパイラオプションを外してしまうとうまくいきます。
ただ、これだと後々日本語の入ったアプリケーションを作ろうと思った時困りますね。今後さらに確認しようと思います。


2022.12.23 tantan


