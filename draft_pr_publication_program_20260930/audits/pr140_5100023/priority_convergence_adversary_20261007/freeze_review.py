from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys, difflib

d = Path(__file__).resolve().parent
b = d.parent
if (d / "FINAL_MANIFEST.json").exists():
    raise SystemExit("Already frozen; refusing to revise this review")
now = datetime.now(timezone.utc).isoformat()
pid = os.getpid()

def pin(p, relative):
    raw = p.read_bytes()
    return {"relative": relative, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "mode": p.stat().st_mode & 0o777}

initial = json.loads((d / "INITIAL_INPUT_PINS.json").read_text())
unchanged = []
for expected in initial["input_pins"]:
    observed = pin(b / expected["relative"], expected["relative"])
    ok = all(observed[k] == expected[k] for k in ("bytes", "sha256", "mode"))
    unchanged.append({"relative": expected["relative"], "unchanged": ok, "observed": observed})
if not all(x["unchanged"] for x in unchanged):
    raise SystemExit("An initially pinned input changed; review required")

families = []
for folder, key in [("historical_general_priority_adversary_20261007", "public_files"),
                    ("contemporary_k405_priority_adversary_20261007", "members")]:
    root = b / folder
    mf = json.loads((root / "FINAL_MANIFEST.json").read_text())
    members = mf[key]
    checks = []
    for expected in members:
        relative = expected.get("path", expected.get("relative"))
        observed = pin(root / relative, relative)
        keys = ("bytes", "sha256", "mode") if "mode" in expected else ("bytes", "sha256")
        checks.append({"relative": relative, "matches_frozen_manifest": all(observed[k] == expected[k] for k in keys)})
    excluded = set(mf.get("private_folders_excluded", []))
    actual = set()
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        relative = p.relative_to(root).as_posix()
        if any(relative == x or relative.startswith(x + "/") for x in excluded):
            continue
        actual.add(relative)
    expected_names = {x.get("path", x.get("relative")) for x in members} | {"FINAL_MANIFEST.json"}
    item = {"folder": folder, "member_count": len(members), "all_member_checks_pass": all(x["matches_frozen_manifest"] for x in checks),
            "portable_census_matches": actual == expected_names, "checks": checks,
            "manifest_pin": pin(root / "FINAL_MANIFEST.json", folder + "/FINAL_MANIFEST.json")}
    families.append(item)
if not all(x["all_member_checks_pass"] and x["portable_census_matches"] for x in families):
    raise SystemExit("Frozen predecessor seal mismatch; report required")

more = [
 "historical_general_priority_adversary_20261007/SEARCH_LOG.json",
 "contemporary_k405_priority_adversary_20261007/CHECKABLE_SCOPE_BRIDGE.md",
 "contemporary_k405_priority_adversary_20261007/SOURCE_ACCESS_AND_SEARCH_BOUNDARIES.json",
 "ROOT_priority_reading_20261007/exact_author_page.html",
 "historical_general_priority_adversary_20261007/private_primary_sources/bialy_tabachnikov_published.txt",
 "historical_general_priority_adversary_20261007/private_primary_sources/gutkin_tabachnikov_2002.txt",
 "historical_general_priority_adversary_20261007/private_primary_sources/reznik_garcia_koiller_v11.html",
 "historical_general_priority_adversary_20261007/private_primary_sources/schwartz_tabachnikov_2016.html"
]
evidence = {"schema": "pr140-priority-convergence-input-readback/v1", "UTC": now, "actual_PID": pid,
            "initial_inputs_unchanged": True, "initial_checks": unchanged,
            "additional_read_inputs": [pin(b / r, r) for r in more],
            "predecessor_seals": families, "copyright_bodies_copied": False}
(d / "INPUT_AND_SEAL_VERIFICATION.json").write_text(json.dumps(evidence, indent=2) + "\n")
diff = "\n".join(difflib.unified_diff((b / "original/PROOF.md").read_text().splitlines(),
                                     (b / "repaired_candidate_v1/PROOF.md").read_text().splitlines(),
                                     fromfile="September30_public_original", tofile="accepted_repair", n=2)) + "\n"
