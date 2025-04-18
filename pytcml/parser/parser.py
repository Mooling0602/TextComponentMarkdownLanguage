from html.parser import HTMLParser
from classes.UnparsedTextComponent import *
from classes.exceptions import *
from collections import deque
from classes.Elements import tagNameToElement, TCMLElement, TCMLQuickElement, TCMLElements, TCMLQuickElements
from classes.misc import Style
from dataclasses import fields

DEBUG = True


class TCMLParser:
    pass


class TCML_HTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)

        self.depth = 0
        self.tagStack = deque()
        self.styleStack = deque([Style()])
        self.attrStack = deque()
        self.tagCheckStack = deque()

        self.inRaw = False
        self.rawStartDepth = -1
        self.rawDatas = ""

        self.parsedContents: list[UnparsedTextComponent] = []

    def tagStackPush(self, tag, style, attr, check):
        self.tagStack.append(tag)
        self.styleStack.append(style)
        self.attrStack.append(attr)
        self.tagCheckStack.append(check)

    def tagStackPop(self, tag):
        if not len(self.tagStack) == 0:
            self.styleStack.pop()
            self.attrStack.pop()
            self.tagStack.pop()
            return self.tagCheckStack.pop()
        else:
            raise TooManyEndTagError(tag)

    def peekTagStack(self) -> tuple[str, Style, list]:
        return self.tagStack[-1], self.styleStack[-1], self.attrStack[-1]

    def getStyle(self) -> Style:
        # 遍历styleStack
        result = Style()
        for singleStyle in self.styleStack:
            for style in fields(singleStyle):
                styleName = style.name
                if getattr(singleStyle, styleName) != None:  # 有被设定的一个style
                    setattr(result, styleName, getattr(singleStyle, styleName))

        return result

    def handle_starttag(self, tag, attrs):
        rtag = tag
        self.depth += 1
        if DEBUG:
            print(f"{'(raw)' if self.inRaw else ''} Start tag: {tag} with depth: {self.depth} & {self.rawStartDepth}")

        if self.inRaw:
            self.rawDatas += self.get_starttag_text()
            return

        style = Style()

        # 处理标签名
        # 快速标签应用
        tag: TCMLElements | TCMLQuickElements = tagNameToElement.get(tag, None)
        if not tag:
            raise NotExistsTagError(rtag)
        tName = ""
        if isinstance(tag, TCMLQuickElement):
            tName = tag.value['baseElement']
            if tag.value.get('specifyAttrs'):
                attrsAsDict = dict(attrs)
                attrsAsDict.update(tag.value.get('specifyAttrs'))
                attrs = list(attrsAsDict.items())
                # 同时需要更新一下style
                for k, v in attrs:
                    setattr(style, k, v)
        elif isinstance(tag, TCMLElement):
            tName = tag.value['element']
        else:
            raise BadTagError(tagName)

        for attr, value in attrs:
            match attr:
                case 'raw':
                    self.inRaw = True
                    self.rawStartDepth = self.depth
                case 'color':
                    style.color = value
                case 'style':
                    for item in value.split(","):
                        setattr(style, item, True)
                case 'font':
                    style.font = value

        self.tagStackPush(tName, style, attrs, rtag)

    def handle_endtag(self, tag):
        self.depth -= 1
        if DEBUG:
            print(f"{'(raw)' if self.inRaw else ''} End tag: {tag} with depth: {self.depth} & {self.rawStartDepth}")

        if self.inRaw:
            if self.rawStartDepth == self.depth+1:
                self.inRaw = False
                self.rawStartDepth = -1
                if DEBUG:
                    print("End raw")
                self.pushContent(self.rawDatas)
                self.rawDatas = ""
            else:
                self.rawDatas += f"<{tag}>"
                return

        tagName: str = self.tagStackPop(tag)
        if tagName != tag:
            raise BadEndTagError(tag)

    def handle_data(self, data):
        if self.inRaw:
            self.rawDatas += data
        else:
            self.pushContent(data)

    def pushContent(self, data):
        tagName, _, attrs = self.peekTagStack()
        style = self.getStyle()

        self.parsedContents.append(UnparsedTextComponent(tagName, attrs, data, style))

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_decl(self, data):
        print("Decl     :", data)


p = TCML_HTMLParser()
f = f"<text><text><aqua><bold>test</bold></aqua>abc</text></text>"
print(f)
p.feed(f)
print(p.parsedContents)
