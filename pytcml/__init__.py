import json

from enum import Enum
from typing import Optional


class TextComponentType(Enum):
    JSON = "json"
    SNBT = "snbt"

class TextColorBase:
    pass

class TextComponentBase:
    pass

class TextColor(TextColorBase):
    def get_color(self, obj, fallback=None):
        if isinstance(obj, TextColor):
            return obj
        if isinstance(obj, str):
            try:
                color = TextColorHex(obj)
                return color
            except ValueError:
                for i in TextColorSimple:
                    if i.value.get("color", None) == obj:
                        return i
        return fallback

class TextColorSimple(TextColorBase, Enum):
    black = {"color": "black"}
    dark_blue = {"color": "dark_blue"}
    dark_green = {"color": "dark_green"}
    dark_aqua = {"color": "dark_aqua"}
    dark_red = {"color": "dark_red"}
    dark_purple = {"color": "dark_purple"}
    gold = {"color": "gold"}
    gray = {"color": "gray"}
    dark_gray = {"color": "dark_gray"}
    blue = {"color": "blue"}
    green = {"color": "green"}
    aqua = {"color": "aqua"}
    red = {"color": "red"}
    light_purple = {"color": "light_purple"}
    yellow = {"color": "yellow"}
    white = {"color": "white"}

class TextColorHex(TextColorBase):
    def __init__(self, hex: str):
        self.hex = hex
        if not hex.startswith("#") and len(hex) == 7:
            raise ValueError('invalid hex color.')
        return {"color": hex}

class hoverAction(Enum):
    text = "show_text"
    item = "show_item"
    entity = "show_entity"

class hoverEvent:
    def __init__(self, action: hoverAction):
        self.action = action

    def to_str(self):
        pass

class TextComponent(TextComponentBase):
    def __init__(self, type: TextComponentType, text: str, color: Optional[TextColorBase] = None):
        self.type = type
        self.text = text
        self.color = color
        try:
            json.loads(self.text)
            raise ValueError("Provided text appears to be a JSON string and is not acceptable as normal text.")
        except json.JSONDecodeError:
            pass

    def to_str(self):
        dict_component = {}
        match self.type:
            case TextComponentType.JSON:
                dict_component.update(text=self.text)
                if self.color is not None:
                    dict_component.update(self.color.value)
                    result = str(dict_component).replace("'", '"')
                    return result
            case TextComponentType.SNBT:
                pass
            case _:
                raise ValueError(f"Unsupported text component type: {self.type}")
            
    
print(TextComponent(type=TextComponentType.JSON, text="测试", color=TextColorSimple.red).to_str())
            


