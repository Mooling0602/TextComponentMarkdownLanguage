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
    ...


class NotExistsTagError(TagError):
    ...
