#!/usr/bin/env python3
"""Small supplemental profile probes, preserving existing reproduction receipts."""
from pathlib import Path
import datetime, hashlib, json, shutil, sys, tempfile, types
sys.dont_write_bytecode = True
OUT=Path(__file__).resolve().parent
SOURCE=OUT.parents[1]/"original/unsolved_math_prioritization/attempts/30004549"
PIN="18b022a9f45f4b8194629cae8143f6be4884dbba51b7616cc64c1b7ab2cf7117"
def sha(data): return hashlib.sha256(data).hexdigest()
def need(condition,message):
    if not condition: raise RuntimeError(message)
events=[]
outputs=[(OUT/("WRAPPER_"+mode+".json")).read_bytes() for mode in ("NORMAL","OPTIMIZED","ISOLATED")]
need(len(set(outputs))==1,"wrapper mode bytes differ")
need(outputs[0]==(SOURCE/"VERIFICATION_RESULTS.json").read_bytes(),"historical wrapper receipt differs")
events.append({"test":"wrapper_all_modes_exact_historical_receipt","outcome":"pass","bytes":len(outputs[0]),"sha256":sha(outputs[0])})
with tempfile.TemporaryDirectory(dir=OUT/"tmp") as tmp:
    root=Path(tmp)/"package"
    shutil.copytree(SOURCE,root)
    mod=types.ModuleType("frozen_pr948_verifier")
    mod.__file__=str(root/"verify_publication.py")
    exec(compile((root/"verify_publication.py").read_bytes(),mod.__file__,"exec",optimize=0),mod.__dict__)
    def probe(name,edit,accept=False):
        clone=Path(tmp)/"mutated"
        shutil.copytree(root,clone)
        try:
            edit(clone)
            try: result=mod.verify(clone)
            except Exception as e:
                events.append({"test":name,"outcome":"rejected","exception":type(e).__name__,"message":str(e)})
                need(not accept,name+" should have exposed accepted limit")
            else:
                events.append({"test":name,"outcome":"accepted","result":result,"public_manifest_sha256":sha((clone/"PUBLIC_MANIFEST.json").read_bytes())})
                need(accept,name+" unexpectedly accepted")
        finally: shutil.rmtree(clone)
    def invalid_json(p):
        raw=b"{"
        (p/"PUBLIC_MANIFEST.json").write_bytes(raw)
        (p/"PUBLIC_MANIFEST.sha256").write_text(sha(raw)+"  PUBLIC_MANIFEST.json\n")
    probe("invalid_JSON_with_matching_sidecar",invalid_json)
    def invalid_array(p):
        raw=b"[]\n"
        (p/"PUBLIC_MANIFEST.json").write_bytes(raw)
        (p/"PUBLIC_MANIFEST.sha256").write_text(sha(raw)+"  PUBLIC_MANIFEST.json\n")
    probe("top_level_array_with_matching_sidecar",invalid_array)
    probe("missing_schema_with_matching_sidecar",lambda p:mod.rewrite_manifest(p,lambda m:m.pop("schema")))
    probe("null_manifest_entry",lambda p:mod.rewrite_manifest(p,lambda m:m["files"].__setitem__(0,None)))
    probe("boolean_payload_size",lambda p:mod.rewrite_manifest(p,lambda m:m["files"][0].update(bytes=True)))
    probe("floating_problem_id_equal_integer",lambda p:mod.rewrite_manifest(p,lambda m:m.update(problem_id=30004549.0)),accept=True)
    def rebind_readme(p):
        name="README.md"
        data=(p/name).read_bytes()+b"\nOWNED NEGATIVE REBIND PROBE\n"
        (p/name).write_bytes(data)
        def edit(m):
            for e in m["files"]:
                if e["path"]==name: e.update(bytes=len(data),sha256=sha(data),git_blob_sha1=mod.git_blob(data))
        mod.rewrite_manifest(p,edit)
        need(sha((p/"PUBLIC_MANIFEST.json").read_bytes())!=PIN,"rebind changes external manifest pin")
    probe("coherent_unpinned_README_rebind",rebind_readme,accept=True)
result={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"pass_with_explicit_limits","events":events,"notes":"The malformed JSON first-pass harness probe was stopped by sidecar mismatch; supplemental probe exercises JSON parser after matching sidecar. No new computation or mathematical construction."}
(OUT/"SUPPLEMENTAL_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
