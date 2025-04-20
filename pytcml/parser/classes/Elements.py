from enum import Enum

from .Attrs import *


class TCMLElement:
    pass


class TCMLQuickElement(TCMLElement):
    pass


class TCMLElements(TCMLElement, Enum):
    line = {'element': 'line'}
    text = {'element': 'text', 'asProviderTarget': True}
    text_hover_text = {'element': 'text-hover-text', 'dataProvider': True,
                       'provideTarget': 'text', 'provideAttr': 'hover:text'}
    score = {'element': 'score', 'attrs': TCMLScoreAttrs}
    selector = {'element': 'selector', 'attrs': TCMLSelectorAttrs, 'asProviderTarget': True}
    selecor_separator = {'element': 'selector-separator',
                         'dataProvider': True, 'provideTarget': 'selector', 'provideAttr': 'selector'}
    keybind = {'element': 'keybind', 'attrs': TCMLKeybindAttrs}
    translate = {'element': 'translate', 'attrs': TCMLTranslateAttrs}
    utranslate = {'element': 'utranslate', 'attrs': TCMLuTranslateAttrs}
    nbt = {'element': 'nbt', 'attrs': TCMLNBTAttrs}
    click = {'element': 'click', 'attrs': TCMLClickAttrs}


class TCMLQuickElements(TCMLQuickElement, Enum):
    # region vanilla_color
    black = {'baseElement': 'text', 'specifyAttrs': {'color': 'black'}}
    dark_blue = {'baseElement': 'text', 'specifyAttrs': {'color': 'dark_blue'}}
    dark_green = {'baseElement': 'text', 'specifyAttrs': {'color': 'dark_green'}}
    dark_aqua = {'baseElement': 'text', 'specifyAttrs': {'color': 'dark_aqua'}}
    dark_red = {'baseElement': 'text', 'specifyAttrs': {'color': 'dark_red'}}
    dark_purple = {'baseElement': 'text', 'specifyAttrs': {'color': 'dark_purple'}}
    gold = {'baseElement': 'text', 'specifyAttrs': {'color': 'gold'}}
    gray = {'baseElement': 'text', 'specifyAttrs': {'color': 'gray'}}
    dark_gray = {'baseElement': 'text', 'specifyAttrs': {'color': 'dark_gray'}}
    blue = {'baseElement': 'text', 'specifyAttrs': {'color': 'blue'}}
    green = {'baseElement': 'text', 'specifyAttrs': {'color': 'green'}}
    aqua = {'baseElement': 'text', 'specifyAttrs': {'color': 'aqua'}}
    red = {'baseElement': 'text', 'specifyAttrs': {'color': 'red'}}
    light_purple = {'baseElement': 'text', 'specifyAttrs': {'color': 'light_purple'}}
    yellow = {'baseElement': 'text', 'specifyAttrs': {'color': 'yellow'}}
    white = {'baseElement': 'text', 'specifyAttrs': {'color': 'white'}}
    # region styles
    bold = {'baseElement': 'text', 'specifyAttrs': {'style': 'bold'}}
    italic = {'baseElement': 'text', 'specifyAttrs': {'style': 'italic'}}
    underlined = {'baseElement': 'text', 'specifyAttrs': {'style': 'underlined'}}
    strikethrough = {'baseElement': 'text', 'specifyAttrs': {'style': 'strikethrough'}}
    obfuscated = {'baseElement': 'text', 'specifyAttrs': {'style': 'obfuscated'}}
    # region fonts
    unifont = {'baseElement': 'text', 'specifyAttrs': {'font': 'uniform'}}
    uniform = {'baseElement': 'text', 'specifyAttrs': {'font': 'uniform'}}
    alt = {'baseElement': 'text', 'specifyAttrs': {'font': 'alt'}}
    illageralt = {'baseElement': 'text', 'specifyAttrs': {'font': 'illageralt'}}
    # region misc
    reset = {'baseElement': 'text', 'specifyAttrs': {'color': 'white', 'style': 'reset', 'font': 'uniform'}}


tagNameToElement = {}
for tag in TCMLElements:
    tagNameToElement[tag.value['element']] = tag
for tag in TCMLQuickElements:
    tagNameToElement[tag.name] = tag
