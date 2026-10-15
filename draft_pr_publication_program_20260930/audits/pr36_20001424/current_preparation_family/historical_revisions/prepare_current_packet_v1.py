#!/usr/bin/env python3
"""Administrative PR36 freeze. Review this source; only root may execute it.

No mathematical search or verifier replay occurs here. All proof material is
copied byte-for-byte from already frozen inputs. Execution requires explicit
hash pins for the finalized root closure receipt and priority decision. No
queue, state, history, inventory, remote, canonical-attempt or tracker write is
implemented. A failed build directory is retained, never replaced or deleted.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import traceback

HEAD = "35be7fe58a2832c4d7012cf69c973810fb4c42f8"
BASE = "01358d66fc67d1c462bddf31c0d4ee5b120e6737"
ID = 20001424
CODE = "AIM-DYNAMICAL_SYSTEMS-0082"
PR_URL = "https://github.com/AlecKriebel/Math/pull/36"
PAIR_HASH = "772b051437b7dbf9ab9eddf38e10981f681b99ac4d83f44fbc886600c5c06270"
STATEMENT_HASH = "66ebcc5661f95cab8df379cd71155d75a571bcf1fdd05acbfe1294c92e2d3f03"
FAMILIES = {
    "graph_family": ("authored_manifest.json", "3b14dc707a10811165c418fb0faacedfbf7082598cb1e5eb663a24e506d5a1cd", 190),
    "algebraic_family": ("authored_manifest.json", "df1065f83fa64f9ee685638b9b115baefe3e9d9fa7c06a2cb1f02b1f63f58176", 50),
    "primary_scope_family": ("AUTHORED_MANIFEST.json", "75cd9b1704194a2adbd451cf0af4c8f24c9bf0fbf9cb6f9139be3369a90a6fb2", 27),
    "antipodal_priority_family": ("AUTHORED_MANIFEST.json", "4a7bb26fe5d32af8df445264a4f54e0bb65c6f13a5c176c6c88b577b6e063d75", 79),
    "arithmetic_graph_priority_family": ("AUTHORED_MANIFEST.json", "f66e249bc5a60d619fedf3390b826f4e19640b5da5a7c1d4385f0180805c88bb", 18),
}
FORBIDDEN_PARTS = {"tmp", "private_tmp", "private_sources", "foreign_downloads", "foreign_sources", "__pycache__"}
EXACT_IMPORTS = {
    "ROOT_UNIVERSAL_CERTIFICATE.md": "CURRENT_UNIVERSAL_CERTIFICATE.md",
    "ROOT_PRIORITY_DECISION.md": "CURRENT_PRIORITY_DECISION.md",
    "algebraic_family/independent_universal_proof.md": "CURRENT_GRAPH_ALGEBRAIC_PROOF.md",
    "graph_family/proof_assessment_seal.md": "CURRENT_GRAPH_DYNAMICS_PROOF.md",
    "primary_scope_family/INDEPENDENT_MATH_SCOPE_SEALED.md": "CURRENT_ORIGINAL_SCOPE_PROOF.md",
    "antipodal_priority_family/PRIOR_APPLICATION.md": "CURRENT_PRIOR_APPLICATION.md",
    "arithmetic_graph_priority_family/INDEPENDENT_SILVERMAN_SOURCE_CONSEQUENCE.md": "CURRENT_INDEPENDENT_PRIOR_SOURCE_CONSEQUENCE.md",
    "antipodal_priority_family/PRIMARY_READING_LEDGER.json": "primary_evidence/ANTIPODAL_PRIMARY_READING_LEDGER.json",
    "antipodal_priority_family/RETRIEVAL_SILVERMAN.json": "primary_evidence/SILVERMAN_RETRIEVAL.json",
    "arithmetic_graph_priority_family/SOURCE_READING_LEDGER.json": "primary_evidence/ARITHMETIC_SOURCE_READING_LEDGER.json",
    "arithmetic_graph_priority_family/PRIMARY_DATE_RECEIPTS.json": "primary_evidence/ARITHMETIC_PRIMARY_DATE_RECEIPTS.json",
    "primary_scope_family/SOURCE_READING_LEDGER.json": "primary_evidence/ORIGINAL_SCOPE_SOURCE_READING_LEDGER.json",
    "primary_scope_family/primary_http_receipts.json": "primary_evidence/LITERAL_AIM_HTTP_RECEIPTS.json",
    "ROOT_PRIMARY_RETRIEVAL.json": "primary_evidence/ROOT_PRIMARY_RETRIEVAL.json",
    "ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json": "root_verification/ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json",
    "ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json": "root_verification/ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json",
}
ROOT_SUPPORT = [
    "snapshot_original.py", "reproduce_root_original.py", "retrieve_root_sources.py",
    "ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json", "ROOT_PRIMARY_RETRIEVAL.json",
    "ROOT_UNIVERSAL_CERTIFICATE.md", "ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json",
    "ROOT_PRIORITY_DECISION.md", "snapshot_manifest.json", "pinned_problem.json",
    "pinned_prior_report.json", "pr_input/metadata.json", "pr_input/diff.patch",
]
HISTORICAL_TOP = [
    "CANDIDATE.md", "graph.svg", "verify_graph.py", "graph_verification.json",
    "source_record.json", "source_manifest.json", "turns.jsonl",
    "review/REVIEW.md", "review/independent_checks.py", "review/independent_results.json",
    "review/review_summary.json",
]
QUEUE_HEADER = ["Rank", "ID / code", "Problem", "EV", "Impact (/10)", "Difficulty", "Proposed", "Status", "Turns", "Chat", "Findings", "DOI"]


def require(condition: bool, message: str) -> None:
    # Ordinary exceptions, rather than assert, preserve checks under python -O.
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path):
    return json.loads(path.read_bytes())


def json_bytes(value) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    require(bool(value) and not path.is_absolute() and ".." not in path.parts, f"Unsafe member path: {value}")
    require(not (set(path.parts) & FORBIDDEN_PARTS), f"Excluded foreign/cache/scratch member: {value}")
    require(path.suffix not in {".pyc", ".tmp"}, f"Excluded temporary member: {value}")
    return path


def closed_members(manifest):
    entries = manifest["files"]
    if isinstance(entries, dict):
        return [{"path": name, **entry} for name, entry in entries.items()]
    require(isinstance(entries, list), "Unsupported authored manifest member schema")
    return entries


def git_bytes(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=repo)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Root-only explicit freeze instruction")
    parser.add_argument("--root-receipt-sha256", required=True)
    parser.add_argument("--root-priority-decision-sha256", required=True)
    parser.add_argument("--root-replay-script", required=True, help="Explicit repository-audit-relative root family replay script")
    parser.add_argument("--root-replay-script-sha256", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    require(args.execute, "Prepared for review only; root must explicitly supply --execute")
    script = Path(__file__).resolve()
    ancestors = [script.parent, *script.parents]
    matches = [p for p in ancestors if p.name == "pr36_20001424"]
    require(len(matches) == 1, "Builder must remain inside the dedicated PR36 audit folder")
    audit = matches[0]
    repo = audit.parents[2]
    source = audit / "source_snapshot"
    destination = audit / "reviewed_candidate"
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    require(git_bytes(repo, "branch", "--show-current").strip() == b"main", "Stay on main")
    require(not destination.exists(), "Never overwrite a frozen current candidate; preserve revisions separately")
    root_receipt_path = audit / "ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json"
    root_decision_path = audit / "ROOT_PRIORITY_DECISION.md"
    require(sha(root_receipt_path.read_bytes()) == args.root_receipt_sha256, "Root closure receipt changed after explicit review")
    require(sha(root_decision_path.read_bytes()) == args.root_priority_decision_sha256, "Root priority decision changed after explicit review")
    root_receipt = load(root_receipt_path)
    require(root_receipt.get("status") == "PASS", "Root closure must be finalized PASS")
    require(root_receipt.get("closed_family_count") == 5, "Root must close all five families")
    require(root_receipt.get("authored_members_verified_before_and_after") == 364, "Root must verify all 364 closed first-party members before and after replay")
    require(root_receipt.get("new_substantive_attempts") == 0, "No new substantive attempts")
    decision = root_decision_path.read_text()
    require("PRIOR_APPLICATION" in decision and "already_solved" in decision, "Finalized root disposition must explicitly credit the prior application")
    root_script_rel = str(safe_relative(args.root_replay_script))
    root_script_path = audit / root_script_rel
    require(root_script_path.suffix == ".py", "Explicit actual root replay script must be Python source")
    require(sha(root_script_path.read_bytes()) == args.root_replay_script_sha256, "Root family replay script changed after explicit review")

    # Freeze the entire preflight input plan in memory before any output write.
    dependencies = {}
    def bind(path: Path, role: str) -> bytes:
        require(path.is_file() and not path.is_symlink(), f"Missing/nonregular/symlink input: {path}")
        rel = str(path.relative_to(audit))
        safe_relative(rel)
        data = path.read_bytes()
        existing = dependencies.get(rel)
        record = {"path": rel, "bytes": len(data), "sha256": sha(data), "role": role}
        if existing is not None:
            require(existing["sha256"] == record["sha256"] and existing["bytes"] == record["bytes"], f"Input changed during preflight: {rel}")
        else:
            dependencies[rel] = record
        return data

    sm = load(audit / "snapshot_manifest.json")
    require(sm["head"] == HEAD and sm["base"] == BASE and len(sm["files"]) == 16, "Wrong original16 scope")
    require(sm["pr"] == 36 and str(sm["problem"]) == str(ID), "Wrong snapshot target")
    original = {}
    for member in sm["files"]:
        rel = str(safe_relative(member["path"]))
        require(rel not in original, f"Duplicate original member: {rel}")
        data = bind(source / rel, "original16_exact_git_input")
        require(len(data) == member["size"] and sha(data) == member["sha256"], f"Snapshot binding failed: {rel}")
        git_path = f"unsolved_math_prioritization/attempts/{ID}/{rel}"
        require(data == git_bytes(repo, "show", f"{HEAD}:{git_path}"), f"Actual original head Git bytes differ: {rel}")
        require(git_bytes(repo, "rev-parse", f"{HEAD}:{git_path}").decode().strip() == member["git_blob"], f"Original Git blob differs: {rel}")
        original[rel] = data
    actual_diff = git_bytes(repo, "diff", "--binary", BASE, HEAD)
    require(actual_diff == (audit / "pr_input/diff.patch").read_bytes(), "Complete original diff changed")
    require(len(actual_diff) == sm["diff_bytes"] and sha(actual_diff) == sm["diff_sha256"], "Original diff hash/size differs")
    changed = git_bytes(repo, "diff", "--name-only", BASE, HEAD).decode().splitlines()
    require(changed == sm["changed_paths"] and len(changed) == 17, "Wrong original17 changed paths")
    metadata = load(audit / "pr_input/metadata.json")
    require(metadata["number"] == 36 and metadata["headRefOid"] == HEAD, "Wrong frozen original PR metadata")
    record = json.loads(original["source_record.json"])
    problem = load(audit / "pinned_problem.json")
    prior = load(audit / "pinned_prior_report.json")
    require(record["problem"] == problem and record["upstream_prior_report"] == prior, "Entire nested original problem/prior must remain unchanged")
    require(sha(json.dumps([problem, prior], sort_keys=True).encode()) == PAIR_HASH, "Native selected source-pair hash differs")
    require(sha(problem["statement"].encode()) == STATEMENT_HASH, "Literal statement hash differs")
    turns = [json.loads(line) for line in original["turns.jsonl"].splitlines() if line]
    require(len(turns) == 1 and turns[0]["turn"] == 1, "Preserve exact original one-turn ledger")
    historical_status = json.loads(original["status.json"])
    historical_readiness = json.loads(original["readiness.json"])
    require(historical_status["turns_used"] == 1 and historical_status["turn_limit"] == 5, "Original budget must remain 1/5")
    family_counts = {}
    for family, (manifest_name, expected_sha, count) in FAMILIES.items():
        manifest_path = audit / family / manifest_name
        raw = bind(manifest_path, "closed_first_party_self_excluding_manifest")
        require(sha(raw) == expected_sha, f"Closed manifest changed: {family}")
        entries = closed_members(json.loads(raw))
        require(len(entries) == count, f"Wrong closed authored member count: {family}")
        seen = set()
        for member in entries:
            rel = str(safe_relative(member["path"]))
            require(rel not in seen and rel != manifest_name, f"Duplicate/self-included family member: {family}/{rel}")
            seen.add(rel)
            raw = bind(audit / family / rel, "closed_first_party_authored_member")
            require(len(raw) == member.get("bytes", member.get("size")) and sha(raw) == member["sha256"], f"Closed authored binding failed: {family}/{rel}")
        family_counts[family] = len(entries)
    require(sum(family_counts.values()) == 364, "All five closed authored families required")
    for rel in ROOT_SUPPORT + [root_script_rel]:
        bind(audit / rel, "explicit_root_git_source_metadata_or_actual_replay")
    bind(script, "actual_executed_administrative_builder")
    frozen_imports = {target: bind(audit / origin, "exact_existing_frozen_proof_or_primary_receipt") for origin, target in EXACT_IMPORTS.items()}

    queue_path = repo / "unsolved_math_prioritization/QUEUE.md"
    queue_bytes = queue_path.read_bytes()
    queue_lines = queue_bytes.decode().splitlines(keepends=True)
    headers = [x.strip() for x in next(line for line in queue_lines if line.startswith("| Rank |")).split("|")[1:-1]]
    require(headers == QUEUE_HEADER and len(headers) == 12, "Require the exact twelve-column queue")
    queue_rows = [line for line in queue_lines if len(line.split("|")) == 14 and line.split("|")[2].strip() == f"{ID} / {CODE}"]
    require(len(queue_rows) == 1, "Require one exact numeric/code target row")
    before = queue_rows[0]
    fields = before.split("|")
    require(fields[8].strip() == "queued" and fields[9].strip() == "0/5", "Selected queue row changed; preserve and review a new named-row rebase")
    findings = (
        "2026-10-02: Credited prior application: Silverman1995 printed cubic i((z-1)/(z+1))^3 is exactly PCF, "
        "absolute field of moduli Q, no real/Q model; universal negative answer already follows from that source. "
        "Original degree11 critically fixed graph verified and preserved; its narrower priority unestablished. "
        "Proposed already_solved after NEW whole source-first gate; original1/5, new0/audit0; no paper/newDOI/tracker. "
        f"PR: {PR_URL}."
    )
    after_fields = list(fields)
    after_fields[8], after_fields[9], after_fields[11] = " already_solved ", " 1/5 ", f" {findings} "
    after = "|".join(after_fields)
    require(all(fields[i] == after_fields[i] for i in range(14) if i not in {8, 9, 11}), "Only selected Status/Turns/Findings may change")
    require(queue_bytes.count(before.encode()) == 1, "Target row replacement must be unique")
    prospective_queue = queue_bytes.replace(before.encode(), after.encode(), 1)
    require(prospective_queue.splitlines(keepends=True) == [after.encode() if line == before.encode() else line for line in queue_bytes.splitlines(keepends=True)], "Preserve every unrelated queue byte")

    outputs = {f"original_archive/{rel}": data for rel, data in original.items()}
    outputs.update({rel: original[rel] for rel in HISTORICAL_TOP})
    outputs.update(frozen_imports)
    outputs["problem.json"] = (audit / "pinned_problem.json").read_bytes()
    outputs["prior_report.json"] = (audit / "pinned_prior_report.json").read_bytes()
    outputs["build/prepare_current_packet.py"] = script.read_bytes()
    historical_notice = """# Historical original16 archive

