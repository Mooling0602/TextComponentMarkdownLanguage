import json
import uuid

from dataclasses import dataclass
from enum import Enum
from typing import Optional


def get_snbt_str(data: dict) -> str:
    def dict_to_snbt(d):
        items = []
        for k, v in d.items():
            key = f"'{k}'" if " " in k or not k.isalnum() else k
            if isinstance(v, dict):
                value = dict_to_snbt(v)
            elif isinstance(v, str):
                value = f"'{v}'"
            else:
                value = str(v)
            items.append(f"{key}:{value}")
        return "{" + ",".join(items) + "}"
    return dict_to_snbt(data)

class TextComponentType(Enum):
    JSON = "json"
    SNBT = "snbt"


class TextColorBase:
    pass


class TextComponentBase:
    pass


class TextColor(TextColorBase):
    def __init__(self, obj, fallback=None):
        if isinstance(obj, TextColor):
            self.value = obj
            return
        if isinstance(obj, str):
            try:
                color = TextColorHex(obj)
                self.value = color.value
                return
            except ValueError:
                for i in TextColorSimple:
                    if i.value.get("color", None) == obj:
                        self.value = i
                        return
        self.value = fallback


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
        if not hex.startswith("#") or len(hex) != 7:
            raise ValueError('invalid hex color.')
        self.value = {"color": hex}

@dataclass
class ObjBase:
    id: str

@dataclass
class entityObj(ObjBase):
    uuid: str
    name: Optional[str] = None
    def __post_init__(self):
        try:
            # Attempt to convert the uuid string using Python's uuid module. This works whether or not hyphens are present.
            uuid_obj = uuid.UUID(self.uuid)
            self.uuid = str(uuid_obj)
        except ValueError:
            raise ValueError("Invalid uuid format. Expected a standard UUID with hyphens (e.g. 123e4567-e89b-12d3-a456-426614174000).")
        
@dataclass
class itemObj(ObjBase):
    count: int = 1 # vanilla default
    components: Optional[dict] = None # not implemented yet, so no checks for it

class hoverAction(Enum):
    text = "show_text"
    item = "show_item"
    entity = "show_entity"

class hoverText:
    def __init__(self, text: str|TextComponentBase):
        self.text = text
        match self.text:
            case t if isinstance(t, str):
                self.value = {"hover_event": {"action": "show_text", "value": t}}
            case t if isinstance(t, TextComponent):
                self.value = {"hover_event": {"action": "show_text", "value": t.to_str()}}

class hoverEvent:
    def __init__(self, action: hoverAction, obj: ObjBase):
        if action == hoverAction.text:
            raise ValueError('use hoverText instead plz')
        self.action = action
        self.obj = obj
        self.id = obj.id
        self.value = {"hover_event": {"action": self.action.value, "id": self.id}}
        match self.action, self.obj:
            case hoverAction.item, obj if isinstance(obj, itemObj):
                count: int = obj.count
                components = obj.components
                self.value["hover_event"].update(count=count)
                if components:
                    self.value["hover_event"].update(components=components)
                return
            case hoverAction.entity, obj if isinstance(obj, entityObj):
                uuid = obj.uuid
                name = obj.name
                self.value["hover_event"].update(uuid=uuid)
                if name:
                    self.value["hover_event"].update(name=name)
                return

class TextComponent(TextComponentBase):
    def __init__(
            self,
            type: TextComponentType,
            text: str,
            color: Optional[TextColorBase] = None,
            hover: Optional[hoverEvent|hoverText] = None
        ):
        self.type = type
        self.text = text
        self.color = color
        self.hover = hover
        try:
            json.loads(self.text)
            raise ValueError("Provided text appears to be a JSON string and is not acceptable as normal text.")
        except json.JSONDecodeError:
            pass

    def to_str(self):
        dict_component = {}
        dict_component.update(text=self.text)
        if self.color is not None:
            dict_component.update(self.color.value)
        if self.hover is not None:
            dict_component.update(self.hover.value)
        match self.type:
            case TextComponentType.JSON:
                result = str(dict_component).replace("'", '"')
                return result
            case TextComponentType.SNBT:
                result = get_snbt_str(dict_component).replace("'", '"')
                return result
            case _:
                raise ValueError(f"Unsupported text component type: {self.type}")


print(TextComponent(
    type=TextComponentType.SNBT,
    text="测试",
    color=TextColor("#442333"),
    hover=hoverEvent(hoverAction.item, itemObj(id="minecraft:apple", count=64))
    ).to_str()
)
