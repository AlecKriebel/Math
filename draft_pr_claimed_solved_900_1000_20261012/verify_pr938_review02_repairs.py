#!/usr/bin/env python3
"""Offline canonical-round/evidence/title regressions. No operational main."""
import copy,hashlib,importlib.util,json,shutil,sys,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent;A=P/'audits/pr938_30003634';D=A/'publication'
SEALS={1:'37feff8cb31bbef2b7f41b98d8f34571923e7a89cb4c8f53226ccd2adf388a91',2:'36a69cb090d28f33be92963bcf7a62ed2ce756d653c44f07d2f37cb468290716'}
TITLE='Mini-Workshop: Interactions between Low-dimensional Topology and Complex Algebraic Geometry'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def rejects(fn,*args):
 try:fn(*args)
 except (RuntimeError,ValueError,KeyError,TypeError,UnicodeError):return True
 return False
def main():
 spec=importlib.util.spec_from_file_location('acceptance_evidence_regression',P/'accept_pr938.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 valid=[]
 for number,pin in SEALS.items():
  folder=A/'reviews'/f'full_package_{number:02d}';need(m.fp(folder/'MANIFEST.json')['sha256']==pin,'External settled review changed');mapping=m.load(folder/'MANIFEST.json');m.authenticate_review_records(folder,mapping);base=D/'reviewed_candidates'/f'candidate{number:02d}';m.validate_review_evidence(folder,m.load(folder/'RESULT.json'),m.load(base/'PREPUBLICATION_FREEZE.json'),base);valid.append(number)
 pin='a'*64;m.validate_review_sequence(['01:'+pin,'02:'+pin])
 bad_rounds=[['001:'+pin,'002:'+pin],['1:'+pin,'2:'+pin],['٠١:'+pin,'٠٢:'+pin],['01:'+pin,'003:'+pin],['01:'+pin,'03:'+pin]]
 need(all(rejects(m.validate_review_sequence,x) for x in bad_rounds),'R4 noncanonical/skipped rounds accepted')
 source=A/'reviews/full_package_01';original=m.load(source/'MANIFEST.json');result=m.load(source/'RESULT.json');base=D/'reviewed_candidates/candidate01';freeze=m.load(base/'PREPUBLICATION_FREEZE.json');scratch=A/'private/review02_repairs';scratch.mkdir(parents=True,exist_ok=True);cases=[]
 def test(label,filename,change,raw=False):
  with tempfile.TemporaryDirectory(dir=scratch) as td:
   folder=Path(td);mapping=copy.deepcopy(original)
   for name in mapping['files']:
    q=folder/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/name,q)
   q=folder/filename
   if raw:q.write_bytes(change)
   else:
    value=m.load(q);change(value);q.write_text(json.dumps(value,indent=2)+'\n')
   mapping['files'][filename]=m.fp(q) # Even a newly rebound fixture map cannot bless inconsistent evidence.
   def actual_gate():
    m.authenticate_review_records(folder,mapping);m.validate_review_evidence(folder,result,freeze,base)
   need(rejects(actual_gate),'R5 bad evidence accepted: '+label);cases.append(label)
 for filename in ['FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json']:
  test('empty_'+filename,filename,b'',True);test('whitespace_'+filename,filename,b' \n\t',True)
 test('cross_head','AUTHENTICATION_START.json',lambda x:x.update(original_pr_head='0'*40))
 test('stale_freeze','AUTHENTICATION_START.json',lambda x:x.update(freeze_sha256='0'*64))
 test('stale_manifest','AUTHENTICATION_START.json',lambda x:x.update(package_manifest_sha256='0'*64))
 test('contradictory_alias','AUTHENTICATION_START.json',lambda x:x.update(manifest_sha256='0'*64))
 test('missing_original','AUTHENTICATION_START.json',lambda x:x['originals'].pop(next(iter(x['originals']))))
 test('wrong_original_mode','AUTHENTICATION_START.json',lambda x:next(iter(x['originals'].values())).update(git_mode='100755'))
 test('bool_original_size','AUTHENTICATION_START.json',lambda x:next(iter(x['originals'].values())).update(bytes=True))
 test('failed_endpoint','AUTHENTICATION_END.json',lambda x:x.update(status='FAIL'))
 test('wrong_endpoint_time','AUTHENTICATION_END.json',lambda x:x.update(utc='2000-01-01T00:00:00+00:00'))
 test('failed_cold','COLD_REPLAY.json',lambda x:x.update(status='FAIL'))
 test('stale_cold_verifier','COLD_REPLAY.json',lambda x:x.update(externally_pinned_verifier_sha256='0'*64))
 test('no_fresh_extraction','COLD_REPLAY.json',lambda x:x.update(cold_extraction=False))
 test('missing_outer_mode','COLD_REPLAY.json',lambda x:x['modes'].pop())
 test('float_optimization','COLD_REPLAY.json',lambda x:x['modes'][1].update(observed_outer_optimization=1.0))
 test('failed_finite_receipt','COLD_REPLAY.json',lambda x:x['modes'][0]['receipt'].update(status='FAIL'))
 test('wrong_worker_guard','COLD_REPLAY.json',lambda x:x['modes'][0]['receipt']['child_execution_guards'][0].update(isolated=0))
 for bad in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}']:need(rejects(m.strict_json,bad),'R5 duplicate/nonfinite JSON accepted')
 text=(D/'note.tex').read_text();generator=(D/'prepare_metadata.py').read_text();descriptor=m.load(D/'zenodo-deposit.json')
 need(TITLE in text and TITLE in generator and any(TITLE in r for r in descriptor['metadata']['references']),'O3 actual title not corrected globally')
 need('Knot Theory' not in text and 'Knot Theory' not in generator and not any('Knot Theory' in r for r in descriptor['metadata']['references']),'O3 current wrong title remains')
 print(json.dumps({'status':'PASS','actual_parent_optimization':sys.flags.optimize,'genuine_historical_reviews_pass':valid,'R4_bad_alias_or_skip_sequences_rejected':len(bad_rounds),'R5_rebound_inconsistent_evidence_cases_rejected':len(cases),'R5_duplicate_nonfinite_JSON_cases_rejected':3,'evidence_cases':cases,'O3_current_note_generator_and_descriptor_title_correct':True,'no_operational_main_or_remote_action':True,'scope':'Recorded schema/provenance consistency only; not certification of actual historical execution, reviewer independence, mathematics or priority.'},indent=2))
if __name__=='__main__':main()