Every member in this directory is an exact frozen original Git artifact from
PR36 head 35be7fe58a2832c4d7012cf69c973810fb4c42f8, base
01358d66fc67d1c462bddf31c0d4ee5b120e6737. The archive contains exactly sixteen
files, so this explanatory notice is kept outside it. The original candidate,
graph diagram/program/results, nested source record, reference manifest, turn
ledger and candidate-era review also remain exact at the top level.

Original PASS/status/model xhigh/deadline/branch fields describe only the dated
original packet. They are not current approval, current model exposure, a new
deadline, or native queue state evidence. Current administration supersedes the
historical resolution framing by crediting Silverman's earlier printed map.
"""
    outputs["HISTORICAL_ORIGINAL_NOTICE.md"] = historical_notice.encode()
    summary = """# PR36: credited prior application of Silverman's printed cubic

The full question, “Are all PCF maps defined over their field of moduli?”, has
a negative answer by an exact elementary consequence of Silverman's printed
1995 cubic i((z−1)/(z+1))^3. Its critical points lie on the exact six-cycle
1 → 0 → −i → −1 → ∞ → i → 1. The imported complete proofs verify PCF,
algebraicity, trivial holomorphic automorphisms, absolute field of moduli Q,
and absence of a real model, hence absence of a Q-model.

