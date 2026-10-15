#!/usr/bin/env python3
"""Root replay of the fresh source-first arrangement audit; queue gate separate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,shutil,subprocess,itertools,sys
A=Path(__file__).resolve().parent
D=A/'clean_final_adversary'
PY=A/'sources_effective_review/private_runtime/bin/python'
W=A/'tmp/root_clean_math'
resume=sys.argv[1:]==['--resume-validated-controls']
assert not sys.argv[1:] or resume
if not resume:
 assert not W.exists()
 W.mkdir(parents=True);(W/'streams').mkdir()
else:assert W.is_dir()
def sha(b):return hashlib.sha256(b).hexdigest()
mf=json.loads((D/'FINAL_AUDIT_MANIFEST.json').read_text())
before={}
for e in mf['files']:
 p=D/e['path'];b=p.read_bytes()
 assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
 before[str(p)]=sha(b)
seals=[]
for line in (D/'initial_seal_sha256.txt').read_text().splitlines():
 wanted,name=line.split(None,1);b=(D/name.strip()).read_bytes()
 assert sha(b)==wanted,name
 seals.append({'path':name.strip(),'sha256':wanted})
assert sha((D/'initial_seal_sha256.txt').read_bytes())==mf['initial_seal_sha256']
assert sha((A/'snapshot_manifest.json').read_bytes())==mf['snapshot_manifest_sha256']
for e in json.loads((D/'source_credit_receipt.json').read_text())['own_primary_pdf_matches']:
 b=(D/e['path']).read_bytes()
 assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
streams=[]
for i in range(1,6):streams.append((f'root_original_check_turn_{i}.stdout',f'streams/author_turn_{i}.stdout.txt'))
streams += [('root_original_REPLAY_ALL.stdout','streams/author_wrapper.stdout.txt'),
            ('root_original_review_independent_checks.stdout','streams/old_independent.stdout.txt'),
            ('root_original_review_verify_review.stdout','streams/review_wrapper.stdout.txt'),
            ('cover_duality_review/exact_fermat_check.stdout.txt','streams/extension_fermat.stdout.txt'),
            ('cover_duality_review/exact_subfamily_check.stdout.txt','streams/extension_subfamily.stdout.txt')]
matches=[]
for p,q in streams:
 b=(A/p).read_bytes();assert b==(D/q).read_bytes(),q
 matches.append({'root_actual_stream':p,'family_stream':q,'bytes':len(b),'sha256':sha(b)})
records=[]
for label,script,expected in [
 ('baseline','independent_controls.py','initial_controls_full.json'),
 ('new_extension','new_extension_controls.py','streams/new_extension_controls.stdout.txt')]:
 if not resume:
  shutil.copyfile(D/script,W/script)
  p=subprocess.run([str(PY),'-B',str(W/script)],cwd=W,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True)
  (A/f'root_clean_{label}.stdout').write_bytes(p.stdout);(A/f'root_clean_{label}.stderr').write_bytes(p.stderr)
  assert p.returncode==0 and not p.stderr,(label,p.stderr.decode())
 else:assert (W/script).read_bytes()==(D/script).read_bytes()
 output=(A/f'root_clean_{label}.stdout').read_bytes()
 assert not (A/f'root_clean_{label}.stderr').read_bytes()
 assert output==(D/expected).read_bytes(),label
 records.append({'label':label,'stdout_bytes':len(output),'stdout_sha256':sha(output),'full_stream_byte_exact':True})
 print(label+': PASS',flush=True)
incidence=[]
for q in [1,2,4]:
 own=(W/f'streams/new_q{q}_all_line_incidence.json').read_bytes()
 original=(D/f'streams/new_q{q}_all_line_incidence.json').read_bytes()
 a,b=json.loads(own),json.loads(original)
 assert a['n']==b['n'] and a['point_kinds']==b['point_kinds']
 N=len(a['point_kinds']);assert a['point_kinds'][-3:]==['vertex']*3
 def canonical(records,mapping):
  values=[]
  for r in records:
   assert len(set(r['representative_pair']))==2 and set(r['representative_pair'])<=set(r['support'])
   values.append((tuple(sorted(mapping[i] for i in r['support'])),r['class'],r['dual_load']))
  return sorted(values)
 expected=canonical(b['records'],list(range(N)))
 candidates=[]
 for permutation in itertools.permutations(range(N-3,N)):
  mapping=list(range(N-3))+list(permutation)
  if canonical(a['records'],mapping)==expected:candidates.append(list(permutation))
 assert candidates,'Incidences differ beyond relabeling three unordered coordinate vertices'
 # Preserve actual root-generated incidence bytes, not only a checksum or summary.
 (A/f'root_clean_q{q}_all_line_incidence.json').write_bytes(own)
 incidence.append({'q':q,'root_sha256':sha(own),'original_sha256':sha(original),
                   'raw_byte_exact':own==original,'only_unordered_vertex_labels_differ':True,
                   'valid_vertex_permutations':candidates,'complete_supports_class_and_loads_equal':True,
                   'representative_pairs_checked_in_support':True,'records':len(a['records'])})
p=subprocess.run([str(PY),'-B',str(D/'verify_git_history.py')],capture_output=True)
(A/'root_clean_git_history.stdout').write_bytes(p.stdout);(A/'root_clean_git_history.stderr').write_bytes(p.stderr)
assert p.returncode==0 and not p.stderr
actual=json.loads(p.stdout);expected=json.loads((D/'git_history_full.json').read_text())
actual.pop('utc');expected.pop('utc');assert actual==expected
assert all(sha(Path(p).read_bytes())==h for p,h in before.items()),'Original reviewer artifacts changed'
receipt={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'workflow_percent':90,
         'scope':'Fresh mathematical/extension/initial Git/source evidence root gate; repaired-head/queue and final manifest gates pending',
         'public_binding_count':len(mf['files']),'initial_seal_instances':len(seals),
         'initial_seals':seals,'root_prior_full_stream_matches':matches,'new_runs':records,
         'full_incidence_reconciliation':incidence,
         'root_initial_harness_error':'Required byte equality despite unordered three-vertex set labels; preserved first script, reconciled all records and saved actual root outputs without rerunning successful controls',
         'git_history_full_receipt_equal_except_utc':True,'existing_git_objects':actual,
         'separate_fresh_PDF_identities':4,'public_source_wrapper_count':0,
         'baseline_own_erratum':'Exponent-one Fermat arrangement concurrent; sealed original retained',
         'original_problem_resolution_percent':0,'original_problem_status':'unsolved',
         'original_family_artifacts_unchanged':True}
(A/'root_clean_mathematical_reproduction_receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','public_bindings':len(mf['files']),'initial_seals':len(seals),'complete_prior_streams':len(matches),'new_programs':len(records)},sort_keys=True))
