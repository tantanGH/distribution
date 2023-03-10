# X680x0 と Mac との間でファイル転送する (MO編)

## はじめに

X680x0 実機と Mac との間でファイル転送を行うには複数の方法があります。今回実際に実機とやり取りする必要性に迫られたので、まずは「固い」やり方の一つと思われる **MO (光磁気ディスク)** を使った方法について覚書として記録しておきます。Twitterで教えて頂いた先輩方に改めてお礼申し上げます。

<br/>

なお、誤りなどありましたら遠慮なくお知らせください。(twitter: tantan @snakGH)

---

## ドライブの準備

一つの MOドライブを X680x0 と Mac の間で共用するのはインターフェイスの面で難しいので、X680x0 と Mac に MOドライブをそれぞれ用意する必要があります。

* X680x0 ... SCSI タイプのもの
* Mac ... USB タイプのもの

MOは自分の知らないうちに大容量化が進んでいて、

* 128MB
* 230MB
* 640MB
* 1.3GB

と容量にバリエーションがあります。基本的に後方互換のようですので、中古であれば年式の新しい大容量メディア対応ドライブの方が良いと思います。ただし、X680x0 で1GBを超えるディスクを扱うのは何かと問題があるようなので、実際に使うメディアとしては640MBまでにしておくのが無難です。

### X680x0 用 SCSI MO ドライブ選択のポイント

SCSI MO ドライブの持つ SCSI コネクタは主に次の2種類があります。

* ハーフピッチ 50pin コネクタ
* ハーフピッチ アンフェノール コネクタ

また、X680x0 側の持つ SCSI コネクタは機種により違いがあります。

* SUPER / XVI ... フルピッチ アンフェノール コネクタ
* CompactXVI / X68030 / X68030Compact ... ハーフピッチ アンフェノール コネクタ
* その他拡張SCSIボード(純正,Mach-2等) ... ？(すみません、覚えてません...)

電気的には同じですが、接続の際にはコネクタ形状に適したケーブルの選択が必要です。

自分が中古で入手したドライブは 640MB 対応ドライブで ハーフピッチ 50pin コネクタのものでした。てっきり実機の X68030 もハーフピッチ 50pin だと思っていたら、実際にケーブルを挿す段階になって ハーフピッチ アンフェノール であることに気づきました。慌てて ハーフピッチ 50pin - ハーフピッチ アンフェノール のケーブルも追加で調達することに...。

なお、余計なトラブルの要素を抱えないためにも、変換コネクタではなくケーブル1本で直結が良いと思います。

また、MOドライブ側にはターミネータ(終端抵抗)が必要です。自分はこちらの製品を新品で購入しました。今でも普通に買えることにビックリ。

https://www.sanwa.co.jp/product/syohin?code=KTR-04PMK

### Mac 用 USB MO　ドライブ選択のポイント

USB接続タイプのMOドライブであればほぼ何でも大丈夫だと思います。ただメカ機構がありそれなりに電気は食うと思い、バスパワー方式のものではなくACアダプタ方式のものにしました。


---

## メディアの準備

上にも書いた通り、1GBを超えるディスクでは X680x0 側で様々なトラブルが想定されるので(単に認識するかどうかというだけでなく、各種アプリケーションが対応できているかどうかも含めて)、容量のバランスを考えても 640MB のメディアを使うのがお勧めです。

ちなみにMOメディアはとても堅牢にできており、自分の手元にある約30年前のメディアもすべて問題なく読み書きできました。剥き出しの5インチフロッピーやCD/DVDと違ってシャッター付きの安全なケースに入っており、カビなどもあまり話を聞いたことがありません。

これから新しくメディアを購入する際には「Windowsフォーマット済み」のものを選択します。これはFAT形式でフォーマットされたメディアであり、X680x0 と Mac のどちらでも読み書きすることが可能です。

「Macintoshフォーマット済み」の場合は再フォーマットが必要になります。この時 macOS 付属の「ディスクユーティリティ」で「MS-DOS互換」かつ「マスターブートレコード」を選択して「Windowsフォーマット済み」相当にできるのですが、残念ながらこの方法でフォーマットされたメディアは X680x0 では全く認識できませんでした。

再フォーマットする場合は X680x0 側で後述の **FIM.X** を使って「IBM フォーマット」を行う必要があります。

---

## ソフトウェアの準備

X680x0 側は、以下のソフトウェアを導入しておきます。

* SCSI デバイスドライバ SUSIE.X
* SCSI デバイスIBMフォーマッタ FIM.X
* TwentyOne (改良版)

Vector:
- https://www.vector.co.jp/soft/x68/hardware/se036103.html
- https://www.vector.co.jp/soft/dl/x68/hardware/se019750.html
- https://www.vector.co.jp/soft/x68/util/se014378.html

