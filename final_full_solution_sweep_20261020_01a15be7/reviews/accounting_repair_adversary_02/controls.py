from pathlib import Path
import collections, copy, datetime as dt, hashlib, json, os, shutil, subprocess, sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
R=Path(__file__).resolve().parent
F=R/'fixtures/full_recursive_mount'
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def change(name,fn):
 p=F/name;d=json.loads(p.read_text());fn(d);save(p,d)
def state(fn):change('STATE.json',fn)
def repl(fn):change('PR0280_REOPENED_DISPOSITION.json',fn)
def proof(fn,pr=280):change(f'PR{pr:04d}_'+('REOPENED_' if pr==280 else '')+'PUBLICATION_VERIFICATION.json',fn)
def path_for(pr,kind):
 problem={292:'30001608',397:'9700002',399:'30001179',280:'30000156'}[pr]
 return f'audits/pr{pr:04d}_{problem}/'+{'ledger':'LEDGER_PUBLICATION_VERIFICATION.json','public':'ZENODO_PUBLIC_FILE_VERIFICATION.json'}[kind]
def nested(pr,kind,fn):change(path_for(pr,kind),fn)
def ordinary_entry(pr,fn):
 lines=[json.loads(x) for x in (F/'dispositions.jsonl').read_text().splitlines() if x.strip()]
 e=next(e for e in lines if e['pr']==pr);fn(e)
 save(F/f'PR{pr:04d}_DISPOSITION.json',e)
 (F/'dispositions.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in lines))

old=[
 ('baseline',lambda:None,False),
 ('alter_historical_hash',lambda:state(lambda d:d['reopened_disposition_overrides'][0].update(historical_disposition_sha256='0'*64)),True),
 ('duplicate_override',lambda:state(lambda d:d['reopened_disposition_overrides'].append(copy.deepcopy(d['reopened_disposition_overrides'][0]))),True),
 ('duplicate_doi',lambda:state(lambda d:d['completed_publications'][0].update(doi=d['completed_publications'][1]['doi'])),True),
 ('publication_flag_false',lambda:proof(lambda d:d.update(published=False)),True),
 ('wrong_completed_doi',lambda:state(lambda d:d['completed_publications'][3].update(doi='10.5281/zenodo.99999999')),True),
 ('publication_row_mismatch',lambda:proof(lambda d:d.update(ledger_row=179)),True),
 ('wrong_replacement_pr',lambda:repl(lambda d:d.update(pr=999)),True),
 ('wrong_publication_pr',lambda:proof(lambda d:d.update(pr=999)),True),
 ('wrong_replacement_row',lambda:repl(lambda d:d.update(ledger_row=179)),True),
 ('wrong_completed_verification_path',lambda:state(lambda d:d['completed_publications'][3].update(verification='PR0292_PUBLICATION_VERIFICATION.json')),True),
 ('wrong_completed_record',lambda:state(lambda d:d['completed_publications'][3].update(record=23524971)),True),
 ('wrong_completed_problem',lambda:state(lambda d:d['completed_publications'][3].update(problem_id='30001608')),True),
 ('wrong_replacement_problem',lambda:repl(lambda d:d.update(problem_ids=['30001608'])),True),
 ('wrong_publication_record',lambda:proof(lambda d:d.update(record=23524971)),True),
 ('missing_public_files',lambda:proof(lambda d:d.update(files=[])),True),
 ('ordinary_wrong_completed_doi',lambda:state(lambda d:d['completed_publications'][0].update(doi='10.5281/zenodo.99999999')),True),
 ('ordinary_wrong_completed_pr',lambda:state(lambda d:d['completed_publications'][0].update(pr=293)),True),
 ('duplicate_completed_pr_new_doi',lambda:state(lambda d:d['completed_publications'].append(dict(d['completed_publications'][0],doi='10.5281/zenodo.99999999'))),True),
 ('unbound_extra_publication',lambda:state(lambda d:d['completed_publications'].append(dict(d['completed_publications'][0],pr=999,doi='10.5281/zenodo.99999999'))),True),
 ('noncanonical_original_verification_for_292',lambda:state(lambda d:d['completed_publications'][0].update(verification='PR0397_PUBLICATION_VERIFICATION.json')),True),
]
new=[('current_baseline',lambda:None,False)]
for field in ['pr','record','ledger_row','problem_id','merge_commit','doi','verification']:
 for val in [None,True,False,0,1.0,[],{},'']:
  new.append((f'type_completed_{field}_{type(val).__name__}_{str(val).replace(" ","")}',lambda field=field,val=val:state(lambda d:d['completed_publications'][0].update({field:val})),True))
for doi in ['https://doi.org/10.5281/zenodo.23524971','10.5281/zenodo.023524971','10.5281/Zenodo.23524971','10.5281/zenodo.23524971?x=1','10.5281/zenodo.23524971#x','10.5281/zenodo.23524971/']:
 new.append(('doi_alias_'+str(len(new)),lambda doi=doi:state(lambda d:d['completed_publications'][0].update(doi=doi)),True))
for field in ['pr','record','ledger_row','problem_id']:
 new.append(('duplicate_completed_'+field,lambda field=field:state(lambda d:d['completed_publications'][1].update({field:d['completed_publications'][0][field]})),True))
for pr in [292,397,399,280]:
 new.extend([
 (f'absent_completed_{pr}',lambda pr=pr:state(lambda d:d.update(completed_publications=[e for e in d['completed_publications'] if e['pr']!=pr])),True),
 (f'proof_pr_string_{pr}',lambda pr=pr:proof(lambda d:d.update(pr=str(pr)),pr),True),
 (f'proof_record_float_{pr}',lambda pr=pr:proof(lambda d:d.update(record=float(d['record'])),pr),True),
 (f'proof_missing_{pr}',lambda pr=pr:(F/(f'PR{pr:04d}_'+('REOPENED_' if pr==280 else '')+'PUBLICATION_VERIFICATION.json')).unlink(),True),
 (f'ledger_missing_{pr}',lambda pr=pr:(F/path_for(pr,'ledger')).unlink(),True),
 (f'ledger_wrong_pr_{pr}',lambda pr=pr:nested(pr,'ledger',lambda d:d.update(pr=999)),True),
 (f'ledger_wrong_row_{pr}',lambda pr=pr:nested(pr,'ledger',lambda d:d.update(row_number=179)),True),
 (f'ledger_false_exact_{pr}',lambda pr=pr:nested(pr,'ledger',lambda d:d.update(read_back_exact=False)),True),
 (f'ledger_missing_values_{pr}',lambda pr=pr:nested(pr,'ledger',lambda d:d.pop('values')),True),
 (f'ledger_wrong_actual_doi_{pr}',lambda pr=pr:nested(pr,'ledger',lambda d:d['values'].__setitem__(2,'https://doi.org/10.5281/zenodo.99999999')),True),
 (f'ledger_wrong_sheet_{pr}',lambda pr=pr:nested(pr,'ledger',lambda d:d.update(spreadsheet_id='another-spreadsheet')),True),
 (f'proof_missing_pdf_{pr}',lambda pr=pr:proof(lambda d:d.update(files=[x for x in d['files'] if not x['name'].endswith('.pdf')]),pr),True),
 (f'proof_missing_zip_{pr}',lambda pr=pr:proof(lambda d:d.update(files=[x for x in d['files'] if not x['name'].endswith('.zip')]),pr),True),
 (f'proof_bad_sha_{pr}',lambda pr=pr:proof(lambda d:d['files'][0].update(sha256='x'*64),pr),True),
 ])
for pr in [397,399,280]:
 new.extend([
 (f'public_missing_{pr}',lambda pr=pr:(F/path_for(pr,'public')).unlink(),True),
 (f'public_wrong_record_{pr}',lambda pr=pr:nested(pr,'public',lambda d:d.update(record=99999999)),True),
 (f'public_wrong_hash_{pr}',lambda pr=pr:nested(pr,'public',lambda d:d['files'][0].update(sha256='0'*64)),True),
 (f'public_false_metadata_{pr}',lambda pr=pr:nested(pr,'public',lambda d:d.update(all_intended_authenticated_and_public_metadata_verified=False)),True),
 (f'public_no_metadata_{pr}',lambda pr=pr:nested(pr,'public',lambda d:[d.pop(k,None) for k in ['all_intended_authenticated_and_public_metadata_verified','all_intended_metadata_verified_by_existing_tool']]),True),
 (f'public_bad_manifest_{pr}',lambda pr=pr:nested(pr,'public',lambda d:d['files'][1].update(all_manifest_payloads_verified=0)),True),
 ])

def downgrade(pr):
 def edit(d):
  d['evidence'].pop('public_files')
  d['reviewed_hashes']={('pdf' if f['name'].endswith('.pdf') else 'zip'):f['sha256'] for f in d['files']}
 proof(edit,pr)
 (F/path_for(pr,'public')).unlink()
for pr in [397,399,280]:new.append((f'modern_silent_legacy_fallback_{pr}',lambda pr=pr:downgrade(pr),True))
def contradict_legacy(pr=292):
 def edit(d):
  d['files'][0].update(downloaded_and_matches_reviewed=False,http_status=404)
 proof(edit,pr)
new.extend([
 ('legacy_conflicting_negative_download_evidence',contradict_legacy,True),
 ('legacy_zip_missing_manifest_member',lambda:proof(lambda d:d['files'][0].update(members=['arbitrary/a','arbitrary/b']),292),True),
 ('ordinary_effective_not_published_but_listed',lambda:ordinary_entry(292,lambda d:d.update(disposition='skip_priority_gate_not_met')),True),
 ('ordinary_effective_missing_new_publication',lambda:ordinary_entry(292,lambda d:d.pop('new_publication')),True),
 ('ordinary_effective_wrong_problem',lambda:ordinary_entry(292,lambda d:d.update(problem_ids=['30000156'])),True),
 ('ordinary_effective_wrong_merge',lambda:ordinary_entry(292,lambda d:d.update(merge_commit='0'*40)),True),
 ('ordinary_effective_pr_float',lambda:ordinary_entry(292,lambda d:d.update(pr=292.0)),True),
 ('reopened_replacement_pr_float',lambda:repl(lambda d:d.update(pr=280.0)),True),
 ('reopened_override_pr_float',lambda:state(lambda d:d['reopened_disposition_overrides'][0].update(pr=280.0)),True),
 ('reopened_ordinary_verification_path',lambda:repl(lambda d:d.update(publication_evidence='PR0280_PUBLICATION_VERIFICATION.json')),True),
 ('reopened_override_absent',lambda:state(lambda d:d.update(reopened_disposition_overrides=[])),True),
 ('completed_order_permutation',lambda:state(lambda d:d['completed_publications'].reverse()),False),
])
for p in ['../coverage_snapshot.py','/tmp/nonexistent.json','./PR0292_PUBLICATION_VERIFICATION.json','audits//pr0292_30001608/LEDGER_PUBLICATION_VERIFICATION.json','audits/../PR0292_PUBLICATION_VERIFICATION.json']:
 new.append(('completed_unsafe_path_'+str(len(new)),lambda p=p:state(lambda d:d['completed_publications'][0].update(verification=p)),True))
def symlink_file():
 p=F/'PR0292_PUBLICATION_VERIFICATION.json';target=R/'fixtures/review_local_external_proof.json';target.write_bytes(p.read_bytes());p.unlink();p.symlink_to(target)
def symlink_dir():
 p=F/'audits/pr0397_9700002';target=R/'fixtures/review_local_external_audit';shutil.copytree(p,target,dirs_exist_ok=True);shutil.rmtree(p);p.symlink_to(target,target_is_directory=True)
new.extend([('canonical_proof_symlink',symlink_file,True),('canonical_audit_directory_symlink',symlink_dir,True)])

results=[]
for group,source,cases in [('historical21','pre_repair',old),('fresh','current',new)]:
 for name,mutate,reject in cases:
  if F.exists():shutil.rmtree(F)
  shutil.copytree(R/'inputs'/source,F)
  shutil.copyfile(R/'inputs/current/coverage_snapshot.py',F/'coverage_snapshot.py')
  before={str(p.relative_to(F)):(p.read_bytes(),False) for p in F.rglob('*') if p.is_file()}
  mutate()
  changes=[]
  for rel,(b,_) in before.items():
   p=F/rel
   if not p.exists():changes.append(dict(path=rel,operation='deleted',before_sha256=sha(b)));continue
   if p.is_symlink() or any(a.is_symlink() for a in p.parents if a.is_relative_to(F)):
    changes.append(dict(path=rel,operation='symlink',before_sha256=sha(b),resolved_path=str(p.resolve())))
   elif p.read_bytes()!=b:
    data=p.read_bytes();changes.append(dict(path=rel,operation='changed',before_sha256=sha(b),after_sha256=sha(data),after_text=data.decode()))
  case_dir=R/'cases'/group/name
  save(case_dir/'MUTATIONS.json',changes)
  for mode,flags in [('normal',[]),('optimized',['-O'])]:
   p=subprocess.run([sys.executable,'-B',*flags,str(F/'coverage_snapshot.py')],cwd=R,env=os.environ,capture_output=True)
   (case_dir/(mode+'.stdout')).write_bytes(p.stdout);(case_dir/(mode+'.stderr')).write_bytes(p.stderr)
   accepted=p.returncode==0
   result=dict(group=group,name=name,mode=mode,expected_reject=reject,accepted=accepted,control_pass=accepted!=reject,returncode=p.returncode,stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr),mutations=str((case_dir/'MUTATIONS.json').relative_to(R)))
   if accepted:
    v=json.loads(p.stdout);result.update(published=v['disposition_counts'].get('published_verified_full_solution'),next_pr=v['next_pr'])
   else:result['error_tail']=p.stderr.decode().splitlines()[-1] if p.stderr else ''
   results.append(result)
save(R/'CONTROL_RESULTS.json',dict(at=now(),results=results))
summary=dict(at=now(),by_group_mode={},false_accepts=[{k:r[k] for k in ['group','name','mode']} for r in results if r['accepted'] and r['expected_reject']])
for group in ['historical21','fresh']:
 for mode in ['normal','optimized']:
  rs=[r for r in results if r['group']==group and r['mode']==mode]
  summary['by_group_mode'][group+'_'+mode]=dict(cases=len(rs),passed=sum(r['control_pass'] for r in rs),false_accepts=sum(r['accepted'] and r['expected_reject'] for r in rs),false_rejects=sum(not r['accepted'] and not r['expected_reject'] for r in rs))
save(R/'CONTROL_SUMMARY.json',summary)
print(json.dumps(summary,indent=2))