Proposed queue disposition: already_solved, credited PRIOR_APPLICATION.
Silverman explicitly printed the formula and descent assertions; the PCF
portrait is an elementary source consequence independently checked in this
audit. No claim of earliest worldwide PCF recognition or novel universal
resolution is made. The distinct original degree-11 critically fixed graph
construction remains exact and mathematically supported; priority for that
narrower construction remains unestablished.

Original substantive budget 1/5; new substantive research 0; audit attempts 0.
No paper, new DOI, tracker row or release is part of this disposition. Five
closed first-party families and the finalized actual root reproduction are
bound. A NEW whole-current-packet source-first adversarial gate is PENDING.
Original and family verdicts do not transfer to that gate. Extensive AI
verification is unrefereed; no external human review or formal proof-assistant
certification is claimed.
"""
    outputs["README.md"] = (summary + """
The current prior proof is CURRENT_PRIOR_APPLICATION.md and its separately
sealed arithmetic reconstruction is CURRENT_INDEPENDENT_PRIOR_SOURCE_CONSEQUENCE.md.
CURRENT_PRIORITY_DECISION.md is the exact finalized root decision. The three
imported graph proofs and CURRENT_UNIVERSAL_CERTIFICATE.md retain their earlier
scope and dated interim-priority statements; the finalized current decision
records the completed priority outcome. CANDIDATE.md and review/ are historical
original inputs, not a new whole-packet review. HISTORICAL_ORIGINAL_NOTICE.md
identifies every historical field explicitly.

