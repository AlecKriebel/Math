from pathlib import Path
import json,hashlib,ast,datetime,os
A=Path(__file__).resolve().parent;O=A/'original_source_authentication_20261006/original_attempt';S=A/'independent_reproduction_adversary_20261006/suggested_guard_repairs';D=A/'repaired_diagnostics_v1'
D.mkdir(exist_ok=False);(D/'independent_review/author_replay').mkdir(parents=True)
def sha(b):return hashlib.sha256(b).hexdigest()
proof=(O/'PROOF.md').read_text()
old='Empty clauses and empty formulas can be mapped to fixed no/yes instances; consequently assume n>=1 variables and m>=1 nonempty clauses, with no variable occurring in both signs within one clause.'
new='An empty clause maps to a fixed no-instance: two vertices with their unique edge, all arc costs1 at both roots and threshold1, whose unique tree has cost2. An empty remaining formula maps to the same graph with all costs0 and threshold0, a fixed yes-instance. Delete unused variable declarations and relabel the actual occurring variable symbols densely; n counts these symbols, never the largest numeric label. Consequently assume n>=1 variables and m>=1 nonempty clauses, with no variable occurring in both signs within one clause.'
if proof.count(old)!=1:raise RuntimeError('preprocessing source span changed')
proof=proof.replace(old,new)
proof=proof.replace('Status:** complete proof candidate; independent review pending.','Status:** mathematically audited candidate; final fresh family authentication pending, priority unestablished.')
pb=proof.encode();(D/'PROOF.md').write_bytes(pb);(D/'independent_review/author_replay/PROOF.md').write_bytes(pb)
for family,source,dest in [
 ('author',S/'author_normal/verify.py',D/'verify.py'),
 ('old_review',S/'old_review_normal/independent_checks.py',D/'independent_review/independent_checks.py')]:
 text=source.read_text()
 if family=='old_review':
  original_sha=sha((O/'PROOF.md').read_bytes())
  oldline="EXPECTED='"+original_sha+"'";newline="EXPECTED='"+sha(pb)+"'"
  if text.count(oldline)!=1:raise RuntimeError('old proof binding changed')
  text=text.replace(oldline,newline)
 if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(text))):raise RuntimeError('removable check')
 dest.write_text(text)
(D/'README.md').write_text('''# PR108 current audit diagnostics v1

The immutable submitted head and original receipts remain in the original
source-authentication archive. This version preserves the mathematical
reduction and adds explicit trivial yes/no endpoints and dense variable
relabeling. It replaces removable Python assertions in both author and old
independent checkers with explicit raising guards, adds verifier-body hashes
to receipts, and binds both checkers to this precise clarified proof.

Run `python3 verify.py` from this directory. Run
`python3 independent_review/independent_checks.py` from this directory for
the separate Prüfer/edge-cut suite. Both may also run with Python `-O`.
These finite diagnostics support the written proof; they do not establish
complexity hardness or novelty by enumeration. Fresh source/model and
arbitrary-tree families are separately preserved in the audit folder.

No novelty, present-open-status, preprint, DOI, merge or closure clearance
is provided by this repaired diagnostic snapshot. Original effort2/5 is
supported by QUEUE and the prose log; no historical structured ledger was
submitted. New central proof-search turns0.
''')
pins=[]
for q in sorted(D.rglob('*')):
 if q.is_file():
  b=q.read_bytes();pins.append({'file':str(q.relative_to(D)),'bytes':len(b),'sha256':sha(b)})
result={'schema':'pr108-effective-diagnostics-preparation/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'original_proof_sha256':sha((O/'PROOF.md').read_bytes()),'effective_proof_sha256':sha(pb),'mathematical_sections_changed':False,'routine_preprocessing_clarification':True,'diagnostic_guard_repair':True,'new_central_proof_search_turns':0,'original_budget':'2/5','pins':pins,'actual_reproduction_pending':True,'priority_clearance':False}
(D/'PREPARATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='pins'}))
