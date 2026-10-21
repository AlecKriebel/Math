from pathlib import Path
import json,hashlib,datetime,subprocess,sys,os
A=Path("draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616").resolve();O=A/"original/unsolved_math_prioritization/attempts/2616/author/public"
D=A/"supplemental";D.mkdir(exist_ok=False)
raw=(O/"verify.py").read_bytes();assert hashlib.sha256(raw).hexdigest()=="b805650e49c5096f0fe368653122989c1087f59447871a5cb6fc32843d6983d1"
old=b"except (Invalid, ValueError, TypeError, KeyError, OSError, UnicodeError) as exc:"
new=b"except (Invalid, ValueError, TypeError, KeyError, OSError, UnicodeError, RecursionError) as exc:"
assert raw.count(old)==1
patched=raw.replace(old,new);(D/"verify_robust.py").write_bytes(patched)
fixture=(O/"fixtures.json").read_bytes();(D/"fixtures.json").write_bytes(fixture)
(D/"README.md").write_text("""# Publication-only checker repair

The immutable submitted 26-file attempt remains unchanged. verify_robust.py differs from its author/public/verify.py by adding RecursionError to the existing structured-error handler. No mathematical check, fixture, loop bound or proof has changed. This repairs audit findingO1: a bounded deeply nested JSON document was already rejected, but emitted an uncaught traceback. The supplemental checker returns a nonzero exit with a structured JSON error instead.

Run with isolated standard-library Python:
    python3 -I -S -B verify_robust.py fixtures.json

The original verifier SHA-256 is b805650e49c5096f0fe368653122989c1087f59447871a5cb6fc32843d6983d1. The adjacent REPAIR_AND_REGRESSION.json records the exact one-line change, real command outcomes, current runtime and output digests. The audit's original adverse results are retained. This is a software error-format repair, not an additional author proof response, mathematical approach, security proof, free-ultrafilter simulation or formal verification of the infinite theorem.
""")
rows=[]
for mode,flags in [(0,[]),(1,["-O"]),(2,["-OO"])]:
 for label,payload,accept in [
  ("valid_pinned_fixture",fixture,True),
  ("valid_exact65536_boundary",fixture+b" "*(65536-len(fixture)),True),
  ("reject_exact65537_boundary",fixture+b" "*(65537-len(fixture)),False),
  ("deep_array2000",b"["*2000+b"0"+b"]"*2000,False),
  ("deep_object2000",b'{"a":'*2000+b"0"+b"}"*2000,False),
  ("deep_array950",b"["*950+b"0"+b"]"*950,False),
  ("duplicate_key",fixture.replace(b'"schema_version": 1',b'"schema_version": 1,"schema_version":1'),False),
  ("boolean_integer",fixture.replace(b'"problem_id": 2616',b'"problem_id":true'),False)]:
  utc=datetime.datetime.now(datetime.timezone.utc).isoformat();cmd=[sys.executable,"-I","-S","-B",*flags,str(D/"verify_robust.py"),"--stdin"]
  r=subprocess.run(cmd,input=payload,cwd=D,capture_output=True,timeout=30)
  assert (r.returncode==0)==accept,(mode,label,r.stderr)
  output=json.loads(r.stdout if accept else r.stderr)
  assert output["ok"] is accept and (r.stderr==b"" if accept else r.stdout==b"")
  if accept: assert output["counts"]=={"group_and_coset_cases":4096,"maximum_fibers":13,"dense_coloring_extensions":23040,"finite_disjoint_block_assignments":16384}
  rows.append({"launch_utc":utc,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"argv":cmd,"mode":mode,"label":label,"input_bytes":len(payload),"input_sha256":hashlib.sha256(payload).hexdigest(),"exit":r.returncode,"stdout":r.stdout.decode(),"stderr":r.stderr.decode(),"expected_accept":accept,"actual_structured_output":True})
assert (O/"verify.py").read_bytes()==raw and patched.replace(new,old)==raw
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"original_sha256":hashlib.sha256(raw).hexdigest(),"supplemental_sha256":hashlib.sha256(patched).hexdigest(),"exact_one_line_change":{"from":old.decode(),"to":new.decode()},"original_immutable_preserved":True,"new_author_proof_responses":0,"uid":os.getuid(),"python":sys.version,"actual_cases":len(rows),"all_pass":True,"runs":rows}
(D/"REPAIR_AND_REGRESSION.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="runs"},indent=2))
