#!/usr/bin/env python3
"""Shared exact helpers for the read-only PC-PARTIAL derivations."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
COMPRESSION_ROOT = HERE.parent
PROJECT = COMPRESSION_ROOT.parent
TEMPLATES = COMPRESSION_ROOT / "templates"


class CompressionFailure(RuntimeError):
    """Fail-closed error raised by the compression derivations."""


def require(condition: bool, code: str, detail: Any | None = None) -> None:
    if not condition:
        suffix = "" if detail is None else f":{detail}"
        raise CompressionFailure(f"{code}{suffix}")


def reject_optimized_python() -> None:
    require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), "JSON_INPUT_MISSING", path)
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON_INPUT_NOT_OBJECT", path)
    return value


def load_gzip_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), "GZIP_JSON_INPUT_MISSING", path)
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), "GZIP_JSON_INPUT_NOT_OBJECT", path)
    return value


def iter_gzip_json_lines(path: Path) -> Iterable[dict[str, Any]]:
    require(path.is_file(), "JSONL_INPUT_MISSING", path)
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            value = json.loads(line)
            require(
                isinstance(value, dict),
                "JSONL_ROW_NOT_OBJECT",
                f"{path}:{line_number}",
            )
            yield value


def sealed(payload: dict[str, Any]) -> dict[str, Any]:
    require("payload_sha256" not in payload, "PAYLOAD_ALREADY_SEALED")
    result = dict(payload)
    result["payload_sha256"] = sha_object(payload)
    return result


def verify_seal(value: dict[str, Any]) -> None:
    observed = value.get("payload_sha256")
    require(isinstance(observed, str), "PAYLOAD_HASH_MISSING")
    payload = dict(value)
    payload.pop("payload_sha256")
    require(observed == sha_object(payload), "PAYLOAD_HASH_MISMATCH")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, value: str) -> None:
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def project_path(relative: str) -> Path:
    requested = Path(relative)
    require(not requested.is_absolute(), "ABSOLUTE_FROZEN_PATH_FORBIDDEN", relative)
    require(".." not in requested.parts, "FROZEN_PATH_ESCAPE_FORBIDDEN", relative)
    path = PROJECT / requested
    require(path.resolve().is_relative_to(PROJECT.resolve()), "FROZEN_PATH_ESCAPE", relative)
    require(path.is_file(), "FROZEN_INPUT_MISSING", relative)
    return path


def input_binding(relative: str) -> dict[str, Any]:
    path = project_path(relative)
    return {
        "path": relative,
        "sha256": sha_file(path),
        "bytes": path.stat().st_size,
    }


def extension_key(path: Path) -> str:
    name = path.name
    for suffix in (".jsonl.gz", ".json.gz", ".sha256"):
        if name.endswith(suffix):
            return suffix
    return path.suffix or "[none]"


def noncomment_sloc(path: Path) -> tuple[int, int]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    sloc = sum(
        1
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    )
    return len(lines), sloc


def direct_terminal_id(source_index: int, class_id: int) -> str:
    return f"source_{source_index}:class_{class_id:06d}"


def literal_quadratic_body(
    certificate: dict[str, Any],
    *,
    coordinate_port_count: int,
    coordinate_convention_id: str,
) -> dict[str, Any]:
    required = ("coefficients", "coordinate_pairs", "degree", "weight")
    require(
        all(key in certificate for key in required),
        "QUADRATIC_BODY_FIELDS_MISSING",
        sorted(certificate),
    )
    require(certificate["degree"] == 2, "QUADRATIC_DEGREE_FAIL")
    coefficients = certificate["coefficients"]
    pairs = certificate["coordinate_pairs"]
    weight = certificate["weight"]
    require(isinstance(coordinate_port_count, int), "PORT_COUNT_NOT_INTEGER")
    require(coordinate_port_count > 0, "PORT_COUNT_NOT_POSITIVE")
    require(
        isinstance(coordinate_convention_id, str) and coordinate_convention_id,
        "COORDINATE_CONVENTION_MISSING",
    )
    require(isinstance(coefficients, list), "QUADRATIC_COEFFICIENTS_NOT_LIST")
    require(isinstance(pairs, list), "QUADRATIC_PAIRS_NOT_LIST")
    require(len(coefficients) == len(pairs) > 0, "QUADRATIC_TERM_LENGTH_FAIL")
    require(
        all(isinstance(value, int) and not isinstance(value, bool) for value in coefficients),
        "QUADRATIC_COEFFICIENT_NOT_INTEGER",
    )
    require(any(value != 0 for value in coefficients), "ZERO_QUADRATIC_BODY")
    nonzero = [abs(value) for value in coefficients if value]
    require(math.gcd(*nonzero) == 1, "QUADRATIC_NOT_PRIMITIVE")
    require(next(value for value in coefficients if value) > 0, "QUADRATIC_SIGN_NOT_NORMALIZED")
    coordinate_bound = 4**coordinate_port_count
    for pair in pairs:
        require(isinstance(pair, list) and len(pair) == 2, "QUADRATIC_PAIR_SHAPE")
        require(
            all(
                isinstance(index, int)
                and not isinstance(index, bool)
                and 0 <= index < coordinate_bound
                for index in pair
            ),
            "QUADRATIC_PAIR_INDEX_RANGE",
            pair,
        )
    require(isinstance(weight, list), "QUADRATIC_WEIGHT_NOT_LIST")
    require(len(weight) == 2 * coordinate_port_count, "QUADRATIC_WEIGHT_ARITY")
    require(
        all(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0
            for value in weight
        ),
        "QUADRATIC_WEIGHT_ENTRY",
    )
    return {
        **{key: certificate[key] for key in required},
        "coordinate_port_count": coordinate_port_count,
        "coordinate_convention_id": coordinate_convention_id,
    }


def format_quadratic(body: dict[str, Any], coordinate: str = "q") -> str:
    terms: list[str] = []
    for coefficient, pair in zip(
        body["coefficients"], body["coordinate_pairs"], strict=True
    ):
        if coefficient == 0:
            continue
        monomial = f"{coordinate}_{{{pair[0]}}}{coordinate}_{{{pair[1]}}}"
        if not terms:
            terms.append(monomial if coefficient == 1 else f"{coefficient}{monomial}")
        elif coefficient == 1:
            terms.append(f"+{monomial}")
        elif coefficient == -1:
            terms.append(f"-{monomial}")
        elif coefficient > 0:
            terms.append(f"+{coefficient}{monomial}")
        else:
            terms.append(f"{coefficient}{monomial}")
    require(bool(terms), "ZERO_QUADRATIC_BODY")
    return "".join(terms)
