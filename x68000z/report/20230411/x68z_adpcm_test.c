#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <iocslib.h>
#include <doslib.h>

#define ADPCM_BUFFER_LEN (0xff00)

#define REG_DMAC_CH3_BTC (0xE840C0 + 0x1A)
#define REG_DMAC_CH3_BAR (0xE840C0 + 0x1C)

// abort vector handler
static void abort_application() {

  // stop ADPCM
  ADPCMMOD(0);

  exit(1);
}

int32_t main(int32_t argc, uint8_t* argv[]) {

  int32_t rc = -1;

  if (argc < 3) {
    printf("x68z_adpcm_test <file.pcm> <1:array-chain 2:linked-array-chain>\n");
    goto exit;
  }

  struct CHAIN ch[2];

  ch[0].adr = (uint32_t)MALLOC(ADPCM_BUFFER_LEN);
  ch[0].len = ADPCM_BUFFER_LEN;

  ch[1].adr = (uint32_t)MALLOC(ADPCM_BUFFER_LEN);
  ch[1].len = ADPCM_BUFFER_LEN;

  struct CHAIN2 ch_tbl[2];
  
  ch_tbl[0].adr = ch[0].adr;
  ch_tbl[0].len = ch[0].len;
  ch_tbl[0].next = &(ch_tbl[1]);
  
  ch_tbl[1].adr = ch[1].adr;
  ch_tbl[1].len = ch[1].len;
  ch_tbl[1].next = NULL;
  
  FILE* fp = fopen(argv[1],"rb");
  if (fp == NULL) {
    printf("error: pcm file open error.\n");
    goto exit;
  }
  fread((void*)ch[0].adr, 1, ADPCM_BUFFER_LEN, fp);
  fread((void*)ch[1].adr, 1, ADPCM_BUFFER_LEN, fp);
  fclose(fp);

  int16_t play_mode = atoi(argv[2]);
  if (play_mode < 0 || play_mode > 2) {
    printf("error: unknown play mode.\n");
    goto exit;
  }

  // set abort vectors
  uint32_t abort_vector1 = INTVCS(0xFFF1, (int8_t*)abort_application);
  uint32_t abort_vector2 = INTVCS(0xFFF2, (int8_t*)abort_application);  

  ADPCMMOD(0);

  int16_t adpcm_mode = 4 * 256 + 3;
  if (play_mode == 0) {
    ADPCMOUT((uint8_t*)ch[0].adr, adpcm_mode, ADPCM_BUFFER_LEN);
  } else if (play_mode == 1) {
    ADPCMAOT(ch, adpcm_mode, 2);
  } else {
    ADPCMLOT(ch_tbl, adpcm_mode);
  }

  // wait 500msec
  for (int32_t t0 = ONTIME(); ONTIME() < t0 + 50;) {}

  // initial actual BAR
  void* dmac_bar = (void*)B_LPEEK((uint32_t*)REG_DMAC_CH3_BAR); 

  // expected BAR
  void* expected_dmac_bar = NULL;
  if (play_mode == 1) {
    expected_dmac_bar = (void*)&(ch[0]) + 6;
  } else if (play_mode == 2) {
    expected_dmac_bar = (void*)ch_tbl[0].next;
  }

  // extected BTC
  uint16_t expected_dmac_btc = 0;
  if (play_mode == 1) {
    expected_dmac_btc = 1;
  }
  
  while (ADPCMSNS() != 0) {

    // wait 100msec
    for (int32_t t0 = ONTIME(); ONTIME() < t0 + 10;) {}

    // current BAR
    void* cur_dmac_bar = (void*)B_LPEEK((uint32_t*)REG_DMAC_CH3_BAR);

    // current BTC
    uint16_t cur_dmac_btc = (uint16_t)B_WPEEK((uint16_t*)REG_DMAC_CH3_BTC);

    // check buffer flip
    if (cur_dmac_bar != dmac_bar) {
      printf("buffer flipped.\n");
      dmac_bar = cur_dmac_bar;
      if (play_mode == 1) {
        expected_dmac_bar = (void*)&(ch[1]) + 6;
        expected_dmac_btc--;
      } else if (play_mode == 2) {
        expected_dmac_bar = (void*)ch_tbl[1].next;
      }
    }

    // expected and actual BAR
    printf("expected BAR = %X  expected BTC = %d  actual BAR = %X  actual BTC = %d\n", 
            expected_dmac_bar, expected_dmac_btc, cur_dmac_bar, cur_dmac_btc);
  }

  MFREE(ch[0].adr);
  MFREE(ch[1].adr);

  ADPCMMOD(0);

  // resume abort vectors
  INTVCS(0xFFF1, (int8_t*)abort_vector1);
  INTVCS(0xFFF2, (int8_t*)abort_vector2);  

  rc = 0;

exit:

  return rc;
}

