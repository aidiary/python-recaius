# -*- coding: utf-8 -*-
import wave
import json
import requests
from settings import HTTP_PROXY, HTTPS_PROXY

ASR_URL = "https://try-api.recaius.jp/asr/v1/"
MAX_QUERY = 20


class RecaiusASR(object):
    """Speech Recognizer by RECAIUS-dev API"""

    def __init__(self, recaius_id, recaius_password):
        # TODO: Use proper id and password automatically according to lang
        self.recaius_id = recaius_id
        self.recaius_password = recaius_password

        self._values = dict()
        self._values['id'] = self.recaius_id
        self._values['password'] = self.recaius_password

        self.set_lang('ja_JP')

        # set proxies
        self.proxies = {
            'http': HTTP_PROXY,
            'https': HTTPS_PROXY,
        }

    def set_lang(self, lang):
        model = dict()
        if lang == 'ja_JP':
            model['model_id'] = 1
        elif lang == 'en_US':
            model['model_id'] = 5
        elif lang == 'zh_CN':
            model['model_id'] = 7

        self._values['model'] = model

        return self

    def login(self):
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

    def logout(self, uuid):
        values = dict()
        values['uuid'] = uuid

        headers = {'Content-Type': 'application/json'}
        data = json.dumps(values)
        data = data.encode('utf-8')
        requests.post(ASR_URL + uuid + '/logout', data=data, headers=headers, proxies=self.proxies)

        return

    def recognize(self, uuid, wave_file):
        result_recognize = []

        wf = wave.open(wave_file)

        # send speech data
        chunk = wf.getnframes()
        data = wf.readframes(chunk)

        voice_id = 1
        while data != b'':
            response = self._voice(uuid, voice_id, data)
            if response.status_code == 204:
                voice_id += 1
                continue

            json_result = json.loads(response.text)

            # add final recognition result if 'RESULT' is contained
            result = [elm[1] for elm in json_result if elm[0] == 'RESULT']
            if result:
                result_recognize.extend(result)
                break

            data = wf.readframes(chunk)
            voice_id += 1

        # send finalize signal
        self._voice(uuid, voice_id, b'')
        voice_id += 1

        # get recognition result
        num_query = 0
        while num_query < MAX_QUERY:
            response = self._result(uuid)
            if response.status_code == 204:
                num_query += 1
                continue
            json_result = json.loads(response.text)

            # add final recognition result if 'RESULT' is contained
            result = [elm[1] for elm in json_result if elm[0] == 'RESULT']
            if result:
                result_recognize.extend(result)
                break

            num_query += 1

        return "".join(result_recognize)

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
