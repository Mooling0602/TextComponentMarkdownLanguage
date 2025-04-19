from enum import Enum
from .exceptions import *


class AttrInvalid:
    ...


class TCMLAttr:
    def valid(self, attrName: str, value: any) -> AttrInvalid | object:
        if attrName.startswith(":"):
            attrName = attrName[1:]
        attrNames = attrName.split(":")
        if len(attrNames) > 2:
            raise TooManySubAttrError(len(attrNames))
        for attr in self:
            if attr.name == attrNames[0]:
                if len(attrNames) == 1:
                    if isinstance(value, attr.value.get('type', object)):
                        return value
                    return AttrInvalid
                elif len(attrNames) == 2:
                    # 匹配sub
                    resolvedSubAttrs = []
                    for name, value in attr.value['subs']:
                        if name == attrName[1]:
                            resolvedSubAttrs.append([name, value.get('priority', 0), value.get('type', object)])
                    resolvedSubAttrs.sort(key=lambda item: item[1], reverse=True)
                    if isinstance(value, resolvedSubAttrs[0][2]):
                        return value
                    else:
                        return AttrInvalid
                else:
                    raise TooManySubAttrError(len(attrNames))


class TCMLGenericAttrs(TCMLAttr, Enum):
    color = {'type': str}
    style = {'type': str}
    font = {'type': str}
    hover = {'type': None, 'subs': {
        'text': {'type': str, 'priority': 100},
        'item': {'type': dict, 'priority': 50},
        'entity': {'type': dict, 'priority': 10},
    }}
    raw = {}


class TCMLScoreAttrs(TCMLAttr, Enum):
    name = {'type': str}
    objective = {'type': str}


class TCMLSelectorAttrs(TCMLAttr, Enum):
    selector = {'type': str}
    separator = {'type': str}


class TCMLKeybindAttrs(TCMLAttr, Enum):
    keybind = {'type': str}


class TCMLTranslateAttrs(TCMLAttr, Enum):
    translate = {'type': str}
    fallback = {'type': str}
    _with = {'type': list}


class TCMLuTranslateAttrs(TCMLAttr, Enum):
    key = {'type': str}


class TCMLNBTAttrs(TCMLAttr, Enum):
    nbt = {'type': str}
    target = {'type': None, 'subs': {
        'block': {'type': str, 'priority': 100},
        'entity': {'type': str, 'priority': 50},
        'storage': {'type': str, 'priority': 10},
    }}
    interpret = {'type': bool}


class TCMLClickAttrs(TCMLAttr, Enum):
    value = {'type': str}
    action = {'type': None, 'subs': {
        'open_url': {'type': str, 'priority': 100},
        'run_command': {'type': str, 'priority': 80},
        'change_page': {'type': str, 'priority': 60},
        'suggest_command': {'type': str, 'priority': 40},
        'copy_to_clipboard': {'type': str, 'priority': 20},
    }}