CURRENT_PROOF_DEPENDENCIES.json uses the repository audit anchor
draft_pr_publication_program_20260930/audits/pr36_20001424. Resolve every listed
path from that anchor, even after this packet is copied to the canonical
attempt folder. Source files under ignored foreign/scratch folders are not
redistributed; primary URLs, versions, page locators, hashes and reading scope
are in primary_evidence/ and the original audit ledgers. Reproduction scripts
that rely on repository context run from the original anchored audit folders;
these administrative copies do not relocate their dependency base.

The original graph checks use standard-library Python without optimization.
Run unchanged copies privately if fresh diagnostics are needed; their output
is finite graph evidence and cannot certify source/prose/descent or priority.
This builder performs no new mathematical replay or research search: the root
receipt binds the actual completed runs. CURRENT_QUEUE_PATCH.json is a dated
prospective named-row patch only. A later integration must independently
guard its live preimage and preserve intervening unrelated acceptances.
""").encode()
    outputs["pr_body.md"] = (summary + f"\nResearch and evidence anchor: draft_pr_publication_program_20260930/audits/pr36_20001424. Original PR: {PR_URL}.\n").encode()
    source_qualification = """# Current source and scope qualification

The exact nested source_record.problem and complete upstream_prior_report are
unchanged historical imports. Their full universal text has no odd-divisor or
rigidity condition. That condition is prior partial progress. Successful live
official AIM HTTP recovery (33,521 bytes, SHA256
990076ea9a8b9a23c9a6a34e6686eda087be82cd616c02d743e996a9c1e7d178)
supersedes the earlier source-access limitation as current evidence; failed
retrievals are preserved in their original receipts, not relabelled success.

