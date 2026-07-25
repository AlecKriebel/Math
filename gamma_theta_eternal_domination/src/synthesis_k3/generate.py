"""Deterministically generate a k=3 synthesis CNF and its manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import tempfile
from pathlib import Path
from typing import Sequence

from .encoding import TEMPLATES, build_k3_encoding, same_color_cut


SCHEMA_VERSION = 2
RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/synthesis_k3/__init__.py",
    "src/synthesis_k3/encoding.py",
    "src/synthesis_k3/generate.py",
    "math/synthesis_k3_cegar_design.md",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".partial",
        dir=path.parent,
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _reject_constant(value: str) -> object:
    raise ValueError(f"non-finite JSON constant {value!r}")


def _object_without_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _canonical_coloring(raw: object, index: int) -> tuple[int, ...]:
    if not isinstance(raw, list):
        raise ValueError(f"coloring {index} is not a list")
    coloring = tuple(raw)
    if len(coloring) != 12 or any(
        type(color) is not int or color not in (0, 1, 2)
        for color in coloring
    ):
        raise ValueError(f"coloring {index} is not a 12-vertex 3-color row")
    relabel: dict[int, int] = {}
    canonical: list[int] = []
    for color in coloring:
        if color not in relabel:
            relabel[color] = len(relabel)
        canonical.append(relabel[color])
    return tuple(canonical)


def load_coloring_bytes(
    payload: bytes,
) -> tuple[tuple[int, ...], ...]:
    try:
        decoded = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("coloring-cut file is not UTF-8") from error
    try:
        parsed = json.loads(
            decoded,
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("malformed coloring-cut JSON") from error
    if not isinstance(parsed, list):
        raise ValueError("coloring-cut file must be a JSON list")
    result: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for index, raw in enumerate(parsed):
        canonical = _canonical_coloring(raw, index)
        if canonical in seen:
            raise ValueError(
                f"duplicate coloring partition at row {index}"
            )
        seen.add(canonical)
        result.append(canonical)
    return tuple(result)


def load_colorings(path: Path | None) -> tuple[tuple[int, ...], ...]:
    if path is None:
        return ()
    return load_coloring_bytes(path.read_bytes())


def _same_file_if_existing(first: Path, second: Path) -> bool:
    try:
        return os.path.samefile(first, second)
    except FileNotFoundError:
        return False


def _validate_path_roles(
    *,
    output: Path,
    manifest: Path,
    colorings_path: Path | None,
    trusted_sources: Sequence[Path],
) -> tuple[Path, Path, Path | None]:
    roles: list[tuple[str, Path]] = [
        ("output", output),
        ("manifest", manifest),
    ]
    if colorings_path is not None:
        roles.append(("colorings", colorings_path))
    roles.extend(
        (f"trusted source {source.name}", source)
        for source in trusted_sources
    )
    resolved = [(name, candidate.resolve(strict=False)) for name, candidate in roles]
    writable_names = {"output", "manifest"}
    for index, (first_name, first_path) in enumerate(resolved):
        for second_name, second_path in resolved[index + 1 :]:
            if not (
                first_name in writable_names or second_name in writable_names
            ):
                continue
            if (
                first_path == second_path
                or _same_file_if_existing(roles[index][1], dict(roles)[second_name])
            ):
                raise ValueError(
                    f"path roles collide: {first_name} and {second_name}"
                )
    return (
        dict(resolved)["output"],
        dict(resolved)["manifest"],
        dict(resolved).get("colorings"),
    )


def runtime_source_manifest() -> tuple[tuple[str, str], ...]:
    campaign_root = Path(__file__).resolve().parents[2]
    records: list[tuple[str, str]] = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        source = campaign_root / relative
        if not source.is_file():
            raise ValueError(f"missing runtime source {source}")
        records.append((relative, sha256_file(source)))
    return tuple(records)


def source_set_sha256(
    records: Sequence[tuple[str, str]],
) -> str:
    payload = "".join(
        f"{relative} {digest}\n" for relative, digest in records
    ).encode("ascii")
    return sha256_bytes(payload)


def generate(
    *,
    template: str,
    output: Path,
    manifest: Path,
    colorings_path: Path | None = None,
) -> dict[str, object]:
    source_manifest = runtime_source_manifest()
    campaign_root = Path(__file__).resolve().parents[2]
    trusted_sources = tuple(
        campaign_root / relative for relative, _ in source_manifest
    )
    output, manifest, resolved_colorings = _validate_path_roles(
        output=output,
        manifest=manifest,
        colorings_path=colorings_path,
        trusted_sources=trusted_sources,
    )
    coloring_bytes = (
        resolved_colorings.read_bytes()
        if resolved_colorings is not None
        else None
    )
    colorings_hash = (
        sha256_bytes(coloring_bytes) if coloring_bytes is not None else None
    )
    colorings = (
        load_coloring_bytes(coloring_bytes)
        if coloring_bytes is not None
        else ()
    )

    encoding = build_k3_encoding(template)
    cut_hash = hashlib.sha256()
    for coloring in colorings:
        clause = same_color_cut(encoding, coloring)
        encoding.cnf.add_clause(clause)
        cut_hash.update(
            (" ".join(map(str, coloring)) + "\n").encode("ascii")
        )

    dimacs = encoding.cnf.dimacs().encode("ascii")
    atomic_write(output, dimacs)
    installed_cnf_hash = sha256_file(output)
    if installed_cnf_hash != sha256_bytes(dimacs):
        raise ValueError("installed CNF bytes changed after atomic write")
    if resolved_colorings is not None:
        if sha256_file(resolved_colorings) != colorings_hash:
            raise ValueError("coloring input changed during generation")

    normalized_invocation = [
        "/usr/bin/env",
        f"PYTHONPATH={campaign_root / 'src'}",
        sys.executable,
        "-m",
        "synthesis_k3.generate",
        "--template",
        template,
        "--output",
        str(output),
        "--manifest",
        str(manifest),
    ]
    if resolved_colorings is not None:
        normalized_invocation.extend(
            ("--colorings", str(resolved_colorings))
        )
    result: dict[str, object] = {
        "schema": "gamma-theta-k3-cnf-v2",
        "schema_version": SCHEMA_VERSION,
        "template": template,
        "order": 12,
        "variable_count": encoding.cnf.variable_count,
        "clause_count": len(encoding.cnf.clauses),
        "literal_count": sum(map(len, encoding.cnf.clauses)),
        "coloring_cut_count": len(colorings),
        "coloring_cut_stream_sha256": cut_hash.hexdigest(),
        "colorings_path": (
            str(resolved_colorings) if resolved_colorings is not None else None
        ),
        "colorings_sha256": colorings_hash,
        "cnf_path": str(output),
        "cnf_sha256": installed_cnf_hash,
        "generator_source_manifest": [
            [relative, digest] for relative, digest in source_manifest
        ],
        "generator_source_set_sha256": source_set_sha256(source_manifest),
        "python_executable": sys.executable,
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "working_directory": str(campaign_root),
        "required_environment": {
            "PYTHONPATH": str(campaign_root / "src"),
        },
        "normalized_invocation": normalized_invocation,
    }
    atomic_write(
        manifest,
        (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", choices=TEMPLATES, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--colorings", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    result = generate(
        template=arguments.template,
        output=arguments.output,
        manifest=arguments.manifest,
        colorings_path=arguments.colorings,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
