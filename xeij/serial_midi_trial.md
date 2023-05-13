### jSerialComm ライブラリを使った XEiJ の RS-MIDI 再生実験

### 目的

XEiJ上でRS-MIDI対応ドライバを使ってMIDI音源実機を鳴らすこと。


### 方法

XEiJのRS232C入出力はXEiJ組み込みのターミナルウィンドゥと接続されている。これは主にデバッグ用途などに使うことが想定されている。

SCC自体のエミュレーションは割り込みも含めてほぼ実装されているので、以下の2箇所にパッチを行う。

1. SCC ch.A コマンドポートに対してWR12,WR13でボーレートを設定している箇所
2. SCC ch.A データポートに対してデータを書き込んでいる箇所

---
0. `RS232CPort.java`

準備として `RS232CPort.java` を作成しておく。読み込みは今回は使わない。データビット数8、ストップビット1、パリティ無し、フロー制御なしは固定とする。

デバイス名は Windows であれば getCommPorts() が動作すると思われるが、macOSだと拾えないようなので決めうちしてる。他の環境ではもちろんこのデバイス名は使えない。

        package xeij;

        public class RS232CPort {

          protected static com.fazecast.jSerialComm.SerialPort comPort = null;
          protected static byte[] read_buffer = new byte [ 64 ];

          static {
        //    comPort = com.fazecast.jSerialComm.SerialPort.getCommPorts()[0];
            comPort = com.fazecast.jSerialComm.SerialPort.getCommPort("/dev/tty.usbserial-AQ02KMMV");
            comPort.setComPortParameters(
                9600,
                8,
                com.fazecast.jSerialComm.SerialPort.ONE_STOP_BIT,
                com.fazecast.jSerialComm.SerialPort.NO_PARITY);
            comPort.setComPortTimeouts(com.fazecast.jSerialComm.SerialPort.TIMEOUT_NONBLOCKING, 0, 0);
            comPort.setFlowControl(com.fazecast.jSerialComm.SerialPort.FLOW_CONTROL_DISABLED);
            comPort.openPort();
          }
          
          public static void setBaudRate(int newBaudRate) {
            comPort.setBaudRate(newBaudRate);
          }
          
          public static void txData(byte d) {
            comPort.writeBytes(new byte[] { d }, 1L);
          }

          public static Byte rxData() {
            if (comPort.bytesAvailable() == 0) {
              return null;
            } else {
              comPort.readBytes(read_buffer, 1);
              return read_buffer[0];
            }
          }
          
        }



1. `MemoryMappedDevice.java`

ボーレート設定変更が入ったら反映させる。

        case 12:  //WR12
          Z8530.scc1BaudRateGen = (Z8530.scc1BaudRateGen & ~0xff) | d;
          Z8530.scc1Interval = XEiJ.TMR_FREQ / ((Z8530.SCC_FREQ / 2 >> Z8530.scc1ClockModeShift) / (Z8530.scc1BaudRateGen + 2));
          RS232CPort.setBaudRate(((Z8530.SCC_FREQ / 2 >> Z8530.scc1ClockModeShift) / (Z8530.scc1BaudRateGen + 2)));
          break;
        case 13:  //WR13
          Z8530.scc1BaudRateGen = d << 8 | (Z8530.scc1BaudRateGen & 0xff);
          Z8530.scc1Interval = XEiJ.TMR_FREQ / ((Z8530.SCC_FREQ / 2 >> Z8530.scc1ClockModeShift) / (Z8530.scc1BaudRateGen + 2));
          RS232CPort.setBaudRate(((Z8530.SCC_FREQ / 2 >> Z8530.scc1ClockModeShift) / (Z8530.scc1BaudRateGen + 2)));
          break;

2. `MemoryMappedDevice.java`

        case Z8530.SCC_1_DATA & 7:  //ポートAデータ書き込み(RS-232C送信)
          //RS232CTerminal.trmPrintSJIS (d);
          RS232CPort.txData((byte)d);
          return;