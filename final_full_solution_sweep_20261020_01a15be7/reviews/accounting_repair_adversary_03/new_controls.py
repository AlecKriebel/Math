from pathlib import Path
import copy, datetime as dt, hashlib, json, os, shutil, subprocess, sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE="1",GIT_OPTIONAL_LOCKS="0")
R=Path(__file__).resolve().parent
F=R/"fixtures/new_controls"
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+"\n")
def change(p,fn):
 p=F/p;d=json.loads(p.read_text());fn(d);save(p,d)
def s(fn):change("STATE.json",fn)
def proofpath(pr):return f"PR{pr:04d}_"+("REOPENED_" if pr==280 else "")+"PUBLICATION_VERIFICATION.json"
def proof(pr,fn):change(proofpath(pr),fn)
def receiptpath(pr,kind):
 return f"audits/pr{pr:04d}_{ {292:'30001608',397:'9700002',399:'30001179',280:'30000156'}[pr]}/"+{"ledger":"LEDGER_PUBLICATION_VERIFICATION.json","public":"ZENODO_PUBLIC_FILE_VERIFICATION.json"}[kind]
def nested(pr,kind,fn):change(receiptpath(pr,kind),fn)
def both(pr,fn):proof(pr,fn);nested(pr,"public",fn)
def resolution(pr,kind,fn):
 (proof(pr,lambda d:fn(d["doi_resolution"])) if kind=="root" else nested(pr,"public",lambda d:fn(d["doi_resolution"])))
def legacy_archive(d):
 f=next(f for f in d['files'] if f['name'].endswith('.zip'))
 f['size']=f.pop('bytes');f['checksum']='md5:'+f.pop('md5')
 for k in ['http_status','downloaded_and_matches_reviewed','zip_crc_safe_unique_pass','all_manifest_payloads_verified']:f.pop(k,None)
 f.update(download_verified=True,zip_crc_ok=True,members=['arbitrary/a','arbitrary/b'])
def alias(pr):
 def edit(d):
  f=next(f for f in d['files'] if f['name'].endswith('.zip'))
  f.update(zip_crc_ok=False)
 proof(pr,edit)
def wrong_range(pr,kind):
 def edit(d):
  row=d['row_number'];d['range']=("'Wrong Sheet'!" if kind=='sheet' else "'Math Puzzles'!")+f"A{row+(kind=='row')}:D{row+(kind=='row')}"
 nested(pr,'ledger',edit)
def wrong_pr_link(pr):
 nested(pr,'ledger',lambda d:d['values'].__setitem__(3,d['values'][3].replace('/pull/'+str(pr),'/pull/'+str(pr)+'evil')))
def wrong_record_link(pr):
 record={292:23524971,397:23527793,399:23539283,280:23539734}[pr]
 nested(pr,'ledger',lambda d:d['values'].__setitem__(3,d['values'][3].replace('/records/'+str(record),'/records/99999999')))
cases=[('current_baseline',lambda:None,False,'baseline'),('completed_permutation',lambda:s(lambda d:d['completed_publications'].reverse()),False,'positive')]
for pr in [397,399,280]:
 cases.extend([
  (f'modern_archive_legacy_schema_without_manifest_{pr}',lambda pr=pr:both(pr,legacy_archive),True,'legacy_manifest'),
  (f'modern_explicit_negative_legacy_crc_{pr}',lambda pr=pr:alias(pr),True,'negative_crc'),
  (f'public_order_permutation_{pr}',lambda pr=pr:nested(pr,'public',lambda d:d['files'].reverse()),False,'positive'),
  (f'modern_zip_manifest_count_mismatch_{pr}',lambda pr=pr:proof(pr,lambda d:next(f for f in d['files'] if f['name'].endswith('.zip')).update(members=3,all_manifest_payloads_verified=2)),True,'manifest_count'),
 ])
 for kind in ['root','public']:
  for field,value in [('status',404),('http_status',404),('resolved_url','https://zenodo.org/record/99999999'),('url','https://doi.org/10.5281/zenodo.99999999'),('expected_record',99999999),('exact_expected_record_destination_verified',False),('destination_verified',dict(record=99999999,status=200,resolved_url='https://zenodo.org/records/99999999'))]:
   cases.append((f'resolution_{kind}_{field}_{pr}',lambda pr=pr,kind=kind,field=field,value=value:resolution(pr,kind,lambda d:d.update({field:value})),True,'destination'))
