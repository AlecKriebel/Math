"""Bounded adversarial probes for ``src/search/extension_killtest.py``.

This script never launches the 110,537-origin campaign.  It demonstrates:

1. the executable hash pin rejects a same-order/same-size but nonisomorphic
   counterfeit canonicalizer;
2. the hardened candidate-state check stops on and exposes an inconsistent
   pending marker; and
3. non-finite resource limits are rejected;
4. the final-batch/host-hash crash window (pending hardening).
"""

from __future__ import annotations

import sqlite3
import shutil
import sys
import tempfile
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

import search.extension_killtest as engine  # noqa: E402
from search.extension_killtest import (  # noqa: E402
    Evaluation,
    build_configuration,
    run_extension_search,
    verify_pinned_labelg,
)
from verifier_a.core import BitGraph  # noqa: E402


CATALOG = CAMPAIGN / "instances" / "mmv2022_table9.csv"
PARAMETERS = CAMPAIGN / "results" / "mmv2022_parameters.csv"
REAL_LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"
NAUTY_ARCHIVE = CAMPAIGN / "tools" / "nauty2_9_3.tar.gz"


def probe_counterfeit_labelg(root: Path) -> None:
    fake_tree = root / "nauty2_9_3"
    fake_tree.mkdir(parents=True)
    shutil.copyfile(
        NAUTY_ARCHIVE,
        fake_tree.parent / "nauty2_9_3.tar.gz",
    )
    (fake_tree / "This_is_nauty2_9_3.txt").write_bytes(b"")
    fake = fake_tree / "labelg"
    fake.write_text(
        "#!/usr/bin/env python3\n"
        "import sys\n"
        "for line in sys.stdin:\n"
        "    if line.strip():\n"
        "        print('Cs')\n",
        encoding="ascii",
    )
    fake.chmod(0o755)

    # P4 and K1,3 both have order four and size three but are nonisomorphic.
    path4 = BitGraph.path(4)
    star = BitGraph.from_edges(4, ((0, 1), (0, 2), (0, 3)))
    assert sorted(row.bit_count() for row in path4.adj) == [1, 1, 2, 2]
    assert sorted(row.bit_count() for row in star.adj) == [1, 1, 1, 3]
    assert star.to_graph6() == "Cs"

    try:
        verify_pinned_labelg(fake)
    except ValueError as error:
        assert "executable hash" in str(error)
    else:
        raise AssertionError("counterfeit labelg passed the executable pin")


