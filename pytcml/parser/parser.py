from html.parser import HTMLParser


class TCMLParser:
    pass


class TCML_HTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)

    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_decl(self, data):
        print("Decl     :", data)


p = TCML_HTMLParser()
f = "<!DOCTYPE TCMLv0><text :attr:subattr=\"abcd\">hello!</text>"
print(f)
p.feed(f)