for pr in [292,397,399,280]:
 for kind in ['row','sheet']:
  cases.append((f'ledger_range_wrong_{kind}_{pr}',lambda pr=pr,kind=kind:wrong_range(pr,kind),True,'ledger_range'))
 cases.extend([
  (f'ledger_nonexistent_pr_url_suffix_{pr}',lambda pr=pr:wrong_pr_link(pr),True,'ledger_pr_url'),
  (f'ledger_wrong_record_url_{pr}',lambda pr=pr:wrong_record_link(pr),True,'ledger_record_url'),
  (f'ledger_doi_bare_positive_{pr}',lambda pr=pr:nested(pr,'ledger',lambda d:d['values'].__setitem__(2,d['doi'])),False,'positive'),
  (f'ledger_problem_longer_integer_{pr}',lambda pr=pr:nested(pr,'ledger',lambda d:d['values'].__setitem__(0,d['values'][0].replace({292:'30001608',397:'9700002',399:'30001179',280:'30000156'}[pr],{292:'30001608',397:'9700002',399:'30001179',280:'30000156'}[pr]+'0'))),True,'ledger_source'),
 ])
# Pin qualification must reject even semantically innocuous rewriting of historical receipt bytes.
def legacy_whitespace():
 p=F/proofpath(292);p.write_bytes(p.read_bytes()+b'\n')
cases.append(('historical_legacy_pin_whitespace',legacy_whitespace,True,'legacy_pin'))
def legacy_add_public_without_manifest():
 p=F/proofpath(292);d=json.loads(p.read_text());next(f for f in d['files'] if f['name'].endswith('.zip'))['members']=['arbitrary/a','arbitrary/b']
 d['evidence']['public_files']=receiptpath(292,'public');save(p,d)
 payload={k:copy.deepcopy(d[k]) for k in ['pr','record','doi','doi_url','title','files','doi_resolution']}
 payload.update(all_public_file_bytes_match_reviewed=True,all_intended_authenticated_and_public_metadata_verified=True,record_http_status=200)
 save(F/receiptpath(292,'public'),payload)
cases.append(('historical_pin_avoided_by_injected_public_receipt',legacy_add_public_without_manifest,True,'legacy_manifest'))
for field,value in [('path','PR0397_DISPOSITION.json'),('sha256','0'*64),('old_disposition','published_verified_full_solution')]:
 cases.append(('root_historical_preserved_wrong_'+field,lambda field=field,value=value:proof(280,lambda d:d['historical_ordered_disposition_preserved'].update({field:value})),True,'historical_declaration'))
for name,fn in [('absent_historical_hash',lambda d:d.pop('historical_disposition_sha256')),('wrong_replacement_path',lambda d:d.update(replacement_disposition='../PR0280_REOPENED_DISPOSITION.json')),('wrong_override_pr',lambda d:d.update(pr='280'))]:
 cases.append((name,lambda fn=fn:s(lambda d:fn(d['reopened_disposition_overrides'][0])),True,'override'))
for pr in [397,399,280]:
 for kind in ['ledger','public']:
  def symlink(pr=pr,kind=kind):
   p=F/receiptpath(pr,kind);target=R/'fixtures/external'/f'{pr}_{kind}.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());p.unlink();p.symlink_to(target)
  cases.append((f'symlink_{kind}_{pr}',symlink,True,'unsafe_evidence'))
