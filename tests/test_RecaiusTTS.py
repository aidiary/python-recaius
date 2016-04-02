# -*- coding: utf-8 -*-
import unittest
from recaius.RecaiusTTS import RecaiusTTS


class RecaiusTTSTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = RecaiusTTS('YOUR_ID', 'YOUR_PASSWORD')

    def setUp(self):
        self.rec.reset()

    def test_speaker(self):
        self.rec.speak('サクラです。')
        self.rec.speaker('hiroto').speak('ヒロトです。')

    def test_emotion(self):
        self.rec.speaker('sakura').emotion('happy', 100).speak('うれしいです。')
        self.rec.speaker('sakura').emotion('angry', 100).speak('怒ってます。')
        self.rec.speaker('sakura').emotion('sad', 100).speak('悲しいです。')

    def test_speed(self):
        self.rec.speaker('moe')
        self.rec.speed(-10).speak('ゆっくりです。')
        self.rec.speed(10).speak('早口です。')

    def test_pitch(self):
        self.rec.pitch(-10).speak('低い声です。')
        self.rec.pitch(10).speak('高い声です。')

    def test_depth(self):
        self.rec.depth(-4).speak('細い声です。')
        self.rec.depth(4).speak('太い声です。')

    def test_volume(self):
        self.rec.volume(-40).speak('小さい声です。')
        self.rec.volume(50).speak('大きい声です。')


if __name__ == '__main__':
    unittest.main()
