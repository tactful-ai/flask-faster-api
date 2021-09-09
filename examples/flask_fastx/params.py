"""define parameters location classes"""

# pylint: disable=E0611
# pylint: disable=R0903
# pylint: disable=too-many-instance-attributes
# pylint: disable=redefined-builtin
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

from enum import Enum
from typing import Any
import six


class ParamTypes(Enum):
    """
    define ParamTypes
    """
    QUERY = "args"
    HEADER = "headers"
    PATH = "path"
    COOKIE = "cookies"
    BODY = 'json'
    FORM = 'form'
    FILE = 'files'


# text_type = lambda x: six.text_type(x)
def text_type(type_):
    """return text type as a unicode"""
    return six.text_type(type_)


class Param:
    """
    define Param class
    """
    in_: ParamTypes

    def __init__(
            self,
            default: Any = None,
            name=None,
            dest=None,
            required=False,
            ignore=False,
            type=text_type,
            location=("json", "values",),
            choices=(),
            action="store",
            help=None,
            operators=("=",),
            case_sensitive=True,
            store_missing=True,
            trim=False,
            nullable=True,

    ):
        self.default = default
        self.name = name
        self.dest = dest
        self.required = required
        self.ignore = ignore
        self.location = location
        self.type = type
        self.choices = choices
        self.action = action
        self.help = help
        self.case_sensitive = case_sensitive
        self.operators = operators
        self.store_missing = store_missing
        self.trim = trim
        self.nullable = nullable

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Path(Param):
    """
    define Path class
    """
    in_ = ParamTypes.PATH

    def __init__(
            self,
            default: Any = None,
            name=None,
            dest=None,
            required=False,
            ignore=False,
            type=text_type,
            location=("path",),
            choices=(),
            action="store",
            help=None,
            operators=("=",),
            case_sensitive=True,
            store_missing=True,
            trim=False,
            nullable=True,
    ):
        self.in_ = self.in_
        super().__init__(
            default=default,
            name=name,
            dest=dest,
            required=required,
            ignore=ignore,
            location=location,
            type=type,
            choices=choices,
            action=action,
            help=help,
            case_sensitive=case_sensitive,
            operators=operators,
            store_missing=store_missing,
            trim=trim,
            nullable=nullable
        )


class Query(Param):
    """
    define Query class
    """
    in_ = ParamTypes.QUERY

    def __init__(
            self,
            default: Any = None,
            name=None,
            dest=None,
            required=False,
            ignore=False,
            type=text_type,
            location=("args",),
            choices=(),
            action="store",
            help=None,
            operators=("=",),
            case_sensitive=True,
            store_missing=True,
            trim=False,
            nullable=True,
    ):
        self.in_ = self.in_
        super().__init__(
            default=default,
            name=name,
            dest=dest,
            required=required,
            ignore=ignore,
            location=location,
            type=type,
            choices=choices,
            action=action,
            help=help,
            case_sensitive=case_sensitive,
            operators=operators,
            store_missing=store_missing,
            trim=trim,
            nullable=nullable
        )


class Header(Param):
    """
    define Header class
    """
    in_ = ParamTypes.HEADER

    def __init__(
            self,
            default: Any = None,
            name=None,
            dest=None,
            required=False,
            ignore=False,
            type=text_type,
            location=(ParamTypes.HEADER,),
            choices=(),
            action="store",
            help=None,
            operators=("=",),
            case_sensitive=True,
            store_missing=True,
            trim=False,
            nullable=True,
    ):
        self.in_ = self.in_
        super().__init__(
            default=default,
            name=name,
            dest=dest,
            required=required,
            ignore=ignore,
            location=location,
            type=type,
            choices=choices,
            action=action,
            help=help,
            case_sensitive=case_sensitive,
            operators=operators,
            store_missing=store_missing,
            trim=trim,
            nullable=nullable
        )


class Cookie(Param):
    """
    define Cookie class
    """
    in_ = ParamTypes.COOKIE

    def __init__(
            self,
            default: Any = None,
            name=None,
            dest=None,
            required=False,
            ignore=False,
            type=text_type,
            location=(ParamTypes.COOKIE,),
            choices=(),
            action="store",
            help=None,
            operators=("=",),
            case_sensitive=True,
            store_missing=True,
            trim=False,
            nullable=True,
    ):
        self.in_ = self.in_
        super().__init__(
            default=default,
            name=name,
            dest=dest,
            required=required,
            ignore=ignore,
            location=location,
            type=type,
            choices=choices,
            action=action,
            help=help,
            case_sensitive=case_sensitive,
            operators=operators,
            store_missing=store_missing,
            trim=trim,
            nullable=nullable
        )


class Body(Param):
    """
    define Body class
    """
    in_ = ParamTypes.BODY

    def __init__(
            self,
            default: Any = None,
            name=None,
            dest=None,
            required=False,
            ignore=False,
            type=text_type,
            location=(ParamTypes.BODY,),
            choices=(),
            action="store",
            help=None,
            operators=("=",),
            case_sensitive=True,
            store_missing=True,
            trim=False,
            nullable=True,
    ):
        self.in_ = self.in_
        super().__init__(
            default=default,
            name=name,
            dest=dest,
            required=required,
            ignore=ignore,
            location=location,
            type=type,
            choices=choices,
            action=action,
            help=help,
            case_sensitive=case_sensitive,
            operators=operators,
            store_missing=store_missing,
            trim=trim,
            nullable=nullable
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Form(Param):
    """
    define Form class
    """
    in_ = ParamTypes.FORM

    def __init__(
            self,
            default: Any = None,
            name=None,
            dest=None,
            required=False,
            ignore=False,
            type=text_type,
            location=(ParamTypes.FORM,),
            choices=(),
            action="store",
            help=None,
            operators=("=",),
            case_sensitive=True,
            store_missing=True,
            trim=False,
            nullable=True,
    ):
        self.in_ = self.in_
        super().__init__(
            default=default,
            name=name,
            dest=dest,
            required=required,
            ignore=ignore,
            location=location,
            type=type,
            choices=choices,
            action=action,
            help=help,
            case_sensitive=case_sensitive,
            operators=operators,
            store_missing=store_missing,
            trim=trim,
            nullable=nullable
        )


class File(Param):
    """
    define File class
    """
    in_ = ParamTypes.FILE

    def __init__(
            self,
            default: Any = None,
            name=None,
            dest=None,
            required=False,
            ignore=False,
            type=text_type,
            location=(ParamTypes.FORM,),
            choices=(),
            action="store",
            help=None,
            operators=("=",),
            case_sensitive=True,
            store_missing=True,
            trim=False,
            nullable=True,
    ):
        self.in_ = self.in_
        super().__init__(
            default=default,
            name=name,
            dest=dest,
            required=required,
            ignore=ignore,
            location=location,
            type=type,
            choices=choices,
            action=action,
            help=help,
            case_sensitive=case_sensitive,
            operators=operators,
            store_missing=store_missing,
            trim=trim,
            nullable=nullable
        )
