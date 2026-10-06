"""Isolated simulations. Never invokes Git, gh, network, shared native main, or tracker.
The native operator source is unchanged; only globals, capture transport and sourcepair
are replaced so the custody acceptance predicates can be tested independently.
"""
import ast, contextlib, datetime, hashlib, importlib.util, io, json, os, shutil, stat, sys, types
from pathlib import Path
O=Path(__file__).resolve().parent
S=O/'retained_sources'
results=[]
def record(name, **kw): results.append({'test':name,**kw})
def module(p,name):
 spec=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
# No top-level side effect execution for the two publication helpers.
for filename in ['01_verify_published_package.py','02_append_and_verify_tracker.py']:
 tree=ast.parse((S/filename).read_text())
 normal=len([x for x in ast.walk(tree) if isinstance(x,ast.Assert)])
 optimized=compile(tree,str(S/filename),'exec',optimize=1)
 # The first gate guard is separately compiled exactly, with intentionally false input.
 first=next(x for x in tree.body if isinstance(x,ast.Assert))
 regular=ast.Module(body=[first],type_ignores=[])
 env={'gate':{'publication_clearance':False},'pub':{'status':'UNVERIFIED'}}
 try: exec(compile(regular,filename,'exec',optimize=0),env);normal_rejected=False
 except AssertionError: normal_rejected=True
 exec(compile(regular,filename,'exec',optimize=1),env)
 record('optimization_removes_guard_'+filename,assert_count=normal,normal_false_gate_rejected=normal_rejected,optimized_false_gate_rejected=False)
