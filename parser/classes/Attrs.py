from enum import Enum


class TCMLAttr:
    pass


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
