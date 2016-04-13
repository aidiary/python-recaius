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

if __name__ == '__main__':
    unittest.main()
