# -*- coding: utf-8 -*-
import unittest
from recaius.asr import RecaiusASR
from settings import ASR_ID, ASR_PASSWORD

class RecaiusASRTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.asr = RecaiusASR(ASR_ID, ASR_PASSWORD)

    def setUp(self):
        pass

    def test_recognition(self):
        self.assertEqual(self.asr.recognize('../recaius_test.wav'),
                         'おはようございます。')
