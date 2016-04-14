# -*- coding: utf-8 -*-
import wave
import json
import requests
import pyaudio
from settings import HTTP_PROXY, HTTPS_PROXY

ASR_URL = "https://try-api.recaius.jp/asr/v1/"
MAX_QUERY = 10

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
        result_recognize = []

        uuid = self._login()
        print("login: uuid=%s" % uuid)

        wf = wave.open(wave_file)

        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

        # send speech data
        chunk = 31250
        data = wf.readframes(chunk)
        voice_id = 1
        while data != b'':
            response = self._voice(uuid, voice_id, data)
            if response.status_code == 204:
                continue

            json_result = json.loads(response.text)
            print(voice_id, response.status_code, json_result)

            # add final recognition result if 'RESULT' is contained
            for elm in json_result:
                if elm[0] == 'RESULT':
                    result_recognize.append(elm[1])

            data = wf.readframes(chunk)
            voice_id += 1

        # send finalize signal
        self._voice(uuid, voice_id, b'')

        # get recognition result
        num_query = 0
        while num_query < MAX_QUERY:
            response = self._result(uuid)
            if response.status_code == 204:
                num_query += 1
                continue
            json_result = json.loads(response.text)
            print(voice_id, response.status_code, json_result)

            # add final recognition result if 'RESULT' is contained
            for elm in json_result:
                if elm[0] == 'RESULT':
                    result_recognize.append(elm[1])
                    break

            num_query += 1

        # final result
        print("====>", "".join(result_recognize))

        self._logout(uuid)
        print("logout")

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

        return

    def _voice(self, uuid, voice_id, pcm_data):
        files = {'voice': ('dummy.wav', pcm_data, 'application/octet-stream')}
        data = {'voiceid': voice_id}
        response = requests.put(ASR_URL + uuid + '/voice', files=files, data=data, proxies=self.proxies)
        return response

    def _result(self, uuid):
        response = requests.get(ASR_URL + uuid + '/result', proxies=self.proxies)
        return response

class RecaiusASRException(Exception):
    pass

if __name__ == '__main__':
    from settings import ASR_ID, ASR_PASSWORD
    rec = RecaiusASR(ASR_ID, ASR_PASSWORD, 'ja_JP')
    rec.recognize('../recaius_test.wav')
