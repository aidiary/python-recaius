# -*- coding: utf-8 -*-
from recaius.tts import RecaiusTTS
from settings import TTS_ID, TTS_PASSWORD

# 登録時に発行された自分のIDとパスワードを設定
rec = RecaiusTTS(TTS_ID, TTS_PASSWORD)

# デフォルトの話者はsakura
rec.speak('あらゆる現実をすべて自分のほうへねじ曲げたのだ。')
rec.speaker('moe').speak('嬉しいはずがゆっくり寝てもいられない。')
rec.speaker('hiroto').speak('テレビゲームやパソコンでゲームをして遊ぶ。')
rec.speaker('itaru').speak('救急車が十分に動けず救助作業が遅れている。')

# sakuraは感情音声が使える
rec.speaker('sakura')
rec.emotion('happy', 100).speak('とってもうれしい。')
rec.emotion('angry', 100).speak('ふざけないでください。')
rec.emotion('sad', 100).speak('悲しいことがありました。')
rec.emotion('fear', 100).speak('怖いこと言わないでよ。')
rec.emotion('tender', 100).speak('どうしましたか？')

# 設定した感情をリセット
rec.reset_emotions()

rec.speaker('moe')
rec.speed(-10).speak('ゆっくりです。')
rec.speed(10).speak('早口です。')

# 設定したパラメータをリセット
rec.reset_parameters()

rec.speaker('sakura')
rec.pitch(-10).speak('低い声です。')
rec.pitch(10).speak('高い声です。')
rec.reset_parameters()

rec.speaker('itaru')
rec.depth(-4).speak('細い声です。')
rec.depth(4).speak('太い声です。')
rec.reset_parameters()

rec.speaker('hiroto')
rec.volume(-40).speak('小さい声です。')
rec.volume(50).speak('大きい声です。')
rec.reset_parameters()

# ファイルに保存する
rec.speaker('sakura')
rec.speed(-3).pitch(8).depth(-2).volume(30).speak('どんな声になるのかな？。')
rec.save_wav('音声をファイルに保存します。', 'output.wav')
rec.reset_parameters()
