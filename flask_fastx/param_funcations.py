"""
define parameters functions
"""
# pylint: disable=E0611

from typing import Any, Dict, Optional
from pydantic.fields import Undefined  # type: ignore
from flask_fastx import params

# pylint: disable=invalid-name
def Path(  # noqa: N802
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
) -> Any:
    """ define path function """
    return params.Path(
        default=default,
        alias=alias,
        title=title,
        description=description,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        example=example,
        examples=examples,
        deprecated=deprecated,
        **extra,
    )


def Query(  # noqa: N802
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
) -> Any:
    """ define Query function """
    return params.Query(
        default,
        alias=alias,
        title=title,
        description=description,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        example=example,
        examples=examples,
        deprecated=deprecated,
        **extra,
    )


def Header(  # noqa: N802
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
) -> Any:
    """ define header function """
    return params.Header(
        default,
        alias=alias,
        convert_underscores=convert_underscores,
        title=title,
        description=description,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        example=example,
        examples=examples,
        deprecated=deprecated,
        **extra,
    )


def Cookie(  # noqa: N802
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
) -> Any:
    """ define cookie function """
    return params.Cookie(
        default,
        alias=alias,
        title=title,
        description=description,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        example=example,
        examples=examples,
        deprecated=deprecated,
        **extra,
    )


def Body(  # noqa: N802
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
) -> Any:
    """ define body function """
    return params.Body(
        default,
        embed=embed,
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


def Form(  # noqa: N802
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
) -> Any:
    """ define form function """
    return params.Form(
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


def File(  # noqa: N802
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
) -> Any:
    """ define file function """
    return params.File(
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