def probe_candidate_marker_and_limits(root: Path) -> None:
    root.mkdir(parents=True)
    database = root / "extensions.sqlite3"
    common = {
        "catalog_path": CATALOG,
        "parameters_path": PARAMETERS,
        "labelg_path": REAL_LABELG,
        "database_path": database,
        "checkpoint_path": root / "extensions.json",
        "candidate_directory": root / "candidates",
        "provenance_output": root / "provenance.csv",
        "unique_output": root / "unique.csv",
        "batch_size": 1,
        "active_host_ids": ("MMV-001",),
        "max_batches": 1,
        "wall_limit_seconds": 60.0,
        "memory_limit_mib": 1024.0,
    }
    first = run_extension_search(**common)
    assert first.summary["raw_processed"] == 1

    missing_candidate = root / "missing-candidate.json"
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            UPDATE metadata SET value = ?
            WHERE key = 'candidate_frozen_path'
            """,
            (str(missing_candidate),),
        )
        connection.commit()

    stopped = run_extension_search(**common)
    assert stopped.status == "candidate_review_pending", stopped
    assert stopped.candidate_path == str(missing_candidate)
    assert not missing_candidate.exists()
    assert stopped.summary["candidate_path"] == str(missing_candidate)
    candidate_state = stopped.summary["candidate_state"]
    assert candidate_state["pending"]
    assert "freeze marker exists without a candidate row" in (
        candidate_state["inconsistencies"]
    )
    assert "freeze marker path does not name an existing file" in (
        candidate_state["inconsistencies"]
    )

    for field in ("wall_limit_seconds", "memory_limit_mib"):
        arguments = {
            "catalog_path": CATALOG,
            "parameters_path": PARAMETERS,
            "labelg_path": REAL_LABELG,
            "batch_size": 1,
            "wall_limit_seconds": 60.0,
            "memory_limit_mib": 1024.0,
        }
        arguments[field] = float("nan")
        try:
            build_configuration(**arguments)
        except ValueError as error:
            assert "positive finite" in str(error)
        else:
            raise AssertionError(f"non-finite {field} was accepted")

    aliased = dict(common)
    aliased["checkpoint_path"] = database
    try:
        run_extension_search(**aliased)
    except ValueError as error:
        assert "path roles alias" in str(error)
    else:
        raise AssertionError("database/checkpoint path alias was accepted")


def probe_final_batch_crash_window(root: Path) -> None:
    """Crash after the final-batch commit and test completed-host recovery."""

    root.mkdir(parents=True)
    database = root / "extensions.sqlite3"
    common = {
        "catalog_path": CATALOG,
        "parameters_path": PARAMETERS,
        "labelg_path": REAL_LABELG,
        "database_path": database,
        "checkpoint_path": root / "extensions.json",
        "candidate_directory": root / "candidates",
        "provenance_output": root / "provenance.csv",
        "unique_output": root / "unique.csv",
        "batch_size": 1023,
        "active_host_ids": ("MMV-001",),
        "max_batches": 1,
        "wall_limit_seconds": 60.0,
        "memory_limit_mib": 1024.0,
    }
    original_canonicalize = engine.canonicalize_graph6_batch
    original_evaluate = engine.evaluate_canonical_extension
    original_stream_hash = engine._host_stream_hash
    engine.canonicalize_graph6_batch = lambda records, _path: tuple(records)
    engine.evaluate_canonical_extension = lambda _graph6: Evaluation(
        gamma=2,
        alpha=3,
        category="gamma_below_3",
        private_obstruction_json=None,
        eternal_a=None,
        eternal_b=None,
        family_a_size=None,
        family_b_size=None,
        family_a_sha256=None,
        family_b_sha256=None,
    )

    def injected_crash(
        _connection: sqlite3.Connection, _host_id: str
    ) -> str:
        raise RuntimeError("injected crash after final-batch commit")

    engine._host_stream_hash = injected_crash
    try:
        try:
            run_extension_search(**common)
        except RuntimeError as error:
            assert "injected crash" in str(error)
        else:
            raise AssertionError("injected crash was not reached")
    finally:
        engine.canonicalize_graph6_batch = original_canonicalize
        engine.evaluate_canonical_extension = original_evaluate
        engine._host_stream_hash = original_stream_hash

    with sqlite3.connect(database) as connection:
        status, next_mask, stream_hash = connection.execute(
            """
            SELECT status, next_mask, canonical_stream_sha256
            FROM hosts WHERE catalog_id = 'MMV-001'
            """
        ).fetchone()
        origin_count = connection.execute(
            """
            SELECT COUNT(*) FROM origins WHERE host_id = 'MMV-001'
            """
        ).fetchone()[0]
    assert (status, next_mask, origin_count) == ("running", 1, 0)
    assert stream_hash is None

    # Repeating the same batch from its authoritative next mask succeeds.
    engine.canonicalize_graph6_batch = lambda records, _path: tuple(records)
    engine.evaluate_canonical_extension = lambda _graph6: Evaluation(
        gamma=2,
        alpha=3,
        category="gamma_below_3",
        private_obstruction_json=None,
        eternal_a=None,
        eternal_b=None,
        family_a_size=None,
        family_b_size=None,
        family_a_sha256=None,
        family_b_sha256=None,
    )
    try:
        resumed = run_extension_search(**common)
    finally:
        engine.canonicalize_graph6_batch = original_canonicalize
        engine.evaluate_canonical_extension = original_evaluate
    assert resumed.status == "bounded_sample_complete"
    with sqlite3.connect(database) as connection:
        status, next_mask, stream_hash = connection.execute(
            """
            SELECT status, next_mask, canonical_stream_sha256 FROM hosts
            WHERE catalog_id = 'MMV-001'
            """
        ).fetchone()
    assert (status, next_mask) == ("complete", 1024)
    assert isinstance(stream_hash, str) and len(stream_hash) == 64


def main() -> None:
    if not REAL_LABELG.is_file():
        raise SystemExit("pinned campaign labelg is not built")
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        probe_counterfeit_labelg(root / "fake")
        probe_candidate_marker_and_limits(root / "state")
        probe_final_batch_crash_window(root / "crash")
    print("all bounded hostile probes reproduced")


if __name__ == "__main__":
    main()
