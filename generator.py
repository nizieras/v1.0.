import json
import urllib.request

class Generation:
    def __init__(self):
        self.__result_text = ""
        self.__headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
                      '(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Origin': 'https://yandex.ru',
        'Referer': 'https://yandex.ru/',
    }
        self.__api_url = 'https://zeapi.yandex.net/lab/api/yalm/text3'
        self.__intro = 0
        self.__filter = 1

    def get_result_str(self):
        return getattr(self, "_Generation__result_text")

    def generate(self, text_for_generate):
        payload = {"query": text_for_generate, "intro": self.__intro, "filter": self.__filter}
        params = json.dumps(payload).encode('utf8')
        req = urllib.request.Request(self.__api_url, data=params, headers=self.__headers)
        response = urllib.request.urlopen(req)
        reqst = json.loads(response.read().decode('utf8'))
        query = reqst['query']
        ans = reqst['text']
        self.__result_text = query + ans
        return query + ans


if __name__ == "__main__":
    generation = Generation()
    result = generation.generate("Солнце вышло покурить на балкон")
    print(result)