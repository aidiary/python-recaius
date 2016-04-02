# -*- coding: utf-8 -*-
import sys
import wave
import json
import urllib.request
import pyaudio


class RecaiusTTS(object):
    """Speech Synthesizer by RECAIUS-dev API"""
    URL = 'https://try-api.recaius.jp/tts/v1/plaintext2speechwave'

    speaker2info = {
        'itaru' : ('ja_JP', 'ja_JP-M0001-H00T'),
        'hiroto': ('ja_JP', 'ja_JP-M0002-H01T'),
        'moe'   : ('ja_JP', 'ja_JP-F0005-U01T'),
        'sakura': ('ja_JP', 'ja_JP-F0006-C53T'),
    }


    def __init__(self, recaius_id, recaius_password):
        self._values = {}

        # user settings
        self._values['id'] = recaius_id
        self._values['password'] = recaius_password

        # default settings
        lang, speaker_id = self.speaker2info['sakura']
        self._values['lang'] = lang
        self._values['speaker_id'] = speaker_id
        self._values['codec'] = 'audio/x-linear'  # for pyaudio

    def reset(self):
        pass

    def speaker(self, speaker):
        if not speaker in spaker2info:
            raise RecaiusTTSException('Unknown speaker: %s' % speaker)

        lang, speaker_id = self.speaker2info[speaker]
        self._values['lang'] = lang
        self._values['speaker_id'] = speaker_id

        return self

    def emotion(self, emotion, level):
        return self

    def speed(self, speed):
        return self

    def pitch(self, pitch):
        return self

    def depth(self, pitch):
        return self

    def volume(self, pitch):
        return self

    def send_request(self):
        # check necessary parameters
        if not 'id' in self._values:
            raise RecaiusTTSException('Missing parameter: id')
        if not 'password' in self._values:
            raise RecaiusTTSException('Missing parameter: password')
        if not 'plain_text' in self._values:
            raise RecaiusTTSException('Missing parameter: plain_text')
        if not 'lang' in self._values:
            raise RecaiusTTSException('Missing parameter: lang')
        if not 'speaker_id' in self._values:
            raise RecaiusTTSException('Missing parameter: speaker_id')

        headers = {'Content-Type': 'application/json'}
        data = json.dumps(self._values)
        data = data.encode('utf-8')
        req = urllib.request.Request(self.URL, data, headers)
        response = urllib.request.urlopen(req)

        return response

    def speak(self, plain_text):
        temp = 'temp.wav'
        self.save_wav(plain_text, temp)

        w = wave.open(temp)
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(w.getsampwidth()),
            channels=w.getnchannels(),
            rate=w.getframerate(),
            output=True)
        chunk = 1024
        data = w.readframes(chunk)
        while data:
            stream.write(data)
            data = w.readframes(chunk)
        stream.close()
        p.terminate()

    def save_wav(self, plain_text, wavefile):
        self._values['plain_text'] = plain_text

        response = self.send_request()
        if response.code == 200:
            with open(wavefile, "wb") as fp:
                fp.write(response.read())


class RecaiusTTSException(Exception):
    pass


if __name__ == '__main__':
    recaius_id = ''
    recaius_password = ''
    rectts = RecaiusTTS(recaius_id, recaius_password)
    rectts.speak(u'こんにちはお元気ですか？')
