# -*- coding: utf-8 -*-
import os
import wave
import json
import urllib.request
import pyaudio
from settings import HTTP_PROXY, HTTPS_PROXY

TTS_URL = "https://try-api.recaius.jp/tts/v1/"

class RecaiusTTS(object):
    """Speech Synthesizer by RECAIUS-dev API"""
    speaker2info = {
        'itaru': ('ja_JP', 'ja_JP-M0001-H00T'),
        'hiroto': ('ja_JP', 'ja_JP-M0002-H01T'),
        'moe': ('ja_JP', 'ja_JP-F0005-U01T'),
        'sakura': ('ja_JP', 'ja_JP-F0006-C53T'),
        'jane': ('en_US', 'en_US-F0001-H00T'),
        'nicole': ('fr_FR', 'fr_FR-F0001-H00T'),
        'miyon': ('ko_KR', 'ko_KR-F0001-H00T'),
        'linly': ('zh_CN', 'zh_CN-en_US-F0002-H00T')
    }

    def __init__(self, recaius_id, recaius_password):
        self.recaius_id = recaius_id
        self.recaius_password = recaius_password

        self._values = dict()
        self._values['id'] = self.recaius_id
        self._values['password'] = self.recaius_password

        # default settings
        lang, speaker_id = self.speaker2info['sakura']
        self._values['lang'] = lang
        self._values['speaker_id'] = speaker_id
        self._values['codec'] = 'audio/x-linear'  # for pyaudio

        self.reset_parameters()

    def clear_parameters(self):
        self._values = dict()
        self._values['id'] = self.recaius_id
        self._values['password'] = self.recaius_password

    def reset_parameters(self):
        delete_keys = ['speed', 'pitch', 'depth', 'volume']
        for k in delete_keys:
            if k in self._values:
                del self._values[k]

    def reset_emotions(self):
        delete_keys = ['happy', 'angry', 'sad', 'fear', 'tender']
        for k in delete_keys:
            if k in self._values:
                del self._values[k]

    def speaker(self, speaker):
        if speaker in self.speaker2info:
            lang, speaker_id = self.speaker2info[speaker]
            self._values['lang'] = lang
            self._values['speaker_id'] = speaker_id
        else:
            raise RecaiusTTSException('Unknown speaker: %s' % speaker)
        return self

    def emotion(self, emotion, level):
        self.reset_emotions()
        if emotion in ['happy', 'angry', 'sad', 'fear', 'tender']:
            self._values[emotion] = level
        else:
            raise RecaiusTTSException('Unknown emotion: %s' % emotion)
        return self

    def speed(self, speed):
        if -10 <= speed <= 10:
            self._values["speed"] = speed
        else:
            raise RecaiusTTSException('Invalid speed: %d [-10, 10]' % speed)
        return self

    def pitch(self, pitch):
        if -10 <= pitch <= 10:
            self._values["pitch"] = pitch
        else:
            raise RecaiusTTSException('Invalid pitch: %d [-10, 10]' % pitch)
        return self

    def depth(self, depth):
        if -4 <= depth <= 4:
            self._values["depth"] = depth
        else:
            raise RecaiusTTSException('Invalid depth: %d [-4, 4]' % depth)
        return self

    def volume(self, volume):
        if -50 <= volume <= 50:
            self._values["volume"] = volume
        else:
            raise RecaiusTTSException('Invalid volume: %d [-50, 50]' % volume)
        return self

    def speak(self, text, is_phonetic=False):
        temp = 'temp.wav'
        self.save_wav(text, temp, is_phonetic)

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

    def save_wav(self, text, wave_file, is_phonetic=False):
        if is_phonetic:
            self._values['phonetic_text'] = text
        else:
            self._values['plain_text'] = text

        response = self._text2speechwave(is_phonetic)
        if response.code == 200:
            with open(wave_file, "wb") as fp:
                fp.write(response.read())
        else:
            raise RecaiusTTSException('ERROR: response code: %d' % response.code)

    def get_speaker_list(self):
        temp_values = dict()
        temp_values['id'] = self.recaius_id
        temp_values['password'] = self.recaius_password

        if HTTP_PROXY:
            self._set_proxy()

        headers = {'Content-Type': 'application/json'}
        data = json.dumps(temp_values)
        data = data.encode('utf-8')
        req = urllib.request.Request(TTS_URL + 'get_speaker_list', data, headers)
        response = urllib.request.urlopen(req)

        if response.code == 200:
            result = response.read().decode('utf-8')
        else:
            raise RecaiusTTSException('ERROR: response code: %d' % response.code)

        return result

    def get_phonetic(self, plain_text, lang):
        temp_values = dict()
        temp_values['id'] = self.recaius_id
        temp_values['password'] = self.recaius_password
        temp_values['plain_text'] = plain_text
        temp_values['lang'] = lang

        if HTTP_PROXY:
            self._set_proxy()

        headers = {'Content-Type': 'application/json'}
        data = json.dumps(temp_values)
        data = data.encode('utf-8')
        req = urllib.request.Request(TTS_URL + 'plaintext2phonetictext', data, headers)
        response = urllib.request.urlopen(req)

        if response.code == 200:
            phonetic_text = response.read().decode('utf-8')
        else:
            raise RecaiusTTSException('ERROR: response code: %d' % response.code)

        return phonetic_text

    def _set_proxy(self):
        proxy_support = urllib.request.ProxyHandler({'http': HTTP_PROXY,
                                                     'https': HTTPS_PROXY})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

    def _text2speechwave(self, is_phonetic=False):
        # check necessary parameters
        if 'id' not in self._values:
            raise RecaiusTTSException('Missing parameter: id')
        if 'password' not in self._values:
            raise RecaiusTTSException('Missing parameter: password')
        if is_phonetic:
            if 'phonetic_text' not in self._values:
                raise RecaiusTTSException('Missing parameter: phonetic_text')
        else:
            if 'plain_text' not in self._values:
                raise RecaiusTTSException('Missing parameter: plain_text')
        if 'lang' not in self._values:
            raise RecaiusTTSException('Missing parameter: lang')
        if 'speaker_id' not in self._values:
            raise RecaiusTTSException('Missing parameter: speaker_id')

        if HTTP_PROXY:
            self._set_proxy()

        if is_phonetic:
            function_name = 'phonetictext2speechwave'
        else:
            function_name = 'plaintext2speechwave'

        headers = {'Content-Type': 'application/json'}
        data = json.dumps(self._values)
        data = data.encode('utf-8')
        req = urllib.request.Request(TTS_URL + function_name, data, headers)
        response = urllib.request.urlopen(req)

        return response

class RecaiusTTSException(Exception):
    pass

if __name__ == '__main__':
    from settings import TTS_ID, TTS_PASSWORD
    rec = RecaiusTTS(TTS_ID, TTS_PASSWORD)
    rec.speak("ｺﾚﾜ/ﾖ'ﾐ ｼｭ%ﾄｸﾉ ﾃ'ｽ%ﾄﾃﾞｽ%.", is_phonetic=True)
