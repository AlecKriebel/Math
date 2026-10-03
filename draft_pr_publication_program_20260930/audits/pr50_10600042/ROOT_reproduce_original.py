"""ROOT literal private PR50 reproduction; diagnostics supplement universal proof."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat,sys
A=Path(__file__).absolute().parent;R=A.parents[2];O=A/'original'
from capture_readonly import capture
assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
 def pairs(items):
  d={}
  for k,v in items:assert k not in d;d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def eq(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
 return a==b
m=parse((A/'ORIGINAL_MANIFEST.json').read_bytes());refs=[]
for row in m['files']:
 p=O/row['path'];b=p.read_bytes();assert not p.is_symlink() and len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
 if p.suffix=='.json':parse(b)
 if p.suffix=='.jsonl':
  for line in b.splitlines():parse(line)
 refs.append(dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)))
assert len(refs)==15
w=A/'ROOT_private_reproduction';w.mkdir();runs=[]
for name,script,receipt,n in [('ROOT_author_replay','verify_even_moves.py','even_move_verification.json',3219),('ROOT_prior_independent_replay','review/independent_checks.py','review/independent_results.json',6641)]:
 c,out,err=capture(name,['/usr/bin/python3','-B',str(O/script)],cwd=w,source=O/script);v=parse(out);old=(O/receipt).read_bytes()
 assert c['exit_code']==0 and c['source_unchanged'] and c['operator_unchanged'] and not err and out==old and eq(v,parse(old)) and type(v['exact_assertions']) is int and v['exact_assertions']==n
 runs.append(dict(capture=c,complete_result=v,stdout_bytes=len(out),stdout_sha256=sha(out),literal_receipt_byte_identical=True))
assert not list(w.iterdir());w.rmdir()
for z in refs:assert sha((R/z['path']).read_bytes())==z['sha256'] and stat.S_IMODE((R/z['path']).stat().st_mode)==z['full_mode']
o=dict(schema='pr50-ROOT-complete-literal-reproduction/v1',actual_pid=os.getpid(),utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='PASS_ROOT_UNCHANGED_15_ORIGINALS_AND_BOTH_LITERAL_RECEIPTS',complete_original_bindings=refs,runs=runs,finite_checks_are_diagnostics_only=True,unrestricted_theorems_imported=True,fresh_independent_reviews_pending=True,priority_unestablished=True,future_acceptance_approved=False)
with (A/'ROOT_ORIGINAL_REPRODUCTION.json').open('x') as f:json.dump(o,f,indent=2);f.write('\n')
print(json.dumps(dict(status=o['status'],actual_pid=os.getpid(),originals=15,author_assertions=3219,prior_independent_assertions=6641,priority_unestablished=True)))
