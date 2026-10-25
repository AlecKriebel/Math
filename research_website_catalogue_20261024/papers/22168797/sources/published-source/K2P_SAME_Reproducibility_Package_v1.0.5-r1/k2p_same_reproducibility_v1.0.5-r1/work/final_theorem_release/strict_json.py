#!/usr/bin/env python3
"""Bounded, duplicate-aware readers for release JSON and compressed ledgers.

The release uses pretty-printed plain ``.json`` documents and compact canonical
``.json.gz`` / ``.jsonl.gz`` evidence.  Python's default decoder silently keeps
the last occurrence of a repeated object name, so no release boundary should
call it directly.  These readers reject repeated names at every nesting depth,
non-finite numeric constants, excessive compressed/decompressed inputs, and
noncanonical compressed payloads.
"""

from __future__ import annotations

import gzip
import io
import json
import math
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Iterator


MAX_PLAIN_JSON_BYTES = 64 * 1024 * 1024
MAX_COMPRESSED_JSON_BYTES = 512 * 1024 * 1024
MAX_GZIP_JSON_DOCUMENT_BYTES = 64 * 1024 * 1024
MAX_GZIP_JSONL_LINE_BYTES = 16 * 1024 * 1024
MAX_GZIP_JSONL_TOTAL_BYTES = 4 * 1024 * 1024 * 1024


class StrictJSONError(ValueError):
    """A deterministic release-JSON syntax, ambiguity, or bound failure."""


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (RecursionError, TypeError, ValueError) as error:
        raise StrictJSONError(f"STRICT_JSON_CANONICAL_ENCODING_FAIL:{error}") from error


def _bounded_token(token: str, limit: int = 96) -> str:
    return token if len(token) <= limit else token[: limit - 3] + "..."


def _reject_constant(label: str, token: str) -> None:
    raise StrictJSONError(
        f"STRICT_JSON_NONFINITE_NUMBER:{label}:token={_bounded_token(token)}"
    )


def _parse_finite_float(label: str, token: str) -> float:
    value = float(token)
    if not math.isfinite(value):
        raise StrictJSONError(
            f"STRICT_JSON_NONFINITE_NUMBER:{label}:token={_bounded_token(token)}"
        )
    return value


def _unique_object(label: str):
    def build(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for name, value in pairs:
            if name in result:
                raise StrictJSONError(
                    f"STRICT_JSON_DUPLICATE_NAME:{label}:"
                    f"name={_bounded_token(repr(name))}"
                )
            result[name] = value
        return result

    return build


def decode_json_document(
    data: str | bytes,
    *,
    label: str,
    max_bytes: int = MAX_PLAIN_JSON_BYTES,
    require_object: bool = False,
    require_canonical_bytes: bool = False,
    require_terminal_newline: bool = False,
) -> Any:
    """Decode one bounded JSON document with recursive duplicate rejection."""

    if isinstance(data, str):
        encoded = data.encode("utf-8")
    elif isinstance(data, bytes):
        encoded = data
    else:
        raise StrictJSONError(f"STRICT_JSON_INPUT_TYPE_FAIL:{label}")
    if len(encoded) > max_bytes:
        raise StrictJSONError(
            f"STRICT_JSON_BYTE_LIMIT:{label}:observed={len(encoded)}:limit={max_bytes}"
        )
    try:
        text = encoded.decode("utf-8")
    except UnicodeDecodeError as error:
        raise StrictJSONError(
            f"STRICT_JSON_UTF8_FAIL:{label}:offset={error.start}"
        ) from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=_unique_object(label),
            parse_constant=lambda token: _reject_constant(label, token),
            parse_float=lambda token: _parse_finite_float(label, token),
        )
    except StrictJSONError:
        raise
    except RecursionError as error:
        raise StrictJSONError(f"STRICT_JSON_DEPTH_FAIL:{label}") from error
    except json.JSONDecodeError as error:
        raise StrictJSONError(
            f"STRICT_JSON_SYNTAX_FAIL:{label}:line={error.lineno}:column={error.colno}"
        ) from error
    except ValueError as error:
        raise StrictJSONError(f"STRICT_JSON_VALUE_FAIL:{label}:{error}") from error
    if require_object and not isinstance(value, dict):
        raise StrictJSONError(f"STRICT_JSON_TOP_LEVEL_OBJECT_FAIL:{label}")
    if require_canonical_bytes:
        expected = canonical_json_bytes(value)
        if require_terminal_newline:
            expected += b"\n"
        if encoded != expected:
            raise StrictJSONError(f"STRICT_JSON_NONCANONICAL_BYTES:{label}")
    elif require_terminal_newline and not encoded.endswith(b"\n"):
        raise StrictJSONError(f"STRICT_JSON_TERMINAL_NEWLINE_FAIL:{label}")
    return value


