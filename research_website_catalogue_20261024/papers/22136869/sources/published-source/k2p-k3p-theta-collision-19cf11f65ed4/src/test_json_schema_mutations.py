#!/usr/bin/env python3
"""Hostile raw-JSON and closed-schema regressions for all certificates."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from strict_json import load_canonical_certificate


CERTIFICATE_NAMES = (
    "certificate_k2p_simple.json",
    "certificate_k2p_continuous_time.json",
    "certificate_k3p.json",
    "jacobian_certificate_k3p.json",
    "continuous_time_certificate_k3p.json",
)


def python_command(script: Path, *arguments: Path) -> list[str]:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-" + "O" * sys.flags.optimize)
    command.append(str(script))
    command.extend(str(argument) for argument in arguments)
    return command


def require_failure(
    name: str, command: list[str], cwd: Path, diagnostic: str
) -> None:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    combined = completed.stdout + completed.stderr
    if completed.returncode == 0:
        raise RuntimeError(f"raw/schema mutation unexpectedly passed: {name}")
    if diagnostic not in combined:
        raise RuntimeError(
            f"mutation {name!r} failed for the wrong reason; expected "
            f"{diagnostic!r}\n{combined}"
        )
    print(f"[JSON mutation rejection] PASS  {name}: {diagnostic}")


def duplicate_first_key(raw: str, key: str, bogus_json: str) -> str:
    marker = f'"{key}":'
    if raw.count(marker) != 1:
        raise RuntimeError(f"expected one raw occurrence of {marker}")
    return raw.replace(marker, f'"{key}": {bogus_json},\n  {marker}', 1)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def run_simple_k2p(
    name: str, transform: Callable[[str, dict[str, object]], str], diagnostic: str
) -> None:
    source = ROOT / "certificate_k2p_simple.json"
    parsed = copy.deepcopy(load_canonical_certificate(source))
    raw = transform(source.read_text(encoding="utf-8"), parsed)
    with tempfile.TemporaryDirectory(prefix="k2p-json-schema-") as temp_name:
        directory = Path(temp_name)
        shutil.copy2(ROOT / "verify_k2p_simple.py", directory / "verify_k2p_simple.py")
        shutil.copy2(ROOT / "strict_json.py", directory / "strict_json.py")
        (directory / source.name).write_text(raw, encoding="utf-8")
        require_failure(
            name,
            python_command(directory / "verify_k2p_simple.py"),
            directory,
            diagnostic,
        )


def run_ct_k2p(
    name: str, transform: Callable[[str, dict[str, object]], str], diagnostic: str
) -> None:
    source = ROOT / "certificate_k2p_continuous_time.json"
    parsed = copy.deepcopy(load_canonical_certificate(source))
    raw = transform(source.read_text(encoding="utf-8"), parsed)
    with tempfile.TemporaryDirectory(prefix="k2p-ct-json-schema-") as temp_name:
        directory = Path(temp_name)
        (directory / "src").mkdir()
        shutil.copy2(ROOT / "src" / "verify_k2p_extended.py", directory / "src" / "verify_k2p_extended.py")
        shutil.copy2(ROOT / "strict_json.py", directory / "strict_json.py")
        (directory / source.name).write_text(raw, encoding="utf-8")
        require_failure(
            name,
            python_command(directory / "src" / "verify_k2p_extended.py"),
            directory,
            diagnostic,
        )


def write_k3p_bundle(
    directory: Path,
    certificate_raw: str,
    certificate: dict[str, object],
    *,
    jacobian_raw: str | None = None,
    continuous_time_raw: str | None = None,
) -> Path:
    certificate_path = directory / "certificate_k3p.json"
    certificate_path.write_text(certificate_raw, encoding="utf-8")
    if jacobian_raw is None:
        jacobian_raw = json.dumps(certificate["jacobian"], indent=2) + "\n"
    if continuous_time_raw is None:
        continuous_time_raw = (
            json.dumps(certificate["continuous_time"], indent=2) + "\n"
        )
    (directory / "jacobian_certificate_k3p.json").write_text(
        jacobian_raw, encoding="utf-8"
    )
    (directory / "continuous_time_certificate_k3p.json").write_text(
        continuous_time_raw, encoding="utf-8"
    )
    return certificate_path


def run_k3p(
    name: str,
    certificate_raw: str,
    certificate: dict[str, object],
    diagnostic: str,
    *,
    jacobian_raw: str | None = None,
    continuous_time_raw: str | None = None,
) -> None:
    with tempfile.TemporaryDirectory(prefix="k3p-json-schema-") as temp_name:
        directory = Path(temp_name)
        certificate_path = write_k3p_bundle(
            directory,
            certificate_raw,
            certificate,
            jacobian_raw=jacobian_raw,
            continuous_time_raw=continuous_time_raw,
        )
        require_failure(
            name,
            python_command(ROOT / "src" / "verify_k3p.py", certificate_path),
            ROOT,
            diagnostic,
        )


def dumped_with_extra(
    _raw: str, value: dict[str, object], path: tuple[str, ...] = ()
) -> str:
    target = value
    for key in path:
        target = target[key]
    target["unverified_claim"] = True
    return json.dumps(value, indent=2) + "\n"


def main() -> None:
    for filename in CERTIFICATE_NAMES:
        load_canonical_certificate(ROOT / filename)
    print("[strict JSON] PASS  all five canonical certificates have unique keys and closed schemas")

    run_simple_k2p(
        "compact K2P duplicate top-level key",
        lambda raw, _value: duplicate_first_key(raw, "schema_version", '"bogus"'),
        "duplicate JSON object key 'schema_version'",
    )
    run_simple_k2p(
        "compact K2P unknown top-level field",
        lambda raw, value: dumped_with_extra(raw, value),
        "closed JSON schema mismatch",
    )
    run_simple_k2p(
        "compact K2P unknown nested vertex field",
        lambda _raw, value: (
            value["rooted_network"]["vertices"][0].__setitem__("unverified_claim", True)
            or json.dumps(value, indent=2) + "\n"
        ),
        "closed JSON schema mismatch",
    )
    run_simple_k2p(
        "compact K2P non-standard NaN constant",
        lambda raw, _value: raw.replace('"schema_version": "1.0"', '"schema_version": NaN', 1),
        "non-standard JSON numeric constant 'NaN'",
    )

    run_ct_k2p(
        "continuous-time K2P duplicate top-level key",
        lambda raw, _value: duplicate_first_key(raw, "schema_version", '"bogus"'),
        "duplicate JSON object key 'schema_version'",
    )
    run_ct_k2p(
        "continuous-time K2P unknown top-level field",
        lambda raw, value: dumped_with_extra(raw, value),
        "closed JSON schema mismatch",
    )

    k3p_path = ROOT / "certificate_k3p.json"
    k3p_raw = k3p_path.read_text(encoding="utf-8")
    k3p = copy.deepcopy(load_canonical_certificate(k3p_path))
    run_k3p(
        "K3P duplicate top-level key",
        duplicate_first_key(k3p_raw, "schema_version", '"bogus"'),
        k3p,
        "duplicate JSON object key 'schema_version'",
    )

    nested_duplicate = k3p_raw.replace(
        '"id": "rho",', '"id": "shadowed",\n        "id": "rho",', 1
    )
    run_k3p(
        "K3P duplicate nested vertex key",
        nested_duplicate,
        k3p,
        "duplicate JSON object key 'id'",
    )

    extra_rooted = copy.deepcopy(k3p)
    extra_rooted["rooted_network"]["unverified_claim"] = True
    run_k3p(
        "K3P unknown rooted-network field",
        json.dumps(extra_rooted, indent=2) + "\n",
        extra_rooted,
        "closed JSON schema mismatch",
    )

    extra_arc = copy.deepcopy(k3p)
    extra_arc["rooted_network"]["arcs"][0]["unverified_claim"] = True
    run_k3p(
        "K3P unknown operative arc field",
        json.dumps(extra_arc, indent=2) + "\n",
        extra_arc,
        "closed JSON schema mismatch",
    )

    shifted_row_shape = copy.deepcopy(k3p)
    shifted_row_shape["rooted_network"]["vertices"][-1] = {
        "id": "shadow",
        "type": "tree",
    }
    run_k3p(
        "K3P same-length row-shape multiplicity shift",
        json.dumps(shifted_row_shape, indent=2) + "\n",
        shifted_row_shape,
        "closed JSON schema mismatch",
    )

    extra_embedded = copy.deepcopy(k3p)
    extra_embedded["jacobian"]["unverified_claim"] = True
    extra_embedded["continuous_time"]["unverified_claim"] = True
    run_k3p(
        "K3P coordinated embedded-and-sidecar extra fields",
        json.dumps(extra_embedded, indent=2) + "\n",
        extra_embedded,
        "closed JSON schema mismatch",
    )

    jacobian_raw = (ROOT / "jacobian_certificate_k3p.json").read_text(encoding="utf-8")
    duplicate_jacobian = duplicate_first_key(
        jacobian_raw, "ambient_space", '"shadowed"'
    )
    run_k3p(
        "K3P Jacobian sidecar duplicate key",
        k3p_raw,
        k3p,
        "duplicate JSON object key 'ambient_space'",
        jacobian_raw=duplicate_jacobian,
    )

    ct_raw = (ROOT / "continuous_time_certificate_k3p.json").read_text(encoding="utf-8")
    duplicate_ct = duplicate_first_key(ct_raw, "method", '"shadowed"')
    run_k3p(
        "K3P continuous-time sidecar duplicate key",
        k3p_raw,
        k3p,
        "duplicate JSON object key 'method'",
        continuous_time_raw=duplicate_ct,
    )

    print("\nALL STRICT JSON AND CLOSED-SCHEMA MUTATION CHECKS PASSED")


if __name__ == "__main__":
    main()
