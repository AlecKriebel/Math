#!/usr/bin/env python3
"""Portable exact serialization for the corrected DTH pseudomoment.

Only the 125 holomorphic support-coordinate matrices ``A_ijk`` need to be
stored.  All support bases, crossing maps, mixed face charts, trace, and
witness functionals are rebuilt by the verifier.  Version 1 uses one common
denominator per symmetric block; compact version 2 stores each reduced
rational separately.  Both use the source-codec order (diagonal first, then
strict upper triangle lexicographically) and decimal strings, avoiding JSON
integer-token limits for exact correction denominators with thousands of
digits.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path
import gzip
import hashlib
import json
import sys


FORMAT = "dth-corrected-five-replica-pseudomoment-v1"
COMPACT_FORMAT = "dth-corrected-five-replica-pseudomoment-v2-per-entry"


if hasattr(sys, "set_int_max_str_digits"):
    # Exact determinants can legitimately exceed Python's defensive default
    # for human-supplied decimal strings.  Certificate hashes and all algebra
    # are checked after parsing.
    sys.set_int_max_str_digits(0)


def lcm(a, b):
    if not a or not b:
        return 0
    return abs(a // gcd(a, b) * b)


def as_rows(matrix):
    if hasattr(matrix, "tolist"):
        matrix = matrix.tolist()
    return [list(row) for row in matrix]


def symmetric_entries(matrix):
    matrix = as_rows(matrix)
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("coordinate block is not square")
    for i in range(n):
        for j in range(i):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"coordinate block is not symmetric at {i},{j}")
    entries = [Fraction(matrix[i][i]) for i in range(n)]
    entries.extend(Fraction(matrix[i][j])
                   for i in range(n) for j in range(i + 1, n))
    return n, entries


def encode_block(shape, matrix):
    dimension, entries = symmetric_entries(matrix)
    denominator = 1
    for value in entries:
        denominator = lcm(denominator, value.denominator)
    numerators = [
        value.numerator * (denominator // value.denominator)
        for value in entries
    ]
    # Remove a common content so the representation is canonical.
    content = denominator
    for numerator in numerators:
        content = gcd(content, abs(numerator))
    if content > 1:
        denominator //= content
        numerators = [value // content for value in numerators]
    return {
        "shape": "".join(str(int(value)) for value in shape),
        "dimension": dimension,
        "denominator": str(denominator),
        "upper": [str(value) for value in numerators],
    }


def decode_block(data):
    shape_text = data["shape"]
    if len(shape_text) != 3 or any(letter not in "01234" for letter in shape_text):
        raise ValueError("invalid holomorphic shape tag")
    shape = tuple(int(letter) for letter in shape_text)
    n = int(data["dimension"])
    denominator = int(data["denominator"])
    if denominator <= 0:
        raise ValueError("block denominator is not positive")
    raw = [int(value) for value in data["upper"]]
    if len(raw) != n * (n + 1) // 2:
        raise ValueError("wrong number of symmetric block entries")
    values = [Fraction(value, denominator) for value in raw]
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    position = 0
    for i in range(n):
        matrix[i][i] = values[position]
        position += 1
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j] = matrix[j][i] = values[position]
            position += 1
    assert position == len(values)
    return shape, matrix


def encode_compact_block(shape, matrix):
    """Encode each rational independently for substantially smaller gzip.

    The exact correction creates unrelated large denominators in only a
    small subset of entries.  Taking one LCM per block (the v1 format) thus
    expands the compressed certificate by a factor of roughly five.  The v2
    format retains canonical decimal strings for every numerator and
    denominator separately.
    """
    dimension, entries = symmetric_entries(matrix)
    return {
        "shape": "".join(str(int(value)) for value in shape),
        "dimension": dimension,
        "upper": [[str(value.numerator), str(value.denominator)]
                  for value in entries],
    }


def decode_compact_block(data):
    shape_text = data["shape"]
    if len(shape_text) != 3 or any(letter not in "01234" for letter in shape_text):
        raise ValueError("invalid holomorphic shape tag")
    shape = tuple(int(letter) for letter in shape_text)
    n = int(data["dimension"])
    raw = data["upper"]
    if len(raw) != n * (n + 1) // 2:
        raise ValueError("wrong number of symmetric block entries")
    values = []
    for pair in raw:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("invalid compact rational entry")
        numerator, denominator = map(int, pair)
        if denominator <= 0:
            raise ValueError("compact rational denominator is not positive")
        values.append(Fraction(numerator, denominator))
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    position = 0
    for i in range(n):
        matrix[i][i] = values[position]
        position += 1
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j] = matrix[j][i] = values[position]
            position += 1
    assert position == len(values)
    return shape, matrix


def certificate_payload(coordinates, metadata=None):
    expected = tuple(product(range(5), repeat=3))
    if set(coordinates) != set(expected):
        missing = set(expected) - set(coordinates)
        extra = set(coordinates) - set(expected)
        raise ValueError(f"coordinate block mismatch; missing={missing}, extra={extra}")
    return {
        "format": FORMAT,
        "metadata": metadata or {},
        "blocks": [encode_block(shape, coordinates[shape]) for shape in expected],
    }


def compact_certificate_payload(coordinates, metadata=None):
    expected = tuple(product(range(5), repeat=3))
    if set(coordinates) != set(expected):
        missing = set(expected) - set(coordinates)
        extra = set(coordinates) - set(expected)
        raise ValueError(f"coordinate block mismatch; missing={missing}, extra={extra}")
    return {
        "format": COMPACT_FORMAT,
        "metadata": metadata or {},
        "blocks": [encode_compact_block(shape, coordinates[shape])
                   for shape in expected],
    }


def canonical_json(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def write_certificate(path, coordinates, metadata=None):
    path = Path(path)
    text = canonical_json(certificate_payload(coordinates, metadata))
    if path.suffix == ".gz":
        # mtime=0 makes the compressed artifact byte-for-byte reproducible.
        with path.open("wb") as raw:
            with gzip.GzipFile(filename="", fileobj=raw, mode="wb",
                               mtime=0) as handle:
                handle.write(text.encode("ascii"))
    else:
        path.write_text(text, encoding="ascii")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_compact_certificate(path, coordinates, metadata=None):
    path = Path(path)
    text = canonical_json(compact_certificate_payload(coordinates, metadata))
    if path.suffix == ".gz":
        with path.open("wb") as raw:
            with gzip.GzipFile(filename="", fileobj=raw, mode="wb",
                               compresslevel=9, mtime=0) as handle:
                handle.write(text.encode("ascii"))
    else:
        path.write_text(text, encoding="ascii")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_certificate(path):
    path = Path(path)
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="ascii") as handle:
            payload = json.load(handle)
    else:
        payload = json.loads(path.read_text(encoding="ascii"))
    format_name = payload.get("format")
    if format_name not in (FORMAT, COMPACT_FORMAT):
        raise ValueError("unknown DTH certificate format")
    coordinates = {}
    for block in payload["blocks"]:
        if format_name == FORMAT:
            shape, matrix = decode_block(block)
        else:
            shape, matrix = decode_compact_block(block)
        if shape in coordinates:
            raise ValueError(f"duplicate coordinate block {shape}")
        coordinates[shape] = matrix
    expected = set(product(range(5), repeat=3))
    if set(coordinates) != expected:
        raise ValueError("certificate does not contain all 125 ordered blocks")
    return coordinates, payload.get("metadata", {})


def _self_test():
    from tempfile import TemporaryDirectory

    coordinates = {}
    for shape in product(range(5), repeat=3):
        n = (sum(shape) % 3)
        matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                value = Fraction(7 * i - 3 * j + sum(shape), 11 + i + j)
                matrix[i][j] = matrix[j][i] = value
        coordinates[shape] = matrix
    with TemporaryDirectory() as directory:
        path = Path(directory) / "certificate.json.gz"
        first_hash = write_certificate(path, coordinates, {"test": True})
        decoded, metadata = read_certificate(path)
        assert decoded == coordinates
        assert metadata == {"test": True}
        second = Path(directory) / "certificate2.json.gz"
        second_hash = write_certificate(second, decoded, metadata)
        assert first_hash == second_hash
        assert path.read_bytes() == second.read_bytes()
        compact = Path(directory) / "compact.json.gz"
        compact_hash = write_compact_certificate(
            compact, coordinates, {"test": True}
        )
        compact_decoded, compact_metadata = read_certificate(compact)
        assert compact_decoded == coordinates
        assert compact_metadata == {"test": True}
        compact_second = Path(directory) / "compact2.json.gz"
        assert write_compact_certificate(
            compact_second, compact_decoded, compact_metadata
        ) == compact_hash
        assert compact.read_bytes() == compact_second.read_bytes()
    print("exact DTH certificate serialization passed")


if __name__ == "__main__":
    _self_test()
