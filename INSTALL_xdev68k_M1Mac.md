# xdev68k install guide for M1 Mac

### xdev68k

[xdev68k](https://github.com/yosshin4004/xdev68k)はよっしんさんが構築されているX680x0向けのクロス開発環境です。
VSCodeをはじめ、普段使い慣れた最新の開発環境のエディタを使える、最新の性能のCPUでコンパイル・リンクまで行い、.X形式の実行ファイルまで作成することができるなど、非常に多くのメリットがあります。

自分がこれを M1 MacBook に導入した際(2022年12月)、いくつかの変更が必要だったので、覚書として記録しておきます。

### 環境

- MacBook Air (M1,2020)
- macOS 13.1 (Ventura)
- Memory 8GB

### 手順

1. Unix 互換環境のインストールと環境構築

Xcode command line tool が入ってなければ導入。
    xcode-select --install

[Homebrew](https://brew.sh/)が入ってなければ導入。

brewでいくつか追加導入

    brew install cmake
    brew install libiconv
    brew install wget
    brew install realpath
    brew install coreutils
    brew install automake

2. xdev68k gitリポジトリのclone

特にひっかかることはない

3. クロスコンパイラのビルド

xdev68k が採用している gcc-10.2 には Apple M1 上でのクロスコンパイラビルドに問題があり、正常にビルドが完了できません。
このためには、以下の2ファイルの一部を書き換えてやる必要があります。
    gcc/config/aarch64/aarch64.h
    gcc/config/host-darwin.c

修正の仕方は[ここ](https://dev.haiku-os.org/attachment/ticket/17191/apple_silicon.patch)の通りにやれば大丈夫です。

具体的には一度 `./build_m68k-toolchain.sh` を流し error で途中終了したら、上記の2ファイルをカレントディレクトリにコピーし、エディタで修正します。
さらに `./build_m68k-toolchain.sh` の以下の部分に2行追加して、gccの本家アーカイブの展開直後に2ファイルを差し替えるようにします。

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

これでクロスコンパイラのビルドが完了できます。


