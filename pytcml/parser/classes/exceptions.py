#
class ParserError(Exception):
    ...


class TCMLSyntaxError(ParserError):
    ...


class BadEndTagError(TCMLSyntaxError):
    ...


class TooManyEndTagError(TCMLSyntaxError):
    ...

# region tagError


class TagError(ParserError):
    ...


class BadTagError(TagError):
    def __repr__(self):
        return super().__repr__()+" It maybe is bug inside pytcml. Report issue."


class NotExistsTagError(TagError):
    ...


class ProviderTagInProviderTagError(TagError):
    ...


class ProviderTagInWrongParentTagError(TagError):
    ...

# region tagError/attrError


class AttrError(TagError):
    ...


class TooManySubAttrError(AttrError):
    ...

# region warning


class AttrWarning(Warning):
    ...


class BadAttrWarning(AttrWarning):
    ...


class BadAttrTypeWarning(BadAttrWarning):
    ...


class BadAttrNameWarning(BadAttrWarning):
    ...


class NoSubAttrWarning(AttrWarning):
    ...
