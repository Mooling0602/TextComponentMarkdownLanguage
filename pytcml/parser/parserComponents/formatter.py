# 第1步: 将parser调用者作用域的值填入list[UnparsedTextComponent]中那些动态绑定值
# 从调用者作用域获取值并应用于所有需要应用的attr和value
import inspect
from typing import Any

from ..classes.parserOptions import ParserOption
from ..classes.UnparsedTextComponent import UnparsedTextComponent


def getCallerScope():
    frame = inspect.currentframe()
    try:
        callerFrame = frame.f_back if frame and frame.f_back else None
        callerLocals = {}
        if callerFrame:
            # 合并调用者的局部变量和全局变量
            callerLocals = callerFrame.f_locals
        callerGlobals = callerFrame.f_globals if callerFrame else {}
        mergedScope = callerGlobals.copy()
        mergedScope.update(callerLocals)
        return mergedScope
    finally:
        del frame  # 防止引用循环导致内存泄漏


class TCML_TCMLFormatter:
    def __init__(self, contents: list[UnparsedTextComponent], scopeValues: dict[Any, Any], options: ParserOption) -> None:
        pass

    def stepApplyConditions(self):
        '''
        应用`if`、`else-if`和`else` attr
        '''
        pass
