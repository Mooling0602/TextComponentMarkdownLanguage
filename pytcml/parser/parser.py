from parserComponents.tcmlParser import *


class TCMLParser:
    pass


p = TCML_HTMLParser()
f = '<line raw><alt>你好</alt></line>'
print(f)
p.feed(f)
print(p.parsedContents)
