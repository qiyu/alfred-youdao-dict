import sys
from dataclasses import dataclass
from json import dumps
from json.encoder import JSONEncoder
from typing import Optional, Any

import pydash as _
import requests
import xmltodict


class AlfredItem:
    def __init__(self, arg, path, quicklookurl, subtitle, copy, title):
        self.arg: Optional[str] = arg
        self.icon: Optional[AlfredIcon] = AlfredIcon(path)
        self.quicklookurl: Optional[str] = quicklookurl
        self.subtitle: Optional[str] = subtitle
        self.text: Optional[AlfredText] = AlfredText(copy)
        self.title: Optional[str] = title
        self.valid: Optional[bool] = True


@dataclass
class AlfredIcon:
    path: str


@dataclass
class AlfredText:
    copy: str


class AlfredJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (AlfredItem, AlfredIcon, AlfredText)):
            return o.__dict__
        return super().default(o)


def main():
    items = []

    if len(sys.argv) == 2:
        query = sys.argv[1]
        r = requests.get('http://dict.youdao.com/fsearch', params={'q': query})
        result = (xmltodict.parse(r.content.decode(), force_list=('translation',)))
        custom_translation = _.get(result, 'yodaodict.custom-translation.translation')
        if not custom_translation:
            items.append(build_translate_result(query, '暂无'))
        else:
            for k in custom_translation:
                content = k['content']
                items.append(build_translate_result(query, content))
    else:
        items.append(build_translate_result('请等待', '请等待'))

    # for k in result['yodaodict']['yodao-web-dict']['web-translation']:
    #     print(k)
    print(dumps({"items": items}, cls=AlfredJSONEncoder))


def build_translate_result(query, content):
    return AlfredItem(content, 'translate.png', f'http://youdao.com/w/{query}', query, content, content)


if __name__ == '__main__':
    main()
