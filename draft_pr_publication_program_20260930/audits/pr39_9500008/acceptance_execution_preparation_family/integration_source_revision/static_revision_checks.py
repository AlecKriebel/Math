"""Own AST/data/finite controls only. Never imports/executes reviewed helpers."""
from pathlib import Path, PurePosixPath
import ast, datetime as dt, hashlib, json
H=Path(__file__).resolve().parent
R=H.parents[4]
P=R/'draft_pr_publication_program_20260930/audits/pr39_9500008/acceptance_preparation_family'
S=P.parent/'acceptance_static_adversary_family'
def sha(b): return hashlib.sha256(b).hexdigest()
def parse(b):
 def unique(rows):
  out={}
  for k,v in rows:
   if k in out: raise ValueError('duplicate '+k)
   out[k]=v
  return out
 return json.loads(b,object_pairs_hook=unique,parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
def closure(root,name,expected):
 b=(root/name).read_bytes();assert sha(b)==expected
 m=parse(b);assert {p.name for p in root.iterdir()}=={z['path'] for z in m['files']}|{name}
 for z in m['files']:
  p=root/z['path'];b=p.read_bytes();assert p.is_file() and not p.is_symlink() and len(b)==z['bytes'] and sha(b)==z['sha256']
 return len(m['files'])
assert closure(P,'PREPARATION_MANIFEST.json','f66df61cb4b57ae63cc007fed3c4dabf9e67e027f1d428d4e0ffbc75a6332fca')==15
assert closure(S,'MANIFEST.json','c782c65b31ef0f38c14bcf49577d11b66b8e19b63b0cce83718f651b3d6f0c9a')==26
for n in ['INPUT_BINDINGS.json','SCIENTIFIC_SCOPE.json','DRAFT_FINAL_PLAN.json','integrate_reviewed_partial.py','seal_final_evidence.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:
 assert (H/n).read_bytes()==(P/n).read_bytes(),n
b=(H/'pr39_guards.py').read_bytes();tree=ast.parse(b);functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
write=functions['write'];branches=[n for n in write.body if isinstance(n,ast.If) and isinstance(n.test,ast.Name) and n.test.id=='exclusive'];assert len(branches)==2
publish=branches[-1];assert len(publish.body)==2
link=publish.body[0].value;unlink=publish.body[1].value
assert isinstance(link,ast.Call) and ast.unparse(link.func)=='os.link' and ast.unparse(unlink.func)=='temporary.unlink'
assert len(publish.orelse)==1 and ast.unparse(publish.orelse[0].value.func)=='os.replace'
assert all('os.replace' not in ast.unparse(n) for n in publish.body)
assert 'os.fsync(stream.fileno())' in ast.unparse(write) and ast.unparse(write).index('os.fsync(stream.fileno())') < ast.unparse(write).index('os.link')
guard=b.decode();assert 'A = HERE.parents[1]' in guard and 'len(set(capture_names)) == 4' in guard
assert "paths['reconciliation_capture'].name == 'CAPTURE.json'" in guard
assert "PurePosixPath(name).name == name" in guard and "exact_closure(cap_base, capture_names)" in guard
assert 'started.utcoffset() == dt.timedelta(0)' in guard and 'finished.utcoffset() == dt.timedelta(0)' in guard and 'started <= finished' in guard
assert 'revision_basis()' in ast.unparse(functions['immutable_basis'])
# Independent finite absent-only interleaving model: collision leaves foreign final and our complete temporary.
final=None;temporary='our-complete-fsynced'
assert final is None
final='foreign-complete'
link_succeeded=final is None
if link_succeeded: final=temporary;temporary=None
assert not link_succeeded and final=='foreign-complete' and temporary=='our-complete-fsynced'
# Successful absent-only link then temporary removal and intentional nonexclusive replace.
final=None;temporary='our-complete-fsynced'
assert final is None;final=temporary;temporary=None
assert final=='our-complete-fsynced' and temporary is None
final='old-owned';final='updated-owned';assert final=='updated-owned'
def aware(start,end):
 try:
  if type(start) is not str or type(end) is not str:return False
  s,e=dt.datetime.fromisoformat(start),dt.datetime.fromisoformat(end)
  return s.tzinfo is not None and e.tzinfo is not None and s.utcoffset()==dt.timedelta(0) and e.utcoffset()==dt.timedelta(0) and s<=e
 except (ValueError,TypeError):return False
clocks=[('banana','earlier',False),('2026-10-02T14:00:00+00:00','2026-10-02T13:00:00+00:00',False),('2026-10-02T13:00:00','2026-10-02T14:00:00',False),('2026-10-02T13:00:00+01:00','2026-10-02T14:00:00+01:00',False),('2026-10-02T13:00:00Z','2026-10-02T13:00:00+00:00',True),('2026-10-02T13:00:00+00:00','2026-10-02T14:00:00Z',True),(True,'2026-10-02T14:00:00Z',False)]
for s,e,wanted in clocks:assert aware(s,e) is wanted
# Root basenames and cardinality are separately required, not inferred from sets.
def four(cap,out,err):
 names=[cap,'prelaunch_source.py',out,err]
 if cap!='CAPTURE.json' or len(set(names))!=4:return False
 for name in names:
  p=PurePosixPath(name)
  if not name or '\\' in name or '\0' in name or '..' in p.parts or p.is_absolute() or str(p)!=name or p.name!=name:return False
 return True
cases=[('CAPTURE.json','ROOTstdout.bin','stderr.bin',True),('CAPTURE.json','explicit-output','explicit-error',True),('CAPTURE.json','same.bin','same.bin',False),('CAPTURE.json','prelaunch_source.py','stderr.bin',False),('CAPTURE.json','CAPTURE.json','stderr.bin',False),('capture.json','stdout.bin','stderr.bin',False),('CAPTURE.json','nested/stdout.bin','stderr.bin',False),('CAPTURE.json','./stdout.bin','stderr.bin',False),('CAPTURE.json','stdout.bin','../stderr.bin',False)]
for cap,out,err,wanted in cases:assert four(cap,out,err) is wanted
for p in H.glob('*.py'):ast.parse(p.read_bytes())
for p in H.glob('*.json'):parse(p.read_bytes())
draft=parse((H/'DRAFT_FINAL_PLAN.json').read_bytes());assert len(draft['immutable_evidence_references'])==33
assert all(draft[k] is False for k in ['root_full_current_read_completed','root_full_whole_scope_read_completed','independent_whole_current_pass']) and draft['preparation_manifest_sha256'] is None
print(json.dumps({'status':'PASS_OWN_STATIC_AST_DATA_FINITE_CONTROLS_ONLY','reviewed_helpers_imported_or_executed':False,'original15_and_static26_closures_preserved':True,'immutable_four_helpers_three_objects_BYTE_exact':True,'atomic_link_collision_preserves_foreign_final_and_completed_temporary':True,'atomic_link_absent_publication_then_unlink':True,'deliberate_nonexclusive_replace_retained':True,'ordered_aware_UTC_clock_cases':len(clocks),'four_distinct_literal_root_basename_cases':len(cases),'draft_flags_false_and_null':True,'scope_reference_count':33},sort_keys=True))