# Exact sourcepair read-only reproduction, no operator invocation.
fake=types.ModuleType('capture');fake.capture=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('No shared transport'))
sys.modules['capture']=fake
native=module(S/'00_native_integrate.py','native_audit')
identity=native.sourcepair()
record('actual_read_only_sourcepair',source_identity=identity)
# Check actual snapshot 9 pins and actual manifest 8 entries using local read-only kit.
kit=module(S/'04_zenodo.py','zenodo_audit')
snapshot=json.loads((S/'07_PUBLICATION_PACKAGE_V2_REVIEW_SNAPSHOT_20261004.json').read_text())
P=Path(snapshot['package_directory'])
checks=[]
for item in snapshot['files']:
 b=(P/item['path']).read_bytes();checks.append(len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'])
metadata,files=kit.load_manifest(P/'zenodo-deposit.json')
record('actual_package_pin_readback',snapshot_count=len(snapshot['files']),all_pins_match=all(checks),manifest_payload_count=len(files),payload_names=[x['name'] for x in files])
# Strict tracker dedup / prior-unknown guards; no t.main and no gws.
t=module(S/'05_append_publication.py','tracker_audit')
keys={'unsolvedmath:OWR-785-003','unsolvedmath:30000177'}; doi=t.normalize_doi('10.5281/zenodo.123456')
rows=[t.HEADERS,['https://www.unsolvedmath.com/problems/OWR-785-003','','https://doi.org/'+doi,'N']]
record('tracker_alias_dedup',alias_keys=[t.normalize_problem('30000177'),t.normalize_problem('https://www.unsolvedmath.com/problems/OWR-785-003')],match=t.duplicate_row(rows,keys,doi))
for name,rs in [('same_problem_different_doi',[t.HEADERS,[rows[1][0],'','https://doi.org/10.5281/zenodo.654321','N']]),('same_doi_other_problem',[t.HEADERS,['30000999','','https://doi.org/'+doi,'N']]),('duplicate_pair',rows+[rows[1]])]:
 try:t.duplicate_row(rs,keys,doi);rejected=False;error=None
 except t.TrackerError as e:rejected=True;error=str(e)
 record('tracker_'+name,rejected=rejected,error=error)
receipts=O/'fixture_receipts_v2'; old=receipts/'tracker-attempt-old';old.mkdir(parents=True,exist_ok=True)
old.joinpath('append-attempted.json').write_text(json.dumps({'problem_keys':list(keys),'doi_key':doi}))
record('tracker_prior_unknown_marker_detected',matched=t.prior_append_attempts(receipts,receipts/'tracker-attempt-new',keys,doi))
# Exact merge row guard admits appended content outside its 14 checked cells.
oldrow='| 30000177 / OWR-785-003 | a | b | c | d | e | f | queued | 0/5 | j | n | u |\n'
newcells=oldrow.split('|');newcells[8]=' preprint_published ';newcells[9]=' 1/5 ';newcells[11]=' now ';newcells[12]=' '+doi+' '
newrow='|'.join(newcells)+'| injected foreign row |\n'
a,b=oldrow.split('|'),newrow.split('|')
accepted=all(a[i]==b[i] for i in range(14) if i not in (8,9,11,12)) and b[8].strip()=='preprint_published' and b[9].strip()=='1/5' and doi in b[12]
record('queue_row_guard_accepts_extra_foreign_line',existing_cell_count=len(a),replacement_cell_count=len(b),replacement_line_count=len(newrow.splitlines()),native_existing_predicates_accept=accepted,old_row=oldrow,replacement=newrow)
# Execute the unchanged native accept phase only in a synthetic fixture with
# simulated Git/GitHub. Deliberately modify one accepted document and one foreign
# untracked held file at simulated commit. No actual Git command or network call.
FR=O/'native_accept_fixture_v2';FA=FR/'draft_pr_publication_program_20260930/audits/pr80_30000177'; FA.mkdir(parents=True,exist_ok=True)
AUTH=FA/'original_source_authentication_20261004';AUTH.mkdir(exist_ok=True)
manifest=json.loads((S/'08_ORIGINAL_BLOB_MANIFEST.json').read_text()); originals=[x for x in manifest['files'] if x['path'].startswith(native.PREFIX+'/')]
AUTH.joinpath('ORIGINAL_BLOB_MANIFEST.json').write_text(json.dumps(manifest))
actual_auth=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr80_30000177/original_source_authentication_20261004/original_head')
for entry in originals:
 path=FR/entry['path'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((actual_auth/entry['path']).read_bytes());path.chmod(0o644)
for name,data in [(native.QUEUE,oldrow.encode()),(native.STATE,b'{\n  "other": {"status": "held"}\n}\n'),(native.HISTORY,b'{"id":"other","status":"held"}\n')]:
 path=FR/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
prepared=FA/'native_preparation_20261004';prepared.mkdir(exist_ok=True)
for name in ['CURRENT_RESULT.md','CURRENT_PRIORITY.md']:prepared.joinpath(name).write_text('Expected exact '+name+'\n')
foreign=FR/'foreign_untracked_held.txt';foreign.write_text('HELD ORIGINAL\n')
start='1'*40;end='2'*40;token='fixture-only-token';utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
owned=[x['path'] for x in originals]+[native.QUEUE,native.STATE,native.HISTORY]+[native.PREFIX+'/'+x for x in ['acceptance.json','CURRENT_RESULT.md','CURRENT_PRIORITY.md']]
plan={'UTC':utc,'ROOT_reviewed_for_execution':True,'PR':80,'head':native.HEAD,'exact_owned_paths':owned,'bound_inputs':[],'DOI':doi,'record_url':'https://zenodo.org/records/123456','tracker_range':"'Math Puzzles'!A2:D2",'exact_claim':'SYNTHETIC fixture; no clearance','queue_after_row':'|'.join(newcells)}
planpath=FA/'plan.json';planpath.write_text(json.dumps(plan))
ack={'UTC':utc,'token':token,'PR':80,'covers_phases':['merge','accept','checkpoint'],'exact_owned_paths':owned,'ROOT_plan_sha256':hashlib.sha256(planpath.read_bytes()).hexdigest(),'starting_main':start};ackpath=FA/'ack.json';ackpath.write_text(json.dumps(ack))
status=FR/'status.json';status.write_text(json.dumps({'shared_git_writes_paused':True,'ascending_pr80_publication_integration_lease_token':token}))
FA.joinpath('ROOT_FINAL_PACKAGE_GATE_20261004.json').write_text(json.dumps({'publication_clearance':True,'fixture':True}))
FA.joinpath('ROOT_PUBLICATION_VERIFICATION_20261004.json').write_text(json.dumps({'all8_public_bytes_identical':True,'intended_metadata_exact':True,'DOI':doi,'fixture':True}))
FA.joinpath('ROOT_TRACKER_VERIFICATION_20261004.json').write_text(json.dumps({'DOI':doi,'fresh_full_table_exactly_one_pair':True,'fixture':True}))
FA.joinpath('ROOT_NATIVE_MERGE_RECEIPT_20261004.json').write_text(json.dumps({'commit':start,'merged_at':utc,'fixture':True}))
native.R=FR; native.A=FA;native.AUTH=AUTH;native.STATUS=status;native.sourcepair=lambda:identity
base_tree={p:(FR/p).read_bytes() for p in [x['path'] for x in originals]+[native.QUEUE,native.STATE,native.HISTORY]}
trees={start:dict(base_tree)};head=start;remote=start;staged=set();commands=[]
def names0(xs):return b''.join(x.encode()+b'\0' for x in sorted(xs))
def capture_stub(label,argv,**kw):
 global head,remote
 commands.append(argv)
 if argv[0].endswith('gh'):
  out=json.dumps({'headRefOid':native.HEAD,'baseRefName':'main','state':'MERGED','mergeCommit':{'oid':start},'mergedAt':utc}).encode()
 else:
  q=argv[2:]
  if q[:2]==['branch','--show-current']:out=b'main\n'
  elif q[:2]==['rev-parse','HEAD']:out=(head+'\n').encode()
  elif q[:1]==['ls-remote']:out=(remote+'\trefs/heads/main\n').encode()
  elif q[:1]==['diff']:
   if '--cached' in q: out=names0(staged)
   elif '--binary' in q:out=b''
   elif len(q)>=5 and q[-2] in trees and q[-1] in trees:out=names0([p for p in set(trees[q[-2]])|set(trees[q[-1]]) if trees[q[-2]].get(p)!=trees[q[-1]].get(p)])
   else:out=names0([p for p,b in trees[head].items() if (FR/p).read_bytes()!=b])
  elif q[:1]==['ls-files']:
   paths=set(trees[head])|staged
   if '--stage' in q:out=b''.join(('100644 '+native.blob((FR/p).read_bytes() if p in staged else trees[head][p])+' 0\t'+p).encode()+b'\0' for p in sorted(paths))
   else:out=b''.join(('H '+p).encode()+b'\0' for p in sorted(paths))
  elif q[:1]==['show']:
   if q[1]=='-s':out=(start+'\n').encode()
   else:
    rev,path=q[1].split(':',1);out=(FR/path).read_bytes() if rev=='' else trees[rev][path]
  elif q[:1]==['ls-tree']:
   p=q[-1];entry=next(x for x in originals if x['path']==p);out=(entry['mode']+' blob '+entry['git_blob_sha1']+'\t'+p+'\n').encode()
  elif q[:1]==['add']:staged.update(q[2:]);out=b''
  elif q[:1]==['commit']:
   FR.joinpath(native.PREFIX+'/CURRENT_RESULT.md').write_text('CORRUPTED DURING COMMIT\n')
   foreign.write_text('FOREIGN CHANGED DURING COMMIT\n')
   trees[end]=dict(trees[head]);trees[end].update({p:(FR/p).read_bytes() for p in staged});staged.clear();head=end;out=b'fixture commit\n'
  elif q[:1]==['push']:remote=head;out=b'fixture push\n'
  else:raise RuntimeError('Unexpected synthetic command '+repr(q))
 return {'exit_code':0},out,b''
native.capture=capture_stub
oldargv=sys.argv;sys.argv=['native_integrate.py','accept','--plan',str(planpath),'--ack',str(ackpath),'--token',token]
stream=io.StringIO()
try:
 with contextlib.redirect_stdout(stream):native.main()
 successful=True;error=None
except Exception as e:successful=False;error=repr(e)
finally:sys.argv=oldargv
record('synthetic_native_accept_corruption',operator_returned_success=successful,error=error,printed_receipt=stream.getvalue(),CURRENT_RESULT_identical_to_prepared=(FR/(native.PREFIX+'/CURRENT_RESULT.md')).read_bytes()==prepared.joinpath('CURRENT_RESULT.md').read_bytes(),foreign_untracked_held_preserved=foreign.read_bytes()==b'HELD ORIGINAL\n',transport='All Git/GitHub simulated; sourcepair actual read-only tested separately; no network or Git process',command_count=len(commands))
O.joinpath('FIXTURE_RESULTS_V2.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'results':results},indent=2)+'\n')
print(json.dumps({'test_count':len(results),'last_test':results[-1]},indent=2))