(d / "ORIGINAL_TO_REPAIR_PROVENANCE_DIFF.txt").write_text(diff)
result = {
 "schema": "pr140-priority-convergence-adversary-result/v1",
 "frozen_UTC": now, "actual_freezer_PID": pid, "python": sys.version,
 "reviewer": "/root/pr140_priority_convergence_adversary_20261007",
 "original_head": "9e908ae58b5ceee6a0825bbebd8acf565db55340",
 "problem_id": "5100023", "source_invariant": "k405",
 "status": "BOUNDED_PRIORITY_SUPPORTS_QUALIFIED_RESOLUTION_NOTE",
 "priority_is_absolute_PASS": False,
 "earlier_complete_answer_before_documented_PR": "NOT_ESTABLISHED_IN_INSPECTED_PRIMARY_LITERATURE",
 "classical_tools_prior": True, "historical_reduction_requires_target_pair_identity": True,
 "historical_complete_subsumption_established": False,
 "exact_contemporary_overlap": True, "specific_contemporary_deposit_precedes_documented_PR": False,
 "documented_PR_created_at": "2026-09-30T11:31:05Z",
 "documented_PR_chronology_provenance": "ROOT provider-backed receipt checked against supplied immutable input pins; no independent new server request",
 "contemporary_deposit_created_at": "2026-10-01T23:58:07.321420+00:00",
 "contemporary_publication_date": "2026-10-02", "contemporary_DOI": "10.5281/zenodo.23092466",
 "accepted_original_already_contains_same_scoped_theorem_and_pair_formula": True,
 "proof_repair_delta": "Source-attribution paragraph only; original already explicitly even least period",
 "absolute_priority": "UNESTABLISHED", "exclusive_theorem_novelty_over_later_note": False,
 "independent_discovery": "UNESTABLISHED", "copying_or_collaboration_inference": False,
 "universal_bridge_first_occurrence": "UNESTABLISHED",
 "concrete_unresolved_prior_complete_theorem_lead_found": False,
 "generic_bounded_literature_uncertainty_remains": True,
 "close_as_already_solved_recommended": False,
 "new_user_exception_required_for_this_qualified_framing": False,
 "PR50_exception_used": False,
 "recommendation": "Proceed to concise package preparation and fresh adversarial package reviews under the existing goal, with explicit overlap/provenance and no exclusive priority claim",
 "defensible_contribution": "Verified self-contained full resolution in the accepted original-source primitive-even confocal-elliptic scope; explicit coefficient; documented project proof disclosure before this exact later deposit",
 "mandatory_framing_repairs": [
  "Say a proof was publicly posted in PR140 on September30; do not use unqualified first documented or first proof.",
  "Cite and substantively compare the exact Ferudun theorem, coefficient and shared pair/moment mechanism.",
  "Credit classical symmetry, stationarity/conservation, and prior skew/pedal machinery when discussed or used.",
  "State source unproved status and bounded historical audit; do not describe the problem as currently unsolved at publication.",
  "Preserve even least period, nondegenerate confocal elliptic caustic, original full-line antipedal and unweighted vertex mean scope.",
  "Do not propagate the superseded comparison_pending flag as the final combined state.",
  "Complete the authoritative goal's publication-package fresh adversarial review loops."
 ],
 "optional_bounded_followups": [
  "Improve originalVeselov/M'Clelland attribution if useful; no specific target theorem located there.",
  "Reopen priority if an actual earlier version or complete old antipedal bridge is identified."
 ],
 "new_mathematical_defects": [], "mathematical_gate_rerun": False,
 "new_central_proof_search_turns": 0, "new_mathematical_reproduction_loops": 0,
 "both_frozen_priority_reports_read": True, "early_family_independence_claimed_by_this_convergence_reviewer": False,
 "additional_queries": 12,
 "initial_inputs_unchanged": True, "predecessor_seals_verified": True,
 "bounded_assignment_completion_percent": 100, "overall_case_best_guess_percent": 75,
 "overall_goal_complete": False, "publication_upload_clearance": False,
 "actions": {"own_review_folder_writes_only": True, "Git_ref_index_native_program_PR_Zenodo_tracker_mutations": False,
             "new_Git_PR_Zenodo_requests": False, "external_human_contact": False, "outreach_prepared": False,
             "copyright_primary_bodies_exported": False}
}
(d / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
with (d / "RESEARCH_LOG.md").open("a") as f:
    f.write("\n" + now + " — Final checkpoint; actual PID " + str(pid) + ". Both frozen families reconciled; older full subsumption remains unestablished, exact later overlap acknowledged, original already contains the same scoped theorem. Twelve additional queries and actual source-statement reads identify no concrete earlier complete proof. Recommendation: qualified resolution note under existing goal, no absolute novelty/independence claim, no PR50 exception. Completion estimate: 100% bounded convergence; 75% overall PR140 case. Predecessor seals and all initial inputs match.\n")
for p in d.iterdir():
    if p.is_file():
        p.chmod(0o444)
members = [pin(p, p.name) for p in sorted(d.iterdir()) if p.is_file()]
manifest = {"schema": "pr140-priority-convergence-closed-manifest/v1", "UTC": now, "actual_freezer_PID": pid,
            "root_relative_folder": d.name, "self_excluded": "FINAL_MANIFEST.json", "member_count": len(members),
            "members": members, "copyright_bodies_exported": False,
            "status": result["status"], "overall_case_complete": False, "publication_upload_clearance": False}
(d / "FINAL_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
(d / "FINAL_MANIFEST.json").chmod(0o444)
print(json.dumps({"UTC": now, "actual_PID": pid, "status": result["status"], "member_count": len(members),
                  "final_manifest_sha256": hashlib.sha256((d / "FINAL_MANIFEST.json").read_bytes()).hexdigest(),
                  "predecessor_seals_verified": True, "own_folder_bytes": sum(p.stat().st_size for p in d.iterdir() if p.is_file())}))

