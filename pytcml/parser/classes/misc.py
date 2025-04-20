from dataclasses import dataclass, fields


@dataclass
class Style:
    color: str | None = None
    font: str | None = None
    bold: bool | None = None
    italic: bool | None = None
    underlined: bool | None = None
    strikethrough: bool | None = None
    obfuscated: bool | None = None

    def reset(self: 'Style') -> 'Style':
        return Style('white', 'uniform', False, False, False, False, False)

    def __repr__(self):
        result = "Style( "
        for style in fields(self):
            if getattr(self, style.name) != None:
                result += f"{style.name}: {getattr(self, style.name)},"
        result = result[:-1]
        result += ")"
        return result


@dataclass
class ClickAndHover:
    clickType: str | None = None
    clickValue: str | None = None
    hoverType: str | None = None
    hoverValue: str | dict | None = None
