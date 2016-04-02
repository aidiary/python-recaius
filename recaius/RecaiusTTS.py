# -*- coding: utf-8 -*-
import os
import wave
import json
import urllib.request
import pyaudio


class RecaiusTTS(object):
    """Speech Synthesizer by RECAIUS-dev API"""
    URL = 'https://try-api.recaius.jp/tts/v1/plaintext2speechwave'

    speaker2info = {
        'itaru': ('ja_JP', 'ja_JP-M0001-H00T'),
        'hiroto': ('ja_JP', 'ja_JP-M0002-H01T'),
        'moe': ('ja_JP', 'ja_JP-F0005-U01T'),
        'sakura': ('ja_JP', 'ja_JP-F0006-C53T'),
    }

    def __init__(self, recaius_id, recaius_password):
        self._values = dict()
        self._values['id'] = recaius_id
        self._values['password'] = recaius_password
        self.reset()

    def reset(self):
        all_keys = ['speed', 'pitch', 'depth', 'volume',
                    'happy', 'angry', 'sad', 'fear', 'tender']
        for k in all_keys:
            if k in self._values:
                del self._values[k]

        # default settings
        lang, speaker_id = self.speaker2info['sakura']
        self._values['lang'] = lang
        self._values['speaker_id'] = speaker_id
        self._values['codec'] = 'audio/x-linear'  # for pyaudio

    def speaker(self, speaker):
        if speaker in self.speaker2info:
            lang, speaker_id = self.speaker2info[speaker]
            self._values['lang'] = lang
            self._values['speaker_id'] = speaker_id
        else:
            raise RecaiusTTSException('Unknown speaker: %s' % speaker)
        return self

    def emotion(self, emotion, level):
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

    def send_request(self):
        # check necessary parameters
        if 'id' not in self._values:
            raise RecaiusTTSException('Missing parameter: id')
        if 'password' not in self._values:
            raise RecaiusTTSException('Missing parameter: password')
        if 'plain_text' not in self._values:
            raise RecaiusTTSException('Missing parameter: plain_text')
        if 'lang' not in self._values:
            raise RecaiusTTSException('Missing parameter: lang')
        if 'speaker_id' not in self._values:
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
        os.remove(temp)

    def save_wav(self, plain_text, wave_file):
        self._values['plain_text'] = plain_text

        response = self.send_request()
        if response.code == 200:
            with open(wave_file, "wb") as fp:
                fp.write(response.read())


class RecaiusTTSException(Exception):
    pass
