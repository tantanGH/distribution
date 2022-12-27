# xdev68k install guide for M1 Mac

### xdev68k

[xdev68k](https://github.com/yosshin4004/xdev68k)はよっしんさんが構築されているX680x0対応クロス開発環境です。

- VSCodeをはじめ、普段使い慣れた最新の開発環境のエディタを使える
- 最新の性能のCPUでコンパイル・リンクまで行い、.X形式の実行ファイルまで作成できる

など非常に多くのメリットがあります。

自分がこれを M1 MacBook に導入した際(2022.12)、いくつかの手作業が必要だったので、覚書として記録しておきます。

---

### 変更履歴

2022.12.28 tantan 内容更新
2022.12.23 tantan 初版

---

### 自分の環境

- MacBook Air (M1,2020)
- macOS 13.1 (Ventura)
- Memory 8GB

---

### 手順ごとのポイント

### 1. Unix 互換環境のインストールと環境構築

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

---

### 2. xdev68k gitリポジトリのclone

特にひっかかることはない

---

### 3. クロスコンパイラのビルド (./build_m68k-toolchain.sh)

3.1. 未定義変数のチェック

macOS の bash は未定義変数チェックの -v が使えないので、239行目付近を以下のように修正する。

    #if [ ! -v newlib_cflags ]; then
	    newlib_cflags=""
    #fi

3.2. gccのバージョン

gcc 10.x.0 は M1 Mac に対応できていないので 12.2.0 に変更する。60行目付近を以下のように修正する。

    GCC_VERSION="12.2.0"
    GCC_ARCHIVE="gcc-${GCC_VERSION}.tar.gz"
    GCC_SHA512SUM="36ab2267540f205b148037763b3806558e796d564ca7831799c88abcf03393c6dc2cdc9d53e8f094f6dc1245e47a406e1782604eb9d119410d406032f59c1544"

どうしても 10.2.0 のままで行く場合は以下の2ファイルの一部を書き換える必要がある。

    gcc/config/aarch64/aarch64.h
    gcc/config/host-darwin.c

一度 `./build_m68k-toolchain.sh` を流し error で途中終了したら、上記の2ファイルをカレントディレクトリにコピーし、エディタで修正。

修正の内容は [https://dev.haiku-os.org/attachment/ticket/17191/apple_silicon.patch](https://dev.haiku-os.org/attachment/ticket/17191/apple_silicon.patch) を参考にする。

さらに `./build_m68k-toolchain.sh` の以下の部分に2行追加して、gccの本家アーカイブの展開直後に2ファイルを差し替えるようにする。コピー元のパスは適宜修正する。

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

3.3. libiconv の場所

このまま build すると gcc が libiconv を見つけられず cp932 のソースを入力として受け入れられなくなるので、stage2 の configure の最後に `--with-libconv-prefix=/opt/homebrew/opt/libiconv` を追加して brew で入れた libiconv を使うようにする。

    cd ${BUILD_DIR}/${GCC_DIR}_stage2
        `realpath --relative-to=./ ${SRC_DIR}/${GCC_DIR}`/configure \
        --prefix=${INSTALL_DIR} \
        --program-prefix=${PROGRAM_PREFIX} \
        --target=${TARGET} \
        --enable-lto \
        --enable-languages=c,c++ \
        --with-arch=m68k \
        --with-cpu=${WITH_CPU} \
        --with-newlib \
        --enable-interwork \
        --enable-multilib \
        --disable-shared \
        --disable-threads \
        --with-libiconv-prefix=/opt/homebrew/opt/libiconv

---

### 4. ユーティリティのインストール (./install_xdev68k-utils.sh)

4.1. cp のオプション

macOS 付属の cp は `--preserve-timestamps` をサポートしていないので、`./build_m68k-toolchain.sh` の中にある
`cp` コマンドの `--preserve-timestamps` をすべて `-p` に書き換える。


4.2. LHA 展開

名前にSJIS文字の含まれたファイルをrun68経由のlhaで展開しようとすると失敗するので、103行目のLHA=の行を以下のように変更して、LZHの展開に7zを使うようにする。

    LHA=7z

また、LHAを使っている行を以下のように変更する。`-x`は`x`に、`-o=`は`-o`にする。

    ${LHA} x -o${ARCHIVE%.*} ${ARCHIVE}

4.3. ヘッダファイル変換

macOS 付属の `sed` だとSJIS文字を含む .h ファイルの変換に失敗するため、代わりに `perl` を使うようにする。バックスラッシュが一つ減るのに注意。

    for f in * ; do cat $f | perl -pe 's/^\x1a$//g' > $f.tmp && rm $f && mv $f.tmp $f; done

---

### 5. 環境変数設定

あまり長いと HAS/HLKがエラーとなってしまう場合があるので、シンボリックリンクなどを使って適宜短縮する。

---

### 6. Hello World

`-finput-charset=cp932` のコンパイラオプションがあると stdio.h, stdlib.h の utf-8 への変換に失敗する。

workaround: `-finput-charset=cp932` のオプションを外す。

他に手が無いか調査中

---

### 7. 実際の利用

7.1. sys/types.h

X68用以外のソース(zlib等)をコンパイルしようとすると、include/xc/ からではなく m68k-toolchain/m68k-elf/include/ のヘッダを使うケースが出てくる。
`sys/types.h` をincludeすると、`time_t`,`clock_t`の定義がXCと競合する。

workaround: コンパイラオプションに `-D__time_t_defined -D__clock_t_defined` を追加する。

7.2. errno.h

X68用以外のソース(zlib等)をコンパイルしようとすると、include/xc/ からではなく m68k-toolchain/m68k-elf/include/ のヘッダを使うケースが出てくる。
`errno.h` をincludeすると、`wint_t`の定義が未定義と怒られる。

workaround: `include/xc/` の中で `error.h` から `errno.h` へのシンボリックリンクを張る。

7.3. HLK で Out of memory

リンクするオブジェクトの数が多いと Out of memory になることがある。

workaround: リンクだけ Human68k 上で実行する。

7.4. AR.X で不正な .A ファイルが作られる

アーカイブするオブジェクトの数が多いと不正な .A (ほぼ空) が作られることがある。

workaround: アーカイブだけ Human68k 上で実行する。