for n in ['duplicate_public_filename','missing_public_receipt','duplicate_inventory','inventory_float']:
 def fn(n=n):
  if n=='duplicate_public_filename':both(399,lambda d:d['files'].append(copy.deepcopy(d['files'][0])))
  elif n=='missing_public_receipt':(F/receiptpath(399,'public')).unlink()
  elif n=='duplicate_inventory':change('rest_inventory.json',lambda d:d['pull_requests'].append(copy.deepcopy(d['pull_requests'][0])))
  else:change('rest_inventory.json',lambda d:d['pull_requests'][0].update(number=float(d['pull_requests'][0]['number'])))
 cases.append((n,fn,True,'identity_safety'))
# Representation probes are retained separately without asserting they violate this validator's stated contract.
for name,fn in [('state_last_processed_float',lambda:s(lambda d:d.update(last_completely_processed_pr=float(d['last_completely_processed_pr'])))),('state_completed_count_float',lambda:s(lambda d:d.update(completed_pr_count=float(d['completed_pr_count'])))),('inventory_gap_float',lambda:change('rest_inventory.json',lambda d:d.update(numeric_gaps=[float(x) for x in d['numeric_gaps']]))),('modern_public_backslash_name',lambda:both(399,lambda d:d['files'][0].update(name='..\\unsafe.pdf'))),('modern_public_nul_name',lambda:both(399,lambda d:d['files'][0].update(name='unsafe\x00.pdf')))]:
 cases.append((name,fn,None,'scope_probe'))
results=[]
for name,mutate,reject,family in cases:
 if F.exists():shutil.rmtree(F)
 shutil.copytree(R/'inputs/current',F)
 before={str(p.relative_to(F)):p.read_bytes() for p in F.rglob('*') if p.is_file()}
 mutate();c=R/'new_cases'/name;changes=[]
 afterfiles={str(p.relative_to(F)):p for p in F.rglob('*') if p.is_file()}
 for rel in sorted(set(before)|set(afterfiles)):
  p=F/rel;b=before.get(rel)
  if not p.exists():changes.append(dict(path=rel,operation='deleted',before_sha256=sha(b)));continue
  a=p.read_bytes()
  if p.is_symlink():changes.append(dict(path=rel,operation='symlink',target=str(p.resolve()),before_sha256=sha(b),after_sha256=sha(a)))
  elif b!=a:changes.append(dict(path=rel,operation='created' if b is None else 'changed',before_sha256=sha(b) if b else None,after_sha256=sha(a),after_text=a.decode()))
 save(c/'MUTATIONS.json',changes)
 for mode,flags in [('normal',[]),('optimized',['-O'])]:
  p=subprocess.run([sys.executable,'-B',*flags,str(F/'coverage_snapshot.py')],cwd=R,env=os.environ,capture_output=True)
  (c/(mode+'.stdout')).write_bytes(p.stdout);(c/(mode+'.stderr')).write_bytes(p.stderr)
  result=dict(name=name,family=family,mode=mode,expected_reject=reject,accepted=p.returncode==0,returncode=p.returncode,stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr),mutations=str((c/'MUTATIONS.json').relative_to(R)))
  if reject is not None:result['control_pass']=(result['accepted']!=reject)
  if p.returncode:result['error_tail']=p.stderr.decode().splitlines()[-1] if p.stderr else None
  else:result.update(published=json.loads(p.stdout)['disposition_counts'].get('published_verified_full_solution'))
  results.append(result)
save(R/'NEW_CONTROL_RESULTS.json',dict(at=now(),results=results))
summary=dict(at=now(),cases_per_mode=len(cases),by_mode={},failures=[])
for mode in ['normal','optimized']:
 rs=[r for r in results if r['mode']==mode];known=[r for r in rs if r['expected_reject'] is not None]
 summary['by_mode'][mode]=dict(total=len(rs),asserted_controls=len(known),passed=sum(r['control_pass'] for r in known),false_accepts=sum(r['accepted'] and r['expected_reject'] for r in known),false_rejects=sum(not r['accepted'] and not r['expected_reject'] for r in known),scope_probes=sum(r['expected_reject'] is None for r in rs))
summary['failures']=[dict(name=r['name'],family=r['family'],mode=r['mode']) for r in results if r.get('control_pass') is False]
save(R/'NEW_CONTROL_SUMMARY.json',summary)
print(json.dumps(summary,indent=2))
