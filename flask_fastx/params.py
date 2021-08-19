"""
define parameters location classes
"""

# pylint: disable=E0611
# pylint: disable=R0903

from enum import Enum
from typing import Any, Dict, Optional

from pydantic.fields import FieldInfo, Undefined  # type: ignore


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





class Param(FieldInfo):
    """
    define Param class
    """
    in_: ParamTypes

    def __init__(
            self,
            default: Any,
            *,
            alias: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            regex: Optional[str] = None,
            example: Any = Undefined,
            examples: Optional[Dict[str, Any]] = None,
            deprecated: Optional[bool] = None,
            **extra: Any,
    ):
        self.deprecated = deprecated
        self.example = example
        self.examples = examples
        super().__init__(
            default,
            alias=alias,
            title=title,
            description=description,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            **extra,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Path(Param):
    """
    define Path class
    """
    in_ = ParamTypes.PATH

    def __init__(
            self,
            default: Any,
            *,
            alias: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            regex: Optional[str] = None,
            example: Any = Undefined,
            examples: Optional[Dict[str, Any]] = None,
            deprecated: Optional[bool] = None,
            **extra: Any,
    ):
        self.in_ = self.in_
        super().__init__(
            ...,
            alias=alias,
            title=title,
            description=description,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            deprecated=deprecated,
            example=example,
            examples=examples,
            **extra,
        )


class Query(Param):
    """
    define Query class
    """
    in_ = ParamTypes.QUERY

    def __init__(
            self,
            default: Any,
            *,
            alias: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            regex: Optional[str] = None,
            example: Any = Undefined,
            examples: Optional[Dict[str, Any]] = None,
            deprecated: Optional[bool] = None,
            **extra: Any,
    ):
        self.in_ = self.in_
        super().__init__(
            default,
            alias=alias,
            title=title,
            description=description,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            deprecated=deprecated,
            example=example,
            examples=examples,
            **extra,
        )


class Header(Param):
    """
    define Header class
    """
    in_ = ParamTypes.HEADER

    def __init__(
            self,
            default: Any,
            *,
            alias: Optional[str] = None,
            convert_underscores: bool = True,
            title: Optional[str] = None,
            description: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            regex: Optional[str] = None,
            example: Any = Undefined,
            examples: Optional[Dict[str, Any]] = None,
            deprecated: Optional[bool] = None,
            **extra: Any,
    ):
        self.convert_underscores = convert_underscores
        self.in_ = self.in_
        super().__init__(
            default,
            alias=alias,
            title=title,
            description=description,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            deprecated=deprecated,
            example=example,
            examples=examples,
            **extra,
        )


class Cookie(Param):
    """
    define Cookie class
    """
    in_ = ParamTypes.COOKIE

    def __init__(
            self,
            default: Any,
            *,
            alias: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            regex: Optional[str] = None,
            example: Any = Undefined,
            examples: Optional[Dict[str, Any]] = None,
            deprecated: Optional[bool] = None,
            **extra: Any,
    ):
        self.in_ = self.in_
        super().__init__(
            default,
            alias=alias,
            title=title,
            description=description,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            deprecated=deprecated,
            example=example,
            examples=examples,
            **extra,
        )


class Body(Param):
    """
    define Body class
    """
    in_ = ParamTypes.BODY

    def __init__(
            self,
            default: Any,
            *,
            embed: bool = False,
            media_type: str = "application/json",
            alias: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            regex: Optional[str] = None,
            example: Any = Undefined,
            examples: Optional[Dict[str, Any]] = None,
            **extra: Any,
    ):
        self.embed = embed
        self.media_type = media_type
        self.example = example
        self.examples = examples
        super().__init__(
            default,
            alias=alias,
            title=title,
            description=description,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            **extra,
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
            default: Any,
            *,
            media_type: str = "application/x-www-form-urlencoded",
            alias: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            regex: Optional[str] = None,
            example: Any = Undefined,
            examples: Optional[Dict[str, Any]] = None,
            **extra: Any,
    ):
        super().__init__(
            default,
            embed=True,
            media_type=media_type,
            alias=alias,
            title=title,
            description=description,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            example=example,
            examples=examples,
            **extra,
        )


class File(Param):
    """
    define File class
    """
    in_ = ParamTypes.FILE

    def __init__(
            self,
            default: Any,
            *,
            media_type: str = "multipart/form-data",
            alias: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            regex: Optional[str] = None,
            example: Any = Undefined,
            examples: Optional[Dict[str, Any]] = None,
            **extra: Any,
    ):
        super().__init__(
            default,
            media_type=media_type,
            alias=alias,
            title=title,
            description=description,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            example=example,
            examples=examples,
            **extra,
        )
