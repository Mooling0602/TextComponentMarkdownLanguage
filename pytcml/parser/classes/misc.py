from dataclasses import dataclass, fields


@dataclass
class Style:
    color: str = None
    font: str = None
    bold: bool = None
    italic: bool = None
    underlined: bool = None
    strikethrough: bool = None
    obfuscated: bool = None

    def __repr__(self):
        result = "Style( "
        for style in fields(self):
            if getattr(self, style.name) != None:
                result += f"{style.name}: {getattr(self, style.name)},"
        result = result[:-1]
        result += ")"
        return result
