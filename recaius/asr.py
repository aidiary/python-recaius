# -*- coding: utf-8 -*-
import wave
import json
import urllib.request
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

        if HTTP_PROXY:
            self._set_proxy()

    def recognize(self, wave_file):
        uuid = self._login()

        w = wave.open(wave_file)
        print('rate:', w.getframerate())

        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(w.getsampwidth()),
            channels=w.getnchannels(),
            rate=w.getframerate(),
            output=True)
        chunk = 999999999
        data = w.readframes(chunk)
        voiceid = 1
        response = self._voice(uuid, voiceid, data)

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
        req = urllib.request.Request(ASR_URL + 'login', data, headers)
        response = urllib.request.urlopen(req)
        uuid = response.read().decode('utf-8')

        return uuid

    def _logout(self, uuid):
        values = dict()
        values['uuid'] = uuid

        headers = {'Content-Type': 'application/json'}
        data = json.dumps(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(ASR_URL + uuid + '/logout', data, headers)
        response = urllib.request.urlopen(req)
        uuid = response.read().decode('utf-8')

        return

    def _voice(self, uuid, voiceid, pcm_data):
        form_data = dict()
        form_data['uuid'] = uuid
        form_data['voiceid'] = voiceid
        form_data['voice'] = pcm_data

        headers = {'Content-Type': 'multipart/form-data'}
        req = urllib.request.Request(ASR_URL + uuid + '/voice', data=form_data, headers=headers, method='PUT')
        response = urllib.request.urlopen(req)

        return response

    def _result(self, uuid):
        pass

    # TODO: Remove dual definition
    def _set_proxy(self):
        proxy_support = urllib.request.ProxyHandler({'http': HTTP_PROXY,
                                                     'https': HTTPS_PROXY})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

class RecaiusASRException(Exception):
    pass

if __name__ == '__main__':
    from settings import ASR_ID, ASR_PASSWORD
    rec = RecaiusASR(ASR_ID, ASR_PASSWORD, 'ja_JP')
    rec.recognize('../recaius_test.wav')
