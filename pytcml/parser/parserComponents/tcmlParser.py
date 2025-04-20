# 第0步: TCML字符串转list[UnparsedTextComponent]

import warnings
from collections import deque
from dataclasses import fields
from html.parser import HTMLParser

from classes.Attrs import AttrInvalid, TCMLGenericAttrs
from classes.Elements import TCMLElements, TCMLQuickElements, tagNameToElement
from classes.exceptions import *
from classes.misc import Style
from classes.parserOptions import ParserOption
from classes.UnparsedTextComponent import *


class TCML_HTMLParser(HTMLParser):
    def __init__(self, options: ParserOption):
        super().__init__(convert_charrefs=True)
        self.options = options

        # 栈
        self.depth = 0  # 解析深度，用于检查是否闭合特定标签
        self.tagStack: deque[str] = deque()  # 检查标签是否配对
        self.styleStack: deque[Style] = deque([Style().reset()])  # 继承style
        self.attrStack: deque[list[tuple | list]] = deque()  # 我也不知道啥用处，留着吧
        self.tagCheckStack: deque[str] = deque()  # 和tagStack一样，但是它里面留的是原始标签名

        self.inRaw: bool = False  # raw模式
        self.rawStartDepth: int = -1
        self.rawDatas: str = ""

        self.inContentProvider: bool = False  # contentProvider模式
        self.provideStartDepth: int = -1
        self.provideContents: list[UnparsedTextComponent] = []

        # 解析内容
        self.parsedContents: list[UnparsedTextComponent] = []

        if self.options.outputDebug:
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

    def handle_starttag(self, tag: str, attrs: list):
        rtag: str = tag
        self.depth += 1
        if self.options.outputDebug:
            print(f"{'(raw)' if self.inRaw else ''} Start tag: {tag} with depth: {self.depth} & {self.rawStartDepth}")

        if self.inRaw:  # 跳过后续解析
            self.rawDatas += self.get_starttag_text() or ""
            return

        style = Style()  # 空style

        # 处理标签名
        # 快速标签应用
        tagAsEnum: TCMLElements | TCMLQuickElements | None = tagNameToElement.get(tag, None)
        if tagAsEnum is None:
            raise NotExistsTagError(rtag, self.getpos())
        tName = ""
        if isinstance(tagAsEnum, TCMLQuickElements):
            tName = tagAsEnum.value['baseElement']
            if tagAsEnum.value.get('specifyAttrs'):
                attrsAsDict = dict(attrs)
                specifyAttrs = tagAsEnum.value.get('specifyAttrs')
                if specifyAttrs:
                    attrsAsDict.update(specifyAttrs)
                attrs = list(attrsAsDict.items())
                # 同时需要更新一下style
                for k, v in attrs:
                    setattr(style, k, v)
        elif isinstance(tagAsEnum, TCMLElements):
            tName = tagAsEnum.value['element']
        else:
            raise BadTagError(rtag, self.getpos())

        if tagAsEnum.value.get('dataProvider', False):
            if self.inContentProvider:
                raise ProviderTagInProviderTagError(tName, self.getpos())
            self.inContentProvider = True
            self.provideStartDepth = self.depth
            if self.options.outputDebug:
                print(f"IN provide: {self.depth}")

        attrList = [TCMLGenericAttrs]
        attrsValue = tagAsEnum.value.get('attrs', None)
        if isinstance(attrsValue, type) and issubclass(attrsValue, TCMLGenericAttrs):
            attrList.append(attrsValue)
        outAttrs = []
        isAttrValid = False
        name = None
        result = None
        for attr, value in attrs:
            for index, attrsWillCheck in enumerate(attrList):
                validResult = TCMLGenericAttrs.valid(attrsWillCheck, attr, value)  # type: ignore
                if isinstance(validResult, AttrInvalid):
                    warnings.warn(attr, BadAttrWarning)
                    if index != len(attrsWillCheck)-1:
                        continue  # 还没有检查完
                    isAttrValid = False
                    break
                else:
                    name, result = validResult
                    isAttrValid = True
                    break
            if not isAttrValid:
                continue
            if name is None or result is None:
                continue
            match name:
                case 'raw':
                    self.inRaw = True
                    self.rawStartDepth = self.depth
                    if self.options.outputDebug:
                        print(f"IN raw: {self.depth}")
                case 'color':
                    style.color = value
                case 'style':
                    for item in value.split(","):
                        if item.strip() == 'reset':
                            style = Style().reset()
                        else:
                            setattr(style, item.strip(), True)
                case 'font':
                    style.font = value
                case _:
                    itemWillAppend = (name, result)
                    if not itemWillAppend in outAttrs:
                        outAttrs.append(itemWillAppend)
            isAttrValid = False
            name = None
            result = None

        self.tagStackPush(tName, style, outAttrs, rtag)

        if not self.inContentProvider:
            if tagAsEnum.value.get('asProviderTarget', False):  # 插入一个空的tc
                self.pushContent("")

    def handle_endtag(self, tag):
        self.depth -= 1
        if self.options.outputDebug:
            print(f"{'(raw)' if self.inRaw else ''} End tag: {tag} with depth: {self.depth} & {self.rawStartDepth}")

        if self.inRaw:
            if self.rawStartDepth == self.depth+1:
                self.inRaw = False
                self.rawStartDepth = -1
                if self.options.outputDebug:
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
                if self.options.outputDebug:
                    print(f"End Content provider with contents: {self.provideContents} and at end tag:{tag}")
                self.parsedContents[-1].attrs
                # 1. 检查target
                trName, _, _ = self.peekTagStack(-2)
                tagAsEnum: TCMLElements | TCMLQuickElements | None = tagNameToElement.get(tag, None)
                if tagAsEnum is None:
                    raise BadEndTagError(tag)
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

    def handle_decl(self, decl):
        print("Decl     :", decl)
