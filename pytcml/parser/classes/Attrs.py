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


def isInstanceOfAny(value, types):
    if isinstance(types, tuple):
        return any(isinstance(value, t) for t in types)
    return isinstance(value, types)


class TCMLAttr:
    def valid(self, attrName: str, value: any) -> AttrInvalid | tuple[str, object]:
        if attrName.startswith(":"):  # 处理动态绑定
            attrName = attrName[1:]
        attrNames = attrName.split(":")  # 分开sub attr
        if len(attrNames) > 2:
            raise TooManySubAttrError(len(attrNames))
        for attr in self:  # 遍历自身的所有attr
            registeredAttrName: str = attr.name  # 处理那些与保留关键字相同的attrName
            if registeredAttrName.startswith("_"):
                registeredAttrName = registeredAttrName[1:]
            registeredAttrName.replace("_", "-")  # 替换下划线
            # 如果偷懒没写name...
            if registeredAttrName == attrNames[0] and attr.value.get('name', attrNames[0]) == attrNames[0]:
                if len(attrNames) == 1:  # 没有sub
                    if isInstanceOfAny(value, attr.value.get('type', object)):
                        return attrName, value
                    warnings.warn(value, BadAttrTypeWarning)
                    return AttrInvalid()
                elif len(attrNames) == 2:  # 有sub
                    if not attr.value.get('subs', None):  # 但是那个attr没有sub
                        warnings.warn(attrNames[1], NoSubAttrWarning)
                        warnings.warn(value, BadAttrNameWarning)
                        return AttrInvalid()
                    # 匹配sub
                    resolvedSubAttrs = []
                    for name, subAttrValue in attr.value['subs'].items():
                        if name == attrNames[1]:
                            resolvedSubAttrs.append([name, subAttrValue.get('priority', 0),
                                                    subAttrValue.get('type', object)])  # sub名称, 优先级, sub类型
                    resolvedSubAttrs.sort(key=lambda item: item[1], reverse=True)  # 按优先级排序
                    if len(resolvedSubAttrs) == 0:  # 没有匹配到sub
                        warnings.warn(value, BadAttrNameWarning)
                        return AttrInvalid()
                    if isInstanceOfAny(value, resolvedSubAttrs[0][2]):
                        return attrNames[0]+":"+resolvedSubAttrs[0][0], value
                    elif resolvedSubAttrs[0][2] == list and isinstance(value, str):  # 行内list
                        return attrNames[0]+":"+resolvedSubAttrs[0][0], strToList(value)
                    elif resolvedSubAttrs[0][2] == dict and isinstance(value, str):  # 行内dict
                        v = strToDict(value)
                        if v == False:
                            warnings.warn(value, BadAttrTypeWarning)
                            return AttrInvalid()
                        return attrNames[0]+":"+resolvedSubAttrs[0][0], v
                    else:
                        warnings.warn(value, BadAttrTypeWarning)  # 类型不对
                        return AttrInvalid()
                else:
                    raise TooManySubAttrError(len(attrNames))
        warnings.warn(attrName, BadAttrNameWarning)  # 没有匹配到
        return AttrInvalid()


'''
attr格式:
attrName:dict = {
    'name': str = '你想要的attr名称，可不填，用于防重',
    'type': type = type( | type) # 你想要的attr类型
    'subs': dict = {
        'xxx' : {
            'type': type = type # 和上面一样
            'priority': int = 100 # 多个sub attr同时存在，按这个大小排序，大的优先
        }
        # 如果用了sub且不需要`xxx="123"`，`type`指定None
    }
}
'''


class TCMLGenericAttrs(TCMLAttr, Enum):
    color = {'name': 'color', 'type': str}
    style = {'name': 'style', 'type': str}
    font = {'name': 'font', 'type': str}
    hover = {'name': 'hover', 'type': None, 'subs': {
        'text': {'type': str, 'priority': 100},
        'item': {'type': dict, 'priority': 50},
        'entity': {'type': dict, 'priority': 10},
    }}
    raw = {'name': 'raw'}
    _if = {'name': 'if', 'type': str}
    _for = {'name': 'for', 'type': str}
    else_if = {'name': 'else-if', 'type': str}
    _else = {'name': 'else'}


class TCMLScoreAttrs(TCMLAttr, Enum):
    name = {'name': 'name', 'type': str}
    objective = {'name': 'objective', 'type': str}


class TCMLSelectorAttrs(TCMLAttr, Enum):
    selector = {'name': 'selector', 'type': str}
    separator = {'name': 'separator', 'type': str}


class TCMLKeybindAttrs(TCMLAttr, Enum):
    keybind = {'name': 'keybind', 'type': str}


class TCMLTranslateAttrs(TCMLAttr, Enum):
    translate = {'name': 'translate', 'type': str}
    fallback = {'name': 'fallback', 'type': str}
    _with = {'name': 'with', 'type': list}


class TCMLuTranslateAttrs(TCMLAttr, Enum):
    key = {'name': 'key', 'type': str}


class TCMLNBTAttrs(TCMLAttr, Enum):
    nbt = {'name': 'nbt', 'type': str}
    target = {'name': 'target', 'type': None, 'subs': {
        'block': {'type': str, 'priority': 100},
        'entity': {'type': str, 'priority': 50},
        'storage': {'type': str, 'priority': 10},
    }}
    interpret = {'name': 'interpret', 'type': bool}


class TCMLClickAttrs(TCMLAttr, Enum):
    value = {'name': 'value', 'type': str}
    action = {'name': 'action', 'type': None, 'subs': {
        'open_url': {'type': str, 'priority': 100},
        'run_command': {'type': str, 'priority': 80},
        'change_page': {'type': str, 'priority': 60},
        'suggest_command': {'type': str, 'priority': 40},
        'copy_to_clipboard': {'type': str, 'priority': 20},
    }}
