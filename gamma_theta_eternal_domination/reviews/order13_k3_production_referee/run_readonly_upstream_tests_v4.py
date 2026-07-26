#!/usr/bin/env python3
"""Run all current focused tests without modifying shared source bytes.

Twenty-four tests are read-only with respect to the repository.  The one test
that deliberately mutates helper sources is run in a private full ``src``
mirror, where its restoration behavior is still exercised exactly.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REVIEW = Path(__file__).resolve().parent
CAMPAIGN = REVIEW.parents[1]
TEST_FILE = CAMPAIGN / "tests/test_order13_k3_production.py"
SOURCE_MUTATION_TEST = (
    "test_transitive_helper_source_mutations_refuse_before_child"
)
EXPECTED_READONLY_COUNT = 24
EXPECTED_TOTAL_COUNT = 25
FROZEN = {
    "src/search/order13_k3/production.py": (
        "7223e9c789b50aa021371f07670af9ee1a2406fd649e1d84713ed4b566a7f11e"
    ),
    "src/search/order13_k3/normalize_bdrat.py": (
        "a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c"
    ),
    "src/search/order13_k3/PRODUCTION_PROTOCOL.md": (
        "cec85e105e1372dc09de055f2b74bc80709b1a732c64541869c8106b6f2316a9"
    ),
    "tests/test_order13_k3_production.py": (
        "51655e8764db2ad436e84041a8b81e83e07131bfdd88084158d6b8800052cc0a"
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def frozen_hashes() -> dict[str, str]:
    return {relative: sha256(CAMPAIGN / relative) for relative in FROZEN}


def main() -> int:
    before = frozen_hashes()
    if before != FROZEN:
        raise AssertionError("v4 focused-test target bytes changed")

    specification = importlib.util.spec_from_file_location(
        "order13_k3_production_final_v4_tests", TEST_FILE
    )
    if specification is None or specification.loader is None:
        raise AssertionError("could not load current focused tests")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    test_class = module.Order13K3ProductionTests
    all_names = sorted(
        unittest.defaultTestLoader.getTestCaseNames(test_class)
    )
    selected = [name for name in all_names if name != SOURCE_MUTATION_TEST]
    if (
        len(all_names) != EXPECTED_TOTAL_COUNT
        or len(selected) != EXPECTED_READONLY_COUNT
    ):
        raise AssertionError(
            f"selected {len(selected)} of {len(all_names)} focused tests"
        )
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestSuite(test_class(name) for name in selected)
    )
    if not result.wasSuccessful():
        return 1

    with tempfile.TemporaryDirectory(
        prefix="order13-k3-v4-source-mirror-"
    ) as temporary:
        mirror = Path(temporary).resolve()
        shutil.copytree(
            CAMPAIGN / "src",
            mirror / "src",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        (mirror / "tests").mkdir()
        shutil.copyfile(
            TEST_FILE, mirror / "tests/test_order13_k3_production.py"
        )
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PYTHONPATH"] = str(mirror / "src")
        isolated = subprocess.run(
            [
                sys.executable,
                str(mirror / "tests/test_order13_k3_production.py"),
                (
                    "Order13K3ProductionTests."
                    + SOURCE_MUTATION_TEST
                ),
                "-v",
            ],
            cwd=mirror,
            env=environment,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
        )
        sys.stdout.write(isolated.stdout.decode("utf-8", errors="replace"))
        if isolated.returncode != 0:
            return 1

    after = frozen_hashes()
    if after != before:
        raise AssertionError("focused replay changed shared source bytes")
    print(
        json.dumps(
            {
                "focused_tests_passed": EXPECTED_TOTAL_COUNT,
                "shared_readonly_tests_passed": EXPECTED_READONLY_COUNT,
                "isolated_source_mutation_tests_passed": 1,
                "shared_source_bytes_unchanged": True,
                "real_solver_executions": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
