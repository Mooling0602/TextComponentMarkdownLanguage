from html.parser import HTMLParser
from classes.UnparsedTextComponent import *
from classes.exceptions import *
from collections import deque
from classes.Elements import tagNameToElement, TCMLElement, TCMLQuickElement, TCMLElements, TCMLQuickElements
from classes.Attrs import TCMLGenericAttrs, AttrInvalid
from classes.misc import Style
from dataclasses import fields
import warnings

DEBUG = True


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

        self.inContentProvider = False
        self.provideStartDepth = -1
        self.provideContents: list[UnparsedTextComponent] = []
        self.parsedContents: list[UnparsedTextComponent] = []

        if DEBUG:
            print("START PARSER")

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
            raise TooManyEndTagError(tag, self.getpos())

    def peekTagStack(self, delta=-1) -> tuple[str, Style, list]:
        return self.tagStack[delta], self.styleStack[delta], self.attrStack[delta]

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
            raise NotExistsTagError(rtag, self.getpos())
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
            raise BadTagError(tagName, self.getpos())

        if tag.value.get('dataProvider', False):
            if self.inContentProvider:
                raise ProviderTagInProviderTagError(tName, self.getpos())
            self.inContentProvider = True
            self.provideStartDepth = self.depth
            if DEBUG:
                print(f"IN provide: {self.depth}")

        attrList = [TCMLGenericAttrs]
        attrList.append(tag.value.get('attrs', TCMLGenericAttrs)) if tag.value.get('attrs', None) else None
        for attr, value in attrs:
            for attrsWillCheck in attrList:
                result = TCMLGenericAttrs.valid(attrsWillCheck, attr, value)
                if isinstance(result, AttrInvalid):
                    warnings.warn(attr, BadAttrWarning)
            match attr:
                case 'raw':
                    self.inRaw = True
                    self.rawStartDepth = self.depth
                    if DEBUG:
                        print(f"IN raw: {self.depth}")
                case 'color':
                    style.color = value
                case 'style':
                    for item in value.split(","):
                        setattr(style, item, True)
                case 'font':
                    style.font = value

        self.tagStackPush(tName, style, attrs, rtag)

        if not self.inContentProvider:
            if tag.value.get('asProviderTarget', False):  # 插入一个空的tc
                self.pushContent("")

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
        elif self.inContentProvider:
            if self.provideStartDepth == self.depth+1:
                self.inContentProvider = False
                self.provideStartDepth = -1
                if DEBUG:
                    print(f"End Content provider with contents: {self.provideContents} and at end tag:{tag}")
                self.parsedContents[-1].attrs
                # 1. 检查target
                trName, _, _ = self.peekTagStack(-2)
                tagAsEnum: TCMLElements | TCMLQuickElements = tagNameToElement.get(tag, None)
                # if tagAsEnum.value.get('element', '???') == tag:
                #     pass
                if tagAsEnum.value.get("provideTarget", "undefined") != trName:
                    raise ProviderTagInWrongParentTagError(
                        trName, tagAsEnum.value.get("provideTarget", "???"), self.getpos())
                # 2. 写入attr
                attrsAsDict = dict(self.parsedContents[-1].attrs)
                attrsAsDict[tagAsEnum.value.get('provideAttr', 'providedContent')] = self.provideContents
                self.parsedContents[-1].attrs = list(attrsAsDict.items())
                self.provideContents = []

        tagName: str = self.tagStackPop(tag)
        if tagName != tag:
            raise BadEndTagError(tag, self.getpos())

    def handle_data(self, data):
        if self.inRaw:
            self.rawDatas += data
        else:
            self.pushContent(data)

    def pushContent(self, data):
        tagName, _, attrs = self.peekTagStack()
        style = self.getStyle()

        if self.inContentProvider:
            self.provideContents.append(UnparsedTextComponent(tagName, attrs, data, style))
        else:
            self.parsedContents.append(UnparsedTextComponent(tagName, attrs, data, style))

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_decl(self, data):
        print("Decl     :", data)


p = TCML_HTMLParser()
f = f"<text><selector b><selector-separator>aaa</selector-separator></selector></text>"
print(f)
p.feed(f)
print(p.parsedContents)
