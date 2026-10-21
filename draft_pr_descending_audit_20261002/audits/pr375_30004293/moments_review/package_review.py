#!/usr/bin/env python3
"""Finalize the exact owned public allowlist; never enumerate/copy raw sources."""
import datetime, hashlib, json, pathlib, subprocess

BASE=pathlib.Path(__file__).resolve().parent
PUBLIC=(
    "README.md", "RESEARCH_LOG.md", "PRE_CANDIDATE_SEAL.md", "PRE_CANDIDATE_SEAL.sha256",
    "MATHEMATICAL_VERDICT.md", "MATHEMATICAL_VERDICT.sha256", "MATHEMATICAL_VERDICT.original_sealed.sha256",
    "acquire_sources.py", "acquire_sources.stdout", "acquire_sources.stderr", "SOURCE_IDENTITY.json",
    "independent_controls.py", "independent_controls.stdout", "independent_controls.stderr", "INDEPENDENT_CONTROLS.json",
    "replay_relevant_author.py", "replay_relevant_author.stdout", "replay_relevant_author.stderr",
    "replay_relevant_author.initial.py", "replay_relevant_author.initial.stdout", "replay_relevant_author.initial.stderr",
    "author_turn5.stdout", "author_turn5.stderr", "AUTHOR_REPLAY_CORROBORATION.json",
    "package_review.py", "package_review.stdout", "package_review.stderr", "PACKAGING_CHECKS.json",
)

def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    ignored=subprocess.run(["git","check-ignore",str(BASE/"tmp"/"ignore_probe")],capture_output=True,text=True)
    assert ignored.returncode==0, "Private temporary path must remain ignored"
    controls=json.loads((BASE/"INDEPENDENT_CONTROLS.json").read_text())
    replay=json.loads((BASE/"AUTHOR_REPLAY_CORROBORATION.json").read_text())
    assert controls["exact_assertions"]==55580
    assert replay["returncode"]==0 and replay["receipt_equal"]
    assert replay["target_file_count"]==53 and replay["snapshot_binding_count"]==54 and replay["all_snapshot_bindings_match"]
    original=(BASE/"tmp"/"MATHEMATICAL_VERDICT.original_sealed.md").read_bytes()
    final=(BASE/"MATHEMATICAL_VERDICT.md").read_bytes()
    original_lines=original.splitlines(keepends=True)
    final_lines=final.splitlines(keepends=True)
    assert original_lines[:2]==final_lines[:2] and original_lines[3:]==final_lines[3:], "Only opening metadata may differ from sealed original"
    recorded_original=(BASE/"MATHEMATICAL_VERDICT.original_sealed.sha256").read_text().split()[0]
    assert sha(original)==recorded_original
    assert sha(final)==(BASE/"MATHEMATICAL_VERDICT.sha256").read_text().split()[0]
    assert sha((BASE/"PRE_CANDIDATE_SEAL.md").read_bytes())==(BASE/"PRE_CANDIDATE_SEAL.sha256").read_text().split()[0]
    identities=json.loads((BASE/"SOURCE_IDENTITY.json").read_text())
    sources=[]
    for item in identities["sources"]:
        path=BASE/"tmp"/"sources"/(item["identity"]+".pdf")
        assert sha(path.read_bytes())==item["sha256"]
        sources.append({"identity":item["identity"],"url":item["url"],"sha256":item["sha256"],"bytes":item["bytes"],"private_raw_excluded":True})
    checks={"utc":now,"private_ignore_returncode":ignored.returncode,"private_ignore_stdout":ignored.stdout,"private_ignore_stderr":ignored.stderr,"independent_exact_assertions":controls["exact_assertions"],"author_replay_receipt_equal":True,"all_54_snapshot_bindings_match":True,"target_file_count":53,"snapshot_binding_count":54,"original_mathematical_seal_sha256":sha(original),"final_metadata_corrected_sha256":sha(final),"mathematical_body_unchanged":True,"source_identities":sources,"raw_extract_render_files_in_public_allowlist":False,"completion_percent_bounded_audit":100,"original_goal":"unresolved"}
    (BASE/"PACKAGING_CHECKS.json").write_text(json.dumps(checks,indent=2)+"\n")
    (BASE/"RESEARCH_LOG.md").open("a").write(f"- {now} - Final packaging verifies source identities, unchanged mathematical body, replay receipt, all 54 frozen bindings and ignored private storage. Exact owned public allowlist finalized. Completion estimate: 100% of bounded audit; original mathematical rate goal remains unresolved. No candidate/Git/remote/service mutations, outreach, release or DOI action.\n")
    # Write our complete public streams before computing their manifest hashes.
    (BASE/"package_review.stdout").write_text(json.dumps({"success":True,"owned_public_files_excluding_manifest":len(PUBLIC),"independent_assertions":55580,"snapshot_bindings":54,"mathematical_body_unchanged":True},indent=2)+"\n")
    (BASE/"package_review.stderr").write_text("")
    observed={p.name for p in BASE.iterdir() if p.is_file() and p.name!="MANIFEST.json"}
    assert observed==set(PUBLIC), {"unexpected":sorted(observed-set(PUBLIC)),"missing":sorted(set(PUBLIC)-observed)}
    files=[]
    for name in PUBLIC:
        path=BASE/name
        assert "tmp" not in pathlib.Path(name).parts and path.is_file()
        data=path.read_bytes()
        files.append({"path":name,"bytes":len(data),"sha256":sha(data)})
    manifest={"utc":now,"owned_directory":str(BASE),"frozen_head":"36c29bb039471f132889d577c9322d78925b62dd","problem_id":30004293,"pr":375,"verdict":"PASS for assigned scoped moments/tails/logarithmic expectations; original quantitative goal unsolved","mandatory_mathematical_fixes":[],"exact_owned_public_allowlist":list(PUBLIC)+["MANIFEST.json"],"manifest_self_hash_excluded":True,"third_party_raw_extract_render_excluded":True,"private_storage_ignore_verified":True,"public_file_count_including_manifest":len(PUBLIC)+1,"files":files,"source_identities":sources,"snapshot_binding_report":"AUTHOR_REPLAY_CORROBORATION.json","full_snapshot_binding_count":54,"target_file_count":53,"independence":"Sources and mechanisms before candidate prose; universal verdict sealed before relevant author replay or historical review; opening timestamp only corrected afterwards with body byte-identical.","historical_corroboration":"Read historical ADVERSARIAL_REVIEW only after seal. Its scoped conclusions agree; no historical assertion was substituted for independent proof or controls.","completion_percent_bounded_audit":100,"original_quantitative_goal_unresolved":True}
    (BASE/"MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")

if __name__=="__main__":main()
