"""Seal source-scope decision independently of subsequent priority research."""
from pathlib import Path
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT.parent.parent / "original/unsolved_math_prioritization/attempts/2306072"
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

initial = json.loads((ROOT / "SOURCE_RETRIEVAL.json").read_text())
content = json.loads((ROOT / "SOURCE_CONTENT_CHECK.json").read_text())
supplements = content["supplementary_retrievals"]
manifest = {
    "sealed_at_utc": now,
    "phase": "source_scope_only",
    "source_records": initial + supplements,
    "full_read_coverage": {"hayman_lingham_v2": "printed143/PDF144 visually; bibliography116 text",
                           "duren_1981_eth": "all14 article pages352-365 text and visual",
                           "pfluger_1971": "sections4.1-4.5 pp21-29 text and visual; earlier setup selected text"},
    "frozen_input_sha256": {name: sha(FROZEN / name) for name in ("PROOF.md", "SOURCE_GATE.md", "SOURCE_MANIFEST.json")},
    "old_duren_binary_match": False,
    "old_duren_article_payload_equivalence": "untested: older binary absent",
    "fresh_duren_article_payload_retrieval_repeat_matches": content["duren_fresh_article_payloads_equal"],
}
(ROOT / "SOURCE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
verdict = {
    "sealed_at_utc": now, "phase": "source_scope_only", "verdict": "PASS_SOURCE_SCOPE",
    "completion_percent": 100,
    "premises_passed": ["exact_problem_target", "normalized_S", "continuous_complex_linear_functional",
                        "real_nonconstancy", "single_analytic_slit", "finite_tip_increasing_modulus",
                        "Duren_positive_differential_sign", "Pfluger_negative_sign_reconciled",
                        "interior_radial_angle_convention", "candidate_L_f_squared_nonzero",
                        "simple_pole", "unique_incoming_trajectory", "actual_slit_continuation",
                        "continuous_argument_lift", "signed_and_unsigned_angle_translation"],
    "blocking_source_scope_gaps": [],
    "provenance_limits": ["Duren restates classical geometry; supplementary original Pfluger proof inspected",
                          "no formal reconstruction of every classical variation foundation",
                          "author old Duren binary not present for content-payload equality test"],
    "full_candidate_quantitative_proof_certified_by_this_phase": False,
    "priority_verdict": "NOT_ASSESSED_IN_THIS_PHASE", "novelty_verdict": "NOT_ASSESSED_IN_THIS_PHASE",
    "report": "REPORT.md", "exact_bridge_check": "SOURCE_BRIDGE_CHECKS.json",
}
(ROOT / "VERDICT.json").write_text(json.dumps(verdict, indent=2) + "\n")
with (ROOT / "RESEARCH_LOG.md").open("a") as stream:
    stream.write(f"\n## {now} - source-scope phase sealed\n\n"
                 "- PASS_SOURCE_SCOPE. No remaining applicability, sign, normalization, endpoint, or angle-convention gap.\n"
                 "- Source facts, independent local proof, source hashes, original-proof limits, and bridge checks are recorded in REPORT.md and VERDICT.json.\n"
                 "- Best-guess completion: 100% of assigned source-scope audit, not the overall discovery/priority goal.\n"
                 "- Parent authorized a separate extensive primary-source priority phase after this seal. Its conclusions will be recorded separately without replacing this dated decision.\n")
(ROOT / "SOURCE_SCOPE_RESEARCH_LOG.md").write_text((ROOT / "RESEARCH_LOG.md").read_text())
names = [".gitignore", "REPORT.md", "VERDICT.json", "SOURCE_MANIFEST.json", "SOURCE_SCOPE_RESEARCH_LOG.md",
         "SOURCE_RETRIEVAL.json", "SOURCE_CONTENT_CHECK.json", "SOURCE_BRIDGE_CHECKS.json",
         "retrieve_sources.py", "inspect_source_content.py", "check_source_bridge.py", "seal_source_scope.py"]
authored = {"sealed_at_utc": now, "phase": "source_scope_only",
            "files": {name: {"sha256": sha(ROOT / name), "bytes": (ROOT / name).stat().st_size} for name in names}}
(ROOT / "AUTHORED_MANIFEST.json").write_text(json.dumps(authored, indent=2) + "\n")
print(json.dumps({"verdict": verdict["verdict"], "sealed_at_utc": now, "authored_file_count": len(names)}))