The decisive priority source is Silverman, Compositio Mathematica 98 (1995),
269–304, printed p.271 equation (1), physical PDF p.4, and printed p.296
odd-exponent family, physical PDF p.29; the no-real-model discussion continues
on pp.296–297. Official primary PDF SHA256
0a405ab1fbe4fc04e73439ecc31db4afaae3d8e38ce58bfd49f65442c6e88116,
3,149,856 bytes. Formula glyphs were visually checked because extraction can
omit them. Silverman printed the algebraic map, exact moduli field Q and
descent obstruction. The source does not label this family PCF; that adjective
is established by the exact orbit derivation in the imported authored proofs.

The original degree-11 proof uses Hlushchanka arXiv:1904.04759v2 (October 2025),
its orientation-preserving graph convention and operative inverse construction,
not arbitrary bijection equivariance. Earlier graph frameworks are credited.
Hidalgo–Quispe arXiv:1502.05306v4 (July 2021) corroborates reflection and
Silverman-family attribution; v4-specific content is not backdated to v1.
The withdrawn arXiv:2405.03612 characterization is not established input.
BBM numerical center labels and generic pseudo-real families do not alone
certify PCF/FOM obstruction and are unnecessary to the decisive old cubic.

Bounded literature inspection does not prove earliest recognition worldwide
or novelty of the exact degree-11 graph. No new discovery credit follows.
All substantive mathematics is imported byte-exact from the frozen proofs;
this administrative certificate introduces no proof search, repair, or new
claim family. Source ledgers preserve version differences, imports, access
failures, independence/exposure limitations, and actual corrected control
failures. Hash changes alone detect altered bytes, not false mathematics.
"""
    outputs["SOURCES.md"] = (source_qualification + """
