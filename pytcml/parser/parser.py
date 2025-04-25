from parserComponents.tcmlParser import *
from classes.parserOptions import ParserOption
from classes.UnparsedTextComponent import UnparsedTextComponent


class TCMLParser:
    pass


o = ParserOption(True)

p = TCML_HTMLParser(o)
f = '<click action:open_url="https://yupu.dev"><aqua><text>Hover on me! <bold><red>RED and HOVER</red></bold></text></aqua></click>'
print(f)
p.feed(f)
print(p.parsedContents)
