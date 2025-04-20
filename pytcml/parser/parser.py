from parserComponents.tcmlParser import *
from classes.parserOptions import ParserOption


class TCMLParser:
    pass


o = ParserOption(True)

p = TCML_HTMLParser(o)
f = '<click action:open_url="https://yupu.dev"><aqua><text>Hover on me! <text-hover-text>hover</text-hover-text><bold><red>RED and HOVER</red></bold></text></aqua></click>'
print(f)
p.feed(f)
print(p.parsedContents)
