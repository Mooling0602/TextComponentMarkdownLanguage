#

class UnparsedTextComponent:
    def __init__(self, tagName, attrs, value, style):
        self.tag = tagName
        self.attrs = attrs
        self.value = value
        self.styles = style

    def __repr__(self):
        attrs = "".join([f'{attr}="{value}"' for attr, value in self.attrs])
        return str(f"UPTC(<{self.tag} {attrs} {self.styles}>{self.value}))")
