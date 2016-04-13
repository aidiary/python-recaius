# -*- coding: utf-8 -*-
import unittest
from recaius.tts import RecaiusTTS
from settings import TTS_ID, TTS_PASSWORD

class RecaiusTTSTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = RecaiusTTS(TTS_ID, TTS_PASSWORD)

    def setUp(self):
        self.rec.reset_parameters()
        self.rec.reset_emotions()

    def test_speaker(self):
        self.rec.speak('サクラです。')
        self.rec.speaker('hiroto').speak('ヒロトです。')
        self.rec.speaker('jane').speak('My name is Jane.')
        self.rec.speaker('nicole').speak('Je m\'appelle Nicole.')
        self.rec.speaker('miyon').speak('저는 미연입니다')
        self.rec.speaker('linly').speak('我是鈴麗.')

    def test_emotion(self):
        self.rec.speaker('sakura')
        self.rec.emotion('happy', 100).speak('うれしいです。')
        self.rec.emotion('angry', 100).speak('怒ってます。')
        self.rec.emotion('sad', 100).speak('悲しいです。')

    def test_speed(self):
        self.rec.speaker('moe')
        self.rec.speed(-10).speak('ゆっくりです。')
        self.rec.speed(10).speak('早口です。')

    def test_pitch(self):
        self.rec.speaker('sakura')
        self.rec.pitch(-10).speak('低い声です。')
        self.rec.pitch(10).speak('高い声です。')

    def test_depth(self):
        self.rec.speaker('hiroto')
        self.rec.depth(-4).speak('細い声です。')
        self.rec.depth(4).speak('太い声です。')

    def test_volume(self):
        self.rec.speaker('itaru')
        self.rec.volume(-40).speak('小さい声です。')
        self.rec.volume(50).speak('大きい声です。')

    def test_get_speaker_list(self):
        self.assertEquals(self.rec.get_speaker_list()[2:5], 'xml')

    def test_get_phonetic(self):
        self.assertEqual(self.rec.get_phonetic('これは読み取得のテストです。', 'ja_JP'),
                         "ｺﾚﾜ/ﾖ'ﾐ ｼｭ%ﾄｸﾉ ﾃ'ｽ%ﾄﾃﾞｽ%.")
        self.assertEqual(self.rec.get_phonetic('This is a test.', 'en_US'),
                         '"DIs "Iz "@ #P.#"tEst#E\#')
        self.assertEqual(self.rec.get_phonetic('Ceci est un test.', 'fr_FR'),
                         's@."si "E:t 9~ #P.#"tE:st#E\#')
        self.assertEqual(self.rec.get_phonetic('이것은 테스트 입니다.', 'ko_KR'),
                         '이거슨 테스트 임니다.')
        self.assertEqual(self.rec.get_phonetic('這是一個考驗。', 'zh_CN'),
                         '#Tg#zhe4 #Tv#shi4 #Tm#yi4 #Tg#ge2 #Tv#kao3 #Tg;P.#yan4')

    def test_phonetictext2speechwave(self):
        self.rec.speak("ｺﾚﾜ/ﾖﾐ ｼｭ%ﾄｸﾉ ﾃ'ｽ%ﾄﾃﾞｽ%.", is_phonetic=True)
        self.rec.speak(self.rec.get_phonetic('ありがとうございます。', 'ja_JP'), is_phonetic=True)
        self.rec.speaker('jane').speak('"DIs "Iz "@ #P.#"tEst#E\#', is_phonetic=True)
        self.rec.speaker('nicole').speak('s@."si "E:t 9~ #P.#"tE:st#E\#', is_phonetic=True)
        self.rec.speaker('miyon').speak('이거슨 테스트 임니다.', is_phonetic=True)
        self.rec.speaker('linly').speak('#Tg#zhe4 #Tv#shi4 #Tm#yi4 #Tg#ge2 #Tv#kao3 #Tg;P.#yan4', is_phonetic=True)

if __name__ == '__main__':
    unittest.main()
