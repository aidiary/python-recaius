# -*- coding: utf-8 -*-
import wave
import json
import requests
import pyaudio
from settings import HTTP_PROXY, HTTPS_PROXY

ASR_URL = "https://try-api.recaius.jp/asr/v1/"

class RecaiusASR(object):
    """Speech Recognizer by RECAIUS-dev API"""

    def __init__(self, recaius_id, recaius_password, lang):
        # TODO: Use proper id and password automatically according to lang
        self.recaius_id = recaius_id
        self.recaius_password = recaius_password
        self.lang = lang

        self._values = dict()
        self._values['id'] = self.recaius_id
        self._values['password'] = self.recaius_password

        model = dict()
        if self.lang == 'ja_JP':
            model['model_id'] = 1
        elif self.lang == 'en_US':
            model['model_id'] = 5
        elif self.lang == 'zh_CN':
            model['model_id'] = 7

        self._values['model'] = model

        # set proxies
        self.proxies = {
            'http': HTTP_PROXY,
            'https': HTTPS_PROXY,
        }

    def recognize(self, wave_file):
        uuid = self._login()
        print("uuid:", uuid)

        wf = wave.open(wave_file)

        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)
        chunk = 31250
        data = wf.readframes(chunk)
        voice_id = 1
        while data != b'':
            response = self._voice(uuid, voice_id, data)
            print("%d:" % voice_id, len(data), response)
            data = wf.readframes(chunk)
            voice_id += 1
        response = self._voice(uuid, voice_id, data)
        print("%d:" % voice_id, len(data), response)
        response = self._result(uuid)
        print("==>", response)
        self._logout(uuid)

    def _login(self):
        # check necessary parameters
        if 'id' not in self._values:
            raise RecaiusASRException('Missing parameter: id')
        if 'password' not in self._values:
            raise RecaiusASRException('Missing parameter: password')
        if 'model' not in self._values:
            raise RecaiusASRException('Missing parameter: model')

        headers = {'Content-Type': 'application/json'}
        data = json.dumps(self._values)
        data = data.encode('utf-8')
        response = requests.post(ASR_URL + 'login', data=data, headers=headers, proxies=self.proxies)
        uuid = response.text

        return uuid

    def _logout(self, uuid):
        values = dict()
        values['uuid'] = uuid

        headers = {'Content-Type': 'application/json'}
        data = json.dumps(values)
        data = data.encode('utf-8')
        response = requests.post(ASR_URL + uuid + '/logout', data=data, headers=headers, proxies=self.proxies)
        uuid = response.text

        return

    def _voice(self, uuid, voice_id, pcm_data):
        files = {'voice': ('dummy.wav', pcm_data, 'application/octet-stream')}
        data = {'voiceid': voice_id}
        response = requests.put(ASR_URL + uuid + '/voice', files=files, data=data, proxies=self.proxies)
        return response.status_code, response.text

    def _result(self, uuid):
        response = requests.get(ASR_URL + uuid + '/result', proxies=self.proxies)
        return response.status_code, response.text

class RecaiusASRException(Exception):
    pass

if __name__ == '__main__':
    from settings import ASR_ID, ASR_PASSWORD
    rec = RecaiusASR(ASR_ID, ASR_PASSWORD, 'ja_JP')
    rec.recognize('../sample.wav')