@contextmanager
def _compressed_stream(
    source: Path | bytes,
    *,
    label: str,
    max_compressed_bytes: int,
) -> Iterator[BinaryIO]:
    if isinstance(source, Path):
        try:
            size = source.stat().st_size
        except OSError as error:
            raise StrictJSONError(f"STRICT_JSON_GZIP_READ_FAIL:{label}:{error}") from error
        if size > max_compressed_bytes:
            raise StrictJSONError(
                f"STRICT_JSON_COMPRESSED_BYTE_LIMIT:{label}:observed={size}:"
                f"limit={max_compressed_bytes}"
            )
        raw_context = source.open("rb")
    elif isinstance(source, bytes):
        if len(source) > max_compressed_bytes:
            raise StrictJSONError(
                f"STRICT_JSON_COMPRESSED_BYTE_LIMIT:{label}:observed={len(source)}:"
                f"limit={max_compressed_bytes}"
            )
        raw_context = io.BytesIO(source)
    else:
        raise StrictJSONError(f"STRICT_JSON_GZIP_INPUT_TYPE_FAIL:{label}")
    try:
        with raw_context as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as expanded:
                yield expanded
    except (EOFError, OSError) as error:
        raise StrictJSONError(f"STRICT_JSON_GZIP_READ_FAIL:{label}:{error}") from error


def load_canonical_gzip_json(
    source: Path | bytes,
    *,
    label: str,
    max_compressed_bytes: int = MAX_COMPRESSED_JSON_BYTES,
    max_decompressed_bytes: int = MAX_GZIP_JSON_DOCUMENT_BYTES,
    require_object: bool = True,
) -> Any:
    """Load one compact-canonical gzip JSON document with an expansion cap."""

    with _compressed_stream(
        source, label=label, max_compressed_bytes=max_compressed_bytes
    ) as expanded:
        data = expanded.read(max_decompressed_bytes + 1)
        if len(data) > max_decompressed_bytes:
            raise StrictJSONError(
                f"STRICT_JSON_DECOMPRESSED_BYTE_LIMIT:{label}:"
                f"limit={max_decompressed_bytes}"
            )
    return decode_json_document(
        data,
        label=label,
        max_bytes=max_decompressed_bytes,
        require_object=require_object,
        require_canonical_bytes=True,
        require_terminal_newline=True,
    )


def iter_canonical_gzip_jsonl(
    source: Path | bytes,
    *,
    label: str,
    max_compressed_bytes: int = MAX_COMPRESSED_JSON_BYTES,
    max_line_bytes: int = MAX_GZIP_JSONL_LINE_BYTES,
    max_total_bytes: int = MAX_GZIP_JSONL_TOTAL_BYTES,
    require_object: bool = True,
) -> Iterator[Any]:
    """Stream compact-canonical gzip JSONL with line and expansion caps."""

    total = 0
    line_number = 0
    with _compressed_stream(
        source, label=label, max_compressed_bytes=max_compressed_bytes
    ) as expanded:
        while True:
            raw_line = expanded.readline(max_line_bytes + 1)
            if not raw_line:
                break
            line_number += 1
            if len(raw_line) > max_line_bytes:
                raise StrictJSONError(
                    f"STRICT_JSON_LINE_BYTE_LIMIT:{label}:line={line_number}:"
                    f"limit={max_line_bytes}"
                )
            total += len(raw_line)
            if total > max_total_bytes:
                raise StrictJSONError(
                    f"STRICT_JSON_DECOMPRESSED_BYTE_LIMIT:{label}:"
                    f"limit={max_total_bytes}"
                )
            row_label = f"{label}:line={line_number}"
            if not raw_line.endswith(b"\n"):
                raise StrictJSONError(
                    f"STRICT_JSON_TERMINAL_NEWLINE_FAIL:{row_label}"
                )
            if raw_line == b"\n":
                raise StrictJSONError(f"STRICT_JSON_BLANK_LINE:{row_label}")
            yield decode_json_document(
                raw_line,
                label=row_label,
                max_bytes=max_line_bytes,
                require_object=require_object,
                require_canonical_bytes=True,
                require_terminal_newline=True,
            )


def validate_release_json_member(relative: str, data: bytes) -> None:
    """Validate JSON content according to its complete release suffix."""

    name = PurePosixPath(relative).name
    if name.endswith(".jsonl.gz"):
        for _ in iter_canonical_gzip_jsonl(data, label=relative):
            pass
    elif name.endswith(".json.gz"):
        load_canonical_gzip_json(data, label=relative)
    elif name.endswith(".json"):
        decode_json_document(data, label=relative, require_object=False)
