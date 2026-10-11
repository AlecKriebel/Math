"""One-shot local seal after root's recorded authorization. No math rerun."""
import argparse, datetime, hashlib, json, pathlib
import verify_namespace as verifier

N = pathlib.Path(__file__).resolve().parent

def stamp(path):
    data = path.read_bytes()
    return {"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approval",required=True,help="Existing root authorization JSON below private/")
    args = parser.parse_args()
    assert not any((N/name).exists() for name in verifier.GENERATED), "seal already exists; never overwrite"
    approval_name = verifier.safe(args.approval)
    assert approval_name.startswith("private/")
    approval_path = N/approval_name
    approval = verifier.load(approval_path)
    assert approval["authorized_by"] == "/root" and approval["one_shot_local_seal_authorized"] is True
    assert approval["root_message_exact"] and approval["observed_utc"]
    before = verifier.verify(draft=True)
    files,dirs = verifier.tree()
    plan = verifier.load(N/"CLOSURE_PLAN.json")
    whitelist = set(plan["public_whitelist_before_generated_closure"])
    sealed_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    def entries(names):
        return [{"path":name,**stamp(N/name)} for name in sorted(names)]
    public = {"schema_version":1,"sealed_utc":sealed_utc,"layer":"public_author_reports_controls_and_custody_summaries",
              "files":entries(whitelist)}
    private = {"schema_version":1,"sealed_utc":sealed_utc,"layer":"private_sources_raw_kit_renders_full_native_receipts_and_versions",
               "files":entries(files-whitelist),"directories":sorted(dirs)}
    for name,obj in [("PUBLIC_MANIFEST.json",public),("PRIVATE_MANIFEST.json",private)]:
        with (N/name).open("x") as output:
            output.write(json.dumps(obj,indent=2)+"\n")
    closure = {"schema_version":1,"closed":True,"status":"FINAL_CLOSED","sealed_utc":sealed_utc,
               "candidate_head":"6be98eac0ba508368218179ecf80020c037dbece",
               "candidate_base":"efd29c05204703acca9a0860812f54b94fae54b1",
               "scope":"Second independent source-first whole-preprint adversarial review of PR359/30001370/OWR-4132-003 only",
               "finding":"PASS exact all-density relative-L1 common-boundary and finite-preimage closure claim; no mandatory submission repair identified",
               "public_manifest":stamp(N/"PUBLIC_MANIFEST.json"),"private_manifest":stamp(N/"PRIVATE_MANIFEST.json"),
               "public_files":len(public["files"]),"private_files":len(private["files"]),
               "root_approval_receipt":{"path":approval_name,**stamp(approval_path)},
               "primary_gate_sha256":plan["primary_gate_sha256"],
               "full_package_outputs_compared_to_current_expected":True,
               "subjective_scoped_audit_completion_percent":100,"human_peer_review":False,
               "known_limits":["Bounded priority evidence does not certify universal novelty","Final BKZ journal proof version not obtained","No independent external human peer review","Private priority dossier payloads absent from public ZIP and not freshly reverified here"],
               "preseal_read_only_verification":before,"no_namespace_writes_after_seal":True,
               "closed_verifier_captures":"Full/public postseal argv/cwd/UTC/exit/stdout/stderr are captured outside this namespace by root and bound in its external final gate"}
    # This is the final namespace write. All following work is read-only.
    with (N/"CLOSURE.json").open("x") as output:
        output.write(json.dumps(closure,indent=2)+"\n")
    print(json.dumps({"status":"SEALED_ONCE","closure":{"path":str(N/"CLOSURE.json"),**stamp(N/"CLOSURE.json")},
                      "sealed_utc":sealed_utc,"public_files":closure["public_files"],"private_files":closure["private_files"]},indent=2))

if __name__ == "__main__":
    main()
