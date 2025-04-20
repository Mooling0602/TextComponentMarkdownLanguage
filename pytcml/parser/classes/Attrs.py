from enum import Enum
from .exceptions import *
import warnings
import re


class AttrInvalid:
    ...


def strToList(value: str) -> list:
    values = re.split(r'(?!\\),', value)
    return values


def strToDict(value: str) -> dict:
    KVs = strToList(value)
    result = {}
    for KV in KVs:
        splitedKV = re.split(r'(?!\\):', KV)
        if len(splitedKV) != 2:
            return False
        result[splitedKV[0].strip()] = splitedKV[1].strip()
    return result


class TCMLAttr:
    def valid(self, attrName: str, value: any) -> AttrInvalid | tuple[str, object]:
        if attrName.startswith(":"):
            attrName = attrName[1:]
        attrNames = attrName.split(":")
        if len(attrNames) > 2:
            raise TooManySubAttrError(len(attrNames))
        for attr in self:
            registeredAttrName = attr.name
            if registeredAttrName.startswith("_"):
                registeredAttrName = registeredAttrName[1:]
            if registeredAttrName == attrNames[0]:
                if len(attrNames) == 1:
                    if isinstance(value, attr.value.get('type', object)):
                        return attrName, value
                    warnings.warn(value, BadAttrTypeWarning)
                    return AttrInvalid()
                elif len(attrNames) == 2:
                    if not attr.value.get('subs', None):
                        warnings.warn(attrNames[1], NoSubAttrWarning)
                        warnings.warn(value, BadAttrNameWarning)
                        return AttrInvalid()
                    # 匹配sub
                    resolvedSubAttrs = []
                    for name, subAttrValue in attr.value['subs'].items():
                        if name == attrNames[1]:
                            resolvedSubAttrs.append([name, subAttrValue.get('priority', 0),
                                                    subAttrValue.get('type', object)])
                    resolvedSubAttrs.sort(key=lambda item: item[1], reverse=True)
                    if len(resolvedSubAttrs) == 0:
                        warnings.warn(value, BadAttrNameWarning)
                        return AttrInvalid()
                    if isinstance(value, resolvedSubAttrs[0][2]):
                        return attrNames[0]+":"+resolvedSubAttrs[0][0], value
                    elif resolvedSubAttrs[0][2] == list:
                        return attrNames[0]+":"+resolvedSubAttrs[0][0], strToList(value)
                    elif resolvedSubAttrs[0][2] == dict:
                        v = strToDict(value)
                        if v == False:
                            warnings.warn(value, BadAttrTypeWarning)
                            return AttrInvalid()
                        return attrNames[0]+":"+resolvedSubAttrs[0][0], v
                    else:
                        warnings.warn(value, BadAttrTypeWarning)
                        return AttrInvalid()
                else:
                    raise TooManySubAttrError(len(attrNames))
        warnings.warn(value, BadAttrNameWarning)
        return AttrInvalid()


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
    _if = {'type': str}
    _for = {'type': str}


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
