# -*- coding: utf-8 -*-
from recaius.asr import RecaiusASR
from settings import ASR_ID, ASR_PASSWORD

rec = RecaiusASR(ASR_ID, ASR_PASSWORD)
rec.set_lang('ja_JP')

# speech recognition from wave file
result = rec.recognize('./recaius_test.wav')
print(result)
