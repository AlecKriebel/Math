"""Read-only body/capture audit of PR302's three closed scientific reviews.

This program writes only its dedicated ROOT evidence files. It grants no Git,
service, novelty, or publication authority. Historical pins are not silently
replaced by current bodies; unresolved differences are reported explicitly.
"""
import datetime, hashlib, json, os, pathlib, stat, sys

A = pathlib.Path(__file__).resolve().parent
FAMILIES = [A / x for x in ("math_empirical_adversary_01", "math_spectral_adversary_01", "math_scope_adversary_01")]
START = datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    p = pathlib.Path(p)
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), mode=oct(stat.S_IMODE(p.stat().st_mode)))
SELF = pin(__file__)
CACHE = {}
def current(p):
    s = str(p)
    if s not in CACHE: CACHE[s] = pin(p)
    return CACHE[s]
def objects(x, loc="$"):
    if isinstance(x, dict):
        if isinstance(x.get("path"), str) and "bytes" in x and "sha256" in x:
            yield loc, x
        for k,v in x.items(): yield from objects(v, loc+"."+k)
    elif isinstance(x,list):
        for i,v in enumerate(x): yield from objects(v,loc+"["+str(i)+"]")

result = dict(status="ROOT_PR302_CLOSED_REVIEW_CUSTODY_DIAGNOSTIC", start_UTC=START, actual_PID=os.getpid(), actual_argv=sys.orig_argv, cwd=os.getcwd(), source=SELF, original_head="eb6e0e999521d84a65f9857d338cad76b84d30db", families=[], historical_body_differences=[], missing_pinned_paths=[], mode_differences=[], native_captures=[])
snapshot = json.loads((A/"snapshot_manifest.json").read_bytes())
for row in snapshot["files"]:
    p=A/"snapshot"/row["path"]; q=current(p)
    assert q["bytes"]==row["bytes"] and q["sha256"]==row["sha256"] and q["mode"]=="0o444", row
    b=p.read_bytes(); blob=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    assert blob==row["git_blob_sha"], row
result["original_snapshot"] = dict(file_count=len(snapshot["files"]), bytes=sum(r["bytes"] for r in snapshot["files"]), manifest=current(A/"snapshot_manifest.json"), all_bodies_modes_and_Git_blob_ids_match=True)

for family in FAMILIES:
    inventory=json.loads((family/"OUTPUT_INVENTORY.json").read_bytes())
    rows=inventory.get("all_payload_files",inventory.get("files",inventory.get("payloads")))
    assert isinstance(rows,list)
    for row in rows:
        q=current(row["path"])
        assert q["bytes"]==row["bytes"] and q["sha256"]==row["sha256"] and q["mode"]=="0o444",row
    owned=[p for p in family.rglob("*") if p.is_file()]
    for p in owned: assert current(p)["mode"]=="0o444",p
    for p in [family]+[p for p in family.rglob("*") if p.is_dir()]: assert stat.S_IMODE(p.stat().st_mode)==0o555,p
    result["families"].append(dict(root=str(family), output_inventory=current(family/"OUTPUT_INVENTORY.json"), inventoried_payload_count=len(rows), inventoried_payload_bytes=sum(x["bytes"] for x in rows), all_current_file_count=len(owned), all_current_files=[current(p) for p in sorted(owned)], all_owned_file_modes="0444", all_owned_directory_modes="0555"))
    for p in sorted(owned):
        if p.suffix!=".json":continue
        x=json.loads(p.read_bytes())
        for loc,row in objects(x):
            target=pathlib.Path(row["path"])
            if not target.is_absolute():
                result["missing_pinned_paths"].append(dict(container=str(p),location=loc,pin=row,reason="relative path must be explicitly interpreted")); continue
            if not target.is_file():
                result["missing_pinned_paths"].append(dict(container=str(p),location=loc,pin=row)); continue
            q=current(target)
            if q["bytes"]!=row["bytes"] or q["sha256"]!=row["sha256"]:
                result["historical_body_differences"].append(dict(container=str(p),location=loc,historical_pin=row,current=q))
            expected=row.get("final_frozen_mode",row.get("mode",row.get("mode_at_authentication",row.get("launch_mode"))))
            if expected is not None:
                expected=oct(int(expected,8)) if isinstance(expected,str) else oct(expected)
                if q["mode"]!=expected:
                    result["mode_differences"].append(dict(container=str(p),location=loc,path=str(target),historical_mode=expected,current_mode=q["mode"],inside_closed_review=any(target.is_relative_to(f) for f in FAMILIES)))
        if p.name=="execution.json" and p.parent.name not in ("private_primary_sources",):
            req=p.parent/"request.json"
            if not req.exists():continue
            request=json.loads(req.read_bytes())
            pid=x.get("native_pid",x.get("pid"))
            assert isinstance(pid,int) and pid>0,(p,x)
            assert isinstance(x.get("exit_code"),int),(p,x)
            argv=x.get("argv",request.get("argv")); cwd=x.get("cwd",request.get("cwd"))
            assert isinstance(argv,list) and argv and isinstance(cwd,str),(p,x)
            for name in ("stdout","stderr"):
                row=x[name];q=current(row["path"])
                assert q["bytes"]==row["bytes"] and q["sha256"]==row["sha256"],(p,row)
            started=p.parent/"started.json"
            if started.exists():
                sx=json.loads(started.read_bytes());spid=sx.get("native_pid",sx.get("pid"))
                assert spid==pid,(p,sx,x)
            if "argv" in x:assert x["argv"]==request["argv"] and x["cwd"]==request["cwd"],p
            result["native_captures"].append(dict(execution=current(p),request=current(req),actual_PID=pid,argv=argv,cwd=cwd,exit_code=x["exit_code"],complete_stdout=current(x["stdout"]["path"]),complete_stderr=current(x["stderr"]["path"]),native_envelope=x))

result["current_distinct_pinned_file_count"]=len(CACHE)
result["complete_native_capture_count"]=len(result["native_captures"])
result["failed_native_captures"]=[r for r in result["native_captures"] if r["exit_code"]!=0]
result["all_output_inventories_match_and_all_original_blobs_unchanged"]=True
result["end_UTC"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
out=A/"ROOT_CLOSED_REVIEW_CUSTODY_DIAGNOSTIC.json"
assert not out.exists(),"Never overwrite an earlier diagnostic run"
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(dict(status=result["status"],actual_PID=result["actual_PID"],receipt=pin(out),inventories_match=True,original_29_blobs_match=True,native_captures=result["complete_native_capture_count"],current_distinct_pinned_files=len(CACHE),body_differences=len(result["historical_body_differences"]),missing_pinned_paths=len(result["missing_pinned_paths"]),mode_differences=len(result["mode_differences"]),failed_native_captures=len(result["failed_native_captures"]))))