Primary references: https://www.numdam.org/item/CM_1995__98_3_269_0/;
http://aimpl.org/finitedynamics/2/;
https://arxiv.org/pdf/1904.04759v2;
https://arxiv.org/pdf/1502.05306v4.
The exact original SOURCES.md is preserved in original_archive/. Current
primary page/version evidence is copied without changing its authorship.
""").encode()
    outputs["CURRENT_SOURCE_SCOPE_CERTIFICATE.md"] = source_qualification.encode()
    current_gate = "pending_NEW_whole_current_packet_source_first_adversary"
    budget = {
        "original_substantive_attempts": 1, "used_substantive_attempts": 1,
        "maximum_substantive_attempts": 5, "cumulative_attempts": "1/5",
        "new_substantive_attempts": 0, "verification_attempts": 0,
        "current_deadline_utc": None,
        "current_model": "Not independently exposed in this runtime",
        "current_reasoning_effort": "Not independently exposed in this runtime",
        "historical_original_model": historical_readiness["model"],
        "historical_original_reasoning": historical_readiness["reasoning"],
        "historical_original_started_utc": historical_readiness["started_utc"],
        "historical_original_deadline_utc": historical_readiness["deadline_utc"],
        "historical_original_branch": historical_readiness["branch"],
        "historical_scope": "These dated original fields are archival only; no retroactive model/effort upgrade or new deadline is inferred.",
    }
    outputs["readiness.json"] = json_bytes({
        "utc": now, "id": ID, "code": CODE, "status": current_gate,
        "queue_outcome_requested": "already_solved", "priority_classification": "PRIOR_APPLICATION",
        "review_hash": PAIR_HASH, "statement_hash": STATEMENT_HASH,
        "exact_target": problem["statement"], "source_record_sha256": sha(original["source_record.json"]),
        "original_candidate_sha256": sha(original["CANDIDATE.md"]),
        "current_prior_application_sha256": sha(outputs["CURRENT_PRIOR_APPLICATION.md"]),
        "budget": budget, "native_queue_lifecycle_claimed": False,
        "historical_custom_readiness": historical_readiness,
        "independent_review": "Five closed first-party families and finalized root actual reproduction; NEW entire current source-first gate pending, with no verdict transferred.",
        "positive_novelty_claim": False, "paper_or_new_doi_or_tracker": False,
        "current_workflow_completion_estimate_percent": 75,
        "universal_negative_answer_verification_percent": 100,
        "narrow_degree11_priority_verified": False,
    })
    outputs["status.json"] = json_bytes({
        "utc": now, "id": ID, "code": CODE, "pr": 36,
        "status": "already_solved_proposed_pending_NEW_whole_gate",
        "queue_status_proposed": "already_solved", "priority_classification": "PRIOR_APPLICATION",
        "current_gate": current_gate, "original_head": HEAD, "actual_original_base": BASE,
        "budget": budget, "original_turns_sha256": sha(original["turns.jsonl"]),
        "historical_original_status": historical_status,
        "original_graph_mathematically_supported": True,
        "universal_target_negative_by_prior_source_application": True,
        "exact_prior_absolute_field_of_moduli": "Q", "exact_prior_degree": 3,
        "earliest_worldwide_recognition_claim": False, "new_discovery_claim": False,
        "original_degree11_exact_coefficients_computed": False,
        "original_degree11_exact_field_of_moduli_computed": False,
        "paper_or_new_doi_or_tracker": False,
        "current_workflow_completion_estimate_percent": 75,
    })
    outputs["CURRENT_QUEUE_PATCH.json"] = json_bytes({
        "utc": now, "phase": "Prospective exact named-row review snapshot; no live queue write",
        "id": ID, "header_names": headers, "column_count": 12,
        "whole_queue_preimage_sha256": sha(queue_bytes), "whole_queue_prospective_sha256": sha(prospective_queue),
        "row_before": before, "row_prospective": after,
        "allowed_named_changes": ["Status", "Turns", "Findings"],
        "allowed_split_field_indices": [8, 9, 11],
        "all_unrelated_bytes_and_Chat_DOI_preserved": True,
        "current_gate": current_gate,
        "integration_guard": "Check live whole-queue preimage; if intervening unrelated acceptance changed it, perform a separately receipted exact named-row rebase preserving every other byte. Do not replay the historical PR diff.",
    })
    outputs["CURRENT_AUDIT_SCOPE.md"] = ("""# NEW whole-current-packet gate: pending

