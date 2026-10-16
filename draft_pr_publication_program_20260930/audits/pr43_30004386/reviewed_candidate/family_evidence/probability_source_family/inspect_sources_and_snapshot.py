"""Read-only byte/source predicates. Never imports, compiles or executes candidate code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys
import urllib.request

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
RUN_LABEL = sys.argv[1] if len(sys.argv) > 1 else "source_inspection"
manifest = json.loads((AUDIT / "snapshot_manifest.json").read_text())
checks = []


def record(name, passed, **evidence):
    checks.append({"name": name, "passed": bool(passed), **evidence})


for row in manifest["files"]:
    data = (AUDIT / "source_snapshot" / row["path"]).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    record("snapshot_file_hash_and_size", digest == row["sha256"] and len(data) == row["size"],
           path=row["path"], actual_sha256=digest, actual_bytes=len(data))

patch = (AUDIT / "original_diff.patch").read_bytes()
record("original_diff_hash_and_size", hashlib.sha256(patch).hexdigest() == manifest["diff_sha256"]
       and len(patch) == manifest["diff_bytes"], bytes=len(patch), sha256=hashlib.sha256(patch).hexdigest())
blocks = re.split(r"(?=^diff --git )", patch.decode(), flags=re.M)[1:]
paths = [block.splitlines()[0].split(" b/", 1)[1] for block in blocks]
record("full_seventeen_path_identity", paths == manifest["changed_paths"], paths=paths)
prefix = "unsolved_math_prioritization/attempts/30004386/"
for block, path in zip(blocks, paths):
    if path.startswith(prefix):
        scientific_path = path[len(prefix):]
        added = [line[1:] for line in block.splitlines()
                 if line.startswith("+") and not line.startswith("+++")]
        reconstructed = ("\n".join(added) + "\n").encode() if added else b""
        expected = (AUDIT / "source_snapshot" / scientific_path).read_bytes()
        record("added_path_matches_snapshot", reconstructed == expected, path=scientific_path)

final_status = (AUDIT / "source_snapshot/SOURCE_STATUS.md").read_bytes()
stored_receipt = json.loads((AUDIT / "source_snapshot/check_results.json").read_text())
record("stored_receipt_is_historical_not_final_hash",
       stored_receipt["source_status_sha256"] != hashlib.sha256(final_status).hexdigest(),
       final_status_sha256=hashlib.sha256(final_status).hexdigest(),
       stored_receipt_source_sha256=stored_receipt["source_status_sha256"],
       interpretation="This difference is not proof of failed mathematics or fabricated execution.")
record("empty_turn_ledger", (AUDIT / "source_snapshot/turns.jsonl").stat().st_size == 0)
record("author_and_replay_code_are_identical",
       (AUDIT / "source_snapshot/check_normalization.py").read_bytes()
       == (AUDIT / "source_snapshot/review/author_replay/check_normalization.py").read_bytes())
record("author_and_replay_receipts_are_identical",
       (AUDIT / "source_snapshot/check_results.json").read_bytes()
       == (AUDIT / "source_snapshot/review/author_replay/check_results.json").read_bytes())

source = HERE / "foreign/jkp_arxiv_v2.pdf"
frozen_sources = json.loads((AUDIT / "source_snapshot/source_checksums.json").read_text())
jkp = next(row for row in frozen_sources if row["cache_filename"] == "jkp2022.pdf")
record("independently_downloaded_versioned_jkp_matches_candidate_hash",
       hashlib.sha256(source.read_bytes()).hexdigest() == jkp["sha256"]
       and source.stat().st_size == jkp["bytes"], actual_sha256=hashlib.sha256(source.read_bytes()).hexdigest())

url = "https://publications.mfo.de/bitstream/handle/mfo/3713/OWR_2020_06.pdf?isAllowed=y&sequence=4"
access = {"url": url, "pid": os.getpid(), "started_utc": datetime.now(timezone.utc).isoformat(),
          "role": "foreign primary report download, read-only inspection, not authored science"}
try:
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
        data = response.read()
        access.update(final_url=response.url, status=response.status, headers=dict(response.headers))
    (HERE / "foreign/owr_mfo_candidate_url.pdf").write_bytes(data)
    access.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    owr = next(row for row in frozen_sources if row["cache_filename"] == "original.pdf")
    record("independent_mfo_download_matches_candidate_hash", access["sha256"] == owr["sha256"]
           and len(data) == owr["bytes"], actual_sha256=access["sha256"], actual_bytes=len(data))
except Exception as error:
    access["error"] = repr(error)
    record("independent_mfo_download_access", False, error=repr(error))
access["ended_utc"] = datetime.now(timezone.utc).isoformat()
(HERE / "captures" / (RUN_LABEL + "_mfo_candidate_source_access.json")).write_text(json.dumps(access, indent=2) + "\n")

pdf_text = (HERE / "foreign/jkp_arxiv_v2.extracted.txt").read_text()
record("versioned_source_contains_theorem_A_and_weak_topology",
       "Theorem A." in pdf_text and "weak topology" in pdf_text and "good rate function" in pdf_text)
record("versioned_source_contains_homeomorphism_and_sphere_LDP",
       "Proposition 3.1." in pdf_text and "homeomorphism" in pdf_text and "Proposition 3.4." in pdf_text)
record("publisher_online_date_literal",
       "17 December 2021" in (HERE / "foreign/jkp_publisher_english.html").read_text())
record("owr_publisher_actual_publication_date_literal",
       "10 February 2021" in (HERE / "foreign/owr_publisher_landing.html").read_text(),
       interpretation="Rendered publisher date. Its machine metadata says 2021/02/09 and UTC timestamp 2021-02-09T23:45:03.000Z; preserve this one-day display/metadata distinction.")

result = {"schema": "probability-source-family-readonly-source-predicates/v1",
          "utc": datetime.now(timezone.utc).isoformat(), "pid": os.getpid(),
          "original_head": manifest["head"], "candidate_helpers_imported_compiled_or_executed": False,
          "all_finite_source_predicates_passed": all(row["passed"] for row in checks),
          "checks": checks,
          "scope": "Byte identities, exact source access and finite textual predicates only. No inference of old execution, mathematical truth, novel discovery or future publication approval."}
print(json.dumps(result, indent=2))