X68000 LIBRARY:
- http://retropc.net/x68000/software/disk/scsi/susie/
- http://retropc.net/x68000/software/disk/filename/twentyone/

などで入手できます。(2023年現在)

---

## X680x0 から Mac への転送

X680x0 では最大 18+3 小文字ありのファイル名を使うことができますが、MOでのやり取りを前提に書き込む際には 8+3 大文字のみに留めておきます。日本語も避けておきます。

ファイル名以外は特に注意点はありません。Macで問題なく読み出すことができます。ただし、Macで一度でもそのメディアを読ませてしまうと、後述の通り macOSが管理情報を書き込んでしまうので、ライトプロテクトノッチをスライドしておくのが無難です。

---

## Mac から X680x0 への転送

同様に 8+3 大文字のみのファイル名にしておきます。ただし、上記の通り Mac で一度でもそのメディアを読ませてしまうと、以下の管理情報が書き込まれてしまいます。

1. Spotlight 用インデックス 

Spotlight (検索) のためのインデックスを作りにいってしまいます。これが **.Spotlight-V100** というピリオドで始まりハイフンも含む長い名前のフォルダを作ってしまいます。

以下などを参考に、外付けディスクは Spotlight の検索対象から外す設定を行います。
- https://dezisaru.com/imac/4304.html
- https://1010uzu.com/blog/external-hard-drive-wont-eject-due-to-spotlight-on-mac

Terminal などから直接 MO のボリュームにアクセスし、作られてしまったフォルダは削除しておいた方が良いかと思います。

2. 外付けメディアのための管理フォルダ

macOS はもう一つ、**.fseventsd** という名前のフォルダを外付けメディアを挿入するたびに作ってしまいます。これは安全な取り外しができなかった時のために用意されるものらしいのですが、削除してもすぐに作り直されてしまいますので、Mac側から何か持っていこうとした場合はこれはそのままとなります。

X680x0 側では TwentyOne の新しいものを入れておくことでとりあえず無視されるようですので、もしうまくいかない場合は TwentyOne を更新してみてください。

---

## Mac 上での MO メディア取り出し問題 (未解決)

これは X680x0 関係なく、純粋に MacとMac側MOドライブの問題です。macOS上で MO メディアを取り出す場合、
Finder 上に見える MO メディアのイジェクトボタンをポチっとすればウィーンと自動的にメディアが排出され... ないことがあります。
というかされないことの方が多いです。

色々と試したのですが、
 * Finderのアイコンではなく、デスクトップにあるアイコンをゴミ箱に放り込む (効果あり)
 * 一度ログアウトしてみる
 * 一度再起動してみる

など。

また、一度イジェクトボタンを押して macOS上からはアンマウントされてしまったメディアは「ディスクユーティリティ」を使うと再マウントできます。そこでもう一度イジェクトを試みることができます。

どうにもこうにもいかなくなった場合は、macOSシャットダウン後に、イジェクトピンを使って強制排出となります。すでに何度かお世話になってます...

ここまで書いて思い出しましたが、最初にX680x0でかつて使っていた昔のMOメディアをサルベージする際には、イジェクトの問題はありませんでした。それらのMOメディアはすべてライトプロテクトノッチを書き込み禁止にしてありました。このあたりが何か関係しているかもしれません。とはいえ何か新規に Macで書き込もうと思ったらライト許可する必要がありますが...

---

## X680x0 用起動可能 MO メディアを作る

X680x0 の内蔵ハードディスクは HDDそのものももちろん、変換基板で CF/SD などを使っている場合であっても物理的なメディアでエミュレーションしている限り、クラッシュからは逃れられません。変換基板そのものが故障してしまう可能性も考えられます。

このため、せっかくMOを用意したのであれば、起動可能なMOメディアを用意しておき、緊急事態に備えるのがお勧めです。昔やった覚えがうっすらとあったのですが、手順が曖昧でした。Twitterで先輩方に教えて頂きました。本当にありがとうございます。


起動可能なMOメディアを作るには Windowsフォーマット(IBMフォーマット) ではなく、Human68k 付属の **FORMAT.X** を使って装置初期化および領域確保(パーティション作成)を行う必要があります。

この時、**FORMAT.X は 640MB MOメディアを認識してくれません**。ですので、緊急ブートMOメディアは230MBもしくは128MBのメディアにしておくのが無難です。自分は手元にあった中身の不要な128MBメディアを使いました。装置初期化は時間がかかるのでそういう意味でも低容量のメディアにしておいた方が良いかもしれません。

領域確保の際は「システム転送する」を選択しておきます。

再起動してドライブを認識したら、`COPYALL` を使って `\BIN\`, `\SYS\`, `AUTOEXEC.BAT`, `CONFIG.SYS` など起動に必要なファイルをコピーします。

注) 「HDモード」に切り替える必要があるドライブもあるようなのですが、詳細はわかりません。すみません。

---

2023.01.15 初版 tantan