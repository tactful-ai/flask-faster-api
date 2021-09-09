"""
define parameters functions
"""
# pylint: disable=E0611
# pylint: disable=redefined-builtin
# pylint: disable=too-many-arguments
# pylint: disable=invalid-name

from typing import Any
import six
from flask_fastx import params


# text_type = lambda x: six.text_type(x)
def text_type(type_):
    """return text type as a unicode"""
    return six.text_type(type_)


def Path(  # noqa: N802
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
) -> Any:
    """ define path function """
    return params.Path(
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


def Query(  # noqa: N802
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
) -> Any:
    """ define Query function """
    return params.Query(
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


def Header(  # noqa: N802
        default: Any = None,
        name=None,
        dest=None,
        required=False,
        ignore=False,
        type=text_type,
        location=("headers",),
        choices=(),
        action="store",
        help=None,
        operators=("=",),
        case_sensitive=True,
        store_missing=True,
        trim=False,
        nullable=True,
) -> Any:
    """ define header function """
    return params.Header(
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


def Cookie(  # noqa: N802
        default: Any = None,
        name=None,
        dest=None,
        required=False,
        ignore=False,
        type=text_type,
        location=("cookies",),
        choices=(),
        action="store",
        help=None,
        operators=("=",),
        case_sensitive=True,
        store_missing=True,
        trim=False,
        nullable=True,
) -> Any:
    """ define cookie function """
    return params.Cookie(
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


def Body(  # noqa: N802
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
) -> Any:
    """ define body function """
    return params.Body(
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


def Form(  # noqa: N802
        default: Any = None,
        name=None,
        dest=None,
        required=False,
        ignore=False,
        type=text_type,
        location=("form",),
        choices=(),
        action="store",
        help=None,
        operators=("=",),
        case_sensitive=True,
        store_missing=True,
        trim=False,
        nullable=True,
) -> Any:
    """ define form function """
    return params.Form(
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


def File(  # noqa: N802
        default: Any = None,
        name=None,
        dest=None,
        required=False,
        ignore=False,
        type=text_type,
        location=("files",),
        choices=(),
        action="store",
        help=None,
        operators=("=",),
        case_sensitive=True,
        store_missing=True,
        trim=False,
        nullable=True,
) -> Any:
    """ define file function """
    return params.File(
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
