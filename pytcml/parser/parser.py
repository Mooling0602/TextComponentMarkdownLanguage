from parserComponents.tcmlParser import *
from classes.parserOptions import ParserOption


class TCMLParser:
    pass


o = ParserOption(True)

p = TCML_HTMLParser(o)
f = '<line raw><alt>你好</alt></line>'
print(f)
p.feed(f)
print(p.parsedContents)