The prospective reviewer must begin with the full pinned literal source and
complete prior report, seal its scope, and independently check every current
scientific/source/credit/metadata/body/status/log/ledger/queue field and the
complete exact dependency bindings. Challenge hidden assumptions, degree and
critical support, the exact six-cycle, exhaustive centralizer logic, Galois
moduli field Q, real-model/reflection obstruction, source formula/page/version
evidence, prior-credit scope, original graph preservation, turn accounting,
historical model/effort/deadline scope, queue column preservation, and copying
dependencies into canonical packets. Five family findings and historical
original review are limited input evidence, never a transferred clean verdict.

No acceptance or shared write is performed here. No new substantive math is
searched. Every original failure/correction and early independence limitation
remains in its frozen family evidence. Exact mathematical claims are the
imported closed proofs, with the current administrative credit distinction
given by the finalized root decision. Current workflow estimate 75%; current
whole gate remains open. No paper, new DOI, tracker or release is requested.
""").encode()
    outputs["RESEARCH_LOG.md"] = (f"# Current PR36 research/audit log\n\n{now} — checkpoint: current workflow 75%; universal negative-answer verification 100%, exact-degree11 novelty unestablished. Five closed families (364 first-party members) and finalized root actual reproduction are bound. Original16 exact Git inputs preserved, original graph science/source/turns unchanged. Proposed already_solved credited PRIOR_APPLICATION from Silverman1995 exact cubic, with complete independently sealed PCF/FOMQ/no-real-model proofs imported byte-exact. Original1/5, new0/audit0. NEW whole source-first gate pending; no paper/newDOI/tracker. Original dated model xhigh/deadline/branch metadata historical only; current model/effort unexposed, current deadline null. Foreign source bytes excluded; no outside individual contacted.\n").encode()
    outputs["CURRENT_PROOF_DEPENDENCIES.json"] = json_bytes({
        "utc": now, "dependency_anchor_repository_relative": str(audit.relative_to(repo)),
        "resolution_rule": "Resolve each path against repository_root/dependency_anchor_repository_relative, not the current packet's parent. This exact audit anchor also applies to copies in canonical attempts.",
        "scope": "All five CLOSED first-party manifests and 364 authored members, exact original16 Git inputs, full17path diff and frozen inputmetadata, explicit root source/universal/actual-reproduction receipts and actual root/builder code; no foreign sources or scratch trees.",
        "closed_family_count": 5, "closed_authored_member_count": 364,
        "family_member_counts": family_counts, "files": sorted(dependencies.values(), key=lambda x: x["path"]),
    })
    outputs["CURRENT_BUILD_RECEIPT.json"] = json_bytes({
        "utc": now, "kind": "Administrative exact-input freeze; not a new mathematical replay or current approval",
        "original16_git_bytes_verified": True, "original17_diff_verified": True,
        "original_archive_member_count": 16, "original_graph_source_and_turns_byte_exact": True,
        "root_receipt_sha256": args.root_receipt_sha256,
        "root_priority_decision_sha256": args.root_priority_decision_sha256,
        "actual_builder_audit_relative": str(script.relative_to(audit)), "actual_builder_sha256": sha(script.read_bytes()),
        "actual_root_family_replay_script": root_script_rel, "actual_root_family_replay_script_sha256": args.root_replay_script_sha256,
        "closed_family_count": 5, "closed_authored_members_bound": 364,
        "new_substantive_attempts": 0, "verification_attempts": 0,
        "current_gate": current_gate, "live_queue_state_history_inventory_remote_canonical_writes": 0,
    })
    # No unbound late reads: all dependencies must still match the preflight.
    for member in dependencies.values():
        raw = (audit / member["path"]).read_bytes()
        require(len(raw) == member["bytes"] and sha(raw) == member["sha256"], f"Input changed before freeze: {member['path']}")
    require(queue_path.read_bytes() == queue_bytes, "Live queue changed during preparation; restart with new reviewed snapshot")
    stage = audit / f"reviewed_candidate.preparation_{stamp}"
    require(not stage.exists(), "Unique staging directory collision")
    stage.mkdir()
    try:
        for rel, raw in sorted(outputs.items()):
            path = stage / str(safe_relative(rel))
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as handle:
                handle.write(raw)
        for rel, raw in original.items():
            require((stage / "original_archive" / rel).read_bytes() == raw, f"Archive changed: {rel}")
        for rel in HISTORICAL_TOP:
            require((stage / rel).read_bytes() == original[rel], f"Historical top-level input changed: {rel}")
        members = [{"path": str(path.relative_to(stage)), "bytes": path.stat().st_size, "sha256": sha(path.read_bytes())} for path in sorted(stage.rglob("*")) if path.is_file()]
        manifest = {
            "utc": now, "schema": "strict_self_excluding_current_packet_v1",
            "self_excluded": ["MANIFEST.json"], "files_count": len(members), "files": members,
            "scope": "Exact original16 archive and current credited prior application administration; NEW whole source-first adversary gate pending",
            "queue_outcome_proposed": "already_solved", "priority_classification": "PRIOR_APPLICATION",
        }
        with (stage / "MANIFEST.json").open("xb") as handle:
            handle.write(json_bytes(manifest))
        actual = {str(path.relative_to(stage)) for path in stage.rglob("*") if path.is_file()}
        require(actual == {entry["path"] for entry in members} | {"MANIFEST.json"}, "Strict self-excluding current inventory differs")
        for member in members:
            raw = (stage / member["path"]).read_bytes()
            require(len(raw) == member["bytes"] and sha(raw) == member["sha256"], f"Current packet binding failed: {member['path']}")
        require(not destination.exists(), "Current destination appeared; retain this stage and review separately")
        os.rename(stage, destination)
    except BaseException:
        failure = {"utc": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "FAILED_BUILD_PRESERVED", "stage": str(stage), "traceback": traceback.format_exc(), "new_substantive_attempts": 0}
        # Keep original failure evidence and all partial files; never overwrite.
        with (stage / "BUILD_FAILURE.json").open("xb") as handle:
            handle.write(json_bytes(failure))
        raise
    print(json.dumps({"status": "CURRENT_PACKET_FROZEN_NEW_WHOLE_GATE_PENDING", "destination": str(destination), "members": len(members), "dependencies": len(dependencies), "manifest_sha256": sha((destination / "MANIFEST.json").read_bytes()), "proposed_queue_status": "already_solved", "priority": "PRIOR_APPLICATION", "attempts": "1/5", "new_substantive_attempts": 0, "verification_attempts": 0, "shared_writes": 0}, indent=2))


if __name__ == "__main__":
    main()
