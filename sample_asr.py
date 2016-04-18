# -*- coding: utf-8 -*-
from recaius.asr import RecaiusASR
from settings import ASR_ID, ASR_PASSWORD

rec = RecaiusASR(ASR_ID, ASR_PASSWORD)
rec.set_lang('ja_JP')

uuid = rec.login()

# speech recognition from wave file
result = rec.recognize(uuid, 'recaius_test.wav')
print(result)

rec.logout(uuid)
