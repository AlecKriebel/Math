"""PR204 local gate validation and durable records; imports perform no operations."""
import sys
sys.dont_write_bytecode=True
import datetime,hashlib,json,os,pathlib,stat

PR=204
PROBLEM=5100012
PREFIX='draft_pr_publication_program_20260930/audits/pr204_5100012/'
UPLOADS={'centered_pedal_dn.pdf','centered_pedal_dn.tex','verification-package.zip'}
KIT_SHA='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'

def require(ok,message):
 if not ok:raise RuntimeError(message)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def encoded(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def pin(path):
 raw=path.read_bytes();return dict(bytes=len(raw),sha256=digest(raw))
def reject_constant(value):raise RuntimeError('Nonfinite JSON value')
def read(path):return json.loads(path.read_text(),parse_constant=reject_constant)
def child(root,relative):
 require(isinstance(relative,str) and relative and not pathlib.PurePosixPath(relative).is_absolute() and '..' not in pathlib.PurePosixPath(relative).parts,'Unsafe relative path')
 p=root/relative;require(p.resolve()==p,'Symlinked path refused');return p
def regular_pinned_input(path):
 require(path.is_file() and not path.is_symlink() and stat.S_ISREG(path.stat().st_mode),'Missing/nonregular pinned review file: '+str(path))
def sealed(path):
 require(path.is_file() and not path.is_symlink() and stat.S_ISREG(path.stat().st_mode) and stat.S_IMODE(path.stat().st_mode)==0o444,'Missing/nonsealed file: '+str(path))
def native_identity(path):
 raw=path.read_bytes();return dict(bytes=len(raw),sha256=digest(raw),git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())
def fsync_dir(path):
 fd=os.open(path,os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
def private_directory(path):
 missing=[];p=path
 while not p.exists():missing.append(p);p=p.parent
 require(p.is_dir() and not p.is_symlink(),'Unsafe private directory parent')
 for q in reversed(missing):q.mkdir(mode=0o700);fsync_dir(q);fsync_dir(q.parent)
 require(path.is_dir() and not path.is_symlink(),'Unsafe private directory')
def durable_json(path,value,readonly=False):
 require(path.parent.is_dir() and not path.parent.is_symlink(),'Output parent missing/unsafe')
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:
  data=encoded(value);view=memoryview(data)
  while view:
   n=os.write(fd,view);require(n>0,'Zero durable write');view=view[n:]
  if readonly:os.fchmod(fd,0o444)
  os.fsync(fd)
 finally:os.close(fd)
 fsync_dir(path.parent)
 return path

def load_context(base):
 """No network/native action. Requires actual PR204 ready90 acceptance, not a draft."""
 base=pathlib.Path(base).resolve();gp=base/'ROOT_PUBLICATION_GATE_01.json';sealed(gp);g=read(gp)
 require(g.get('PR')==PR and g.get('problem_id')==PROBLEM,'Wrong gate PR/problem')
 require(g.get('publication_ready_gate_accepted') is True and g.get('whole_package_review_loop_complete') is True and g.get('historical_priority_established') is False,'Root final gate not accepted')
 events=g.get('whole_package_review_events');require(isinstance(events,list) and len(events)>=2,'Two fresh whole-package reviews required')
 require(len({e['directory'] for e in events})==len(events),'Review events are not distinct')
 require(len({e['review_number'] for e in events})==len(events) and len({e['Root_acceptance_file'] for e in events})==len(events),'Review acceptance events are not distinct')
 for e in events:
  require(isinstance(e['safe_files'],dict) and e['report_file'] in e['safe_files'],'Actual fresh whole-review report missing')
  review_dir=child(base,e['directory'])
  for rel,wanted in e['safe_files'].items():
   p=child(review_dir,rel);regular_pinned_input(p);require(pin(p)==wanted,'Whole-review artifact changed')
  accepted=child(base,e['Root_acceptance_file']);regular_pinned_input(accepted);require(pin(accepted)==e['Root_acceptance_pin'],'Review Root acceptance changed')
  prior_seal=child(base,e['reviewed_package'])/'PACKAGE_SEAL.json';sealed(prior_seal);require(pin(prior_seal)==e['reviewed_package_seal'],'Reviewed package seal changed')
 require(events[-1]['verdict']=='CLEANPASS' and events[-1]['reviewed_package']==g['package'] and events[-1]['reviewed_package_seal']==g['package_seal'],'Last CLEANPASS does not bind exact final package')
 package=child(base,g['package']);safe=g['package_safe_files'];require(isinstance(safe,dict) and safe.get('PACKAGE_SEAL.json')==g['package_seal'],'Final seal missing from safe files')
 actual=[]
 for p in package.rglob('*'):
  require(not p.is_symlink(),'Package symlink refused')
  if p.is_file():actual.append(p.relative_to(package).as_posix())
 require(set(actual)==set(safe),'Package file set differs from final gate')
 for rel,wanted in safe.items():
  p=child(package,rel);sealed(p);require(pin(p)==wanted,'Package file changed: '+rel)
 require(set(g['intended_upload_files'])==UPLOADS,'Exactly the three authorized upload names required')
 for name,wanted in g['intended_upload_files'].items():require(pin(package/name)==wanted,'Intended upload changed')
 manifest=package/'zenodo-deposit.json';m=read(manifest)
 require(m.get('metadata')==g['metadata'] and set(m)=={'metadata','files'},'Manifest metadata differs from final gate')
 require(len(m['files'])==3 and all(set(x)=={'path'} for x in m['files']) and {x['path'] for x in m['files']}==UPLOADS,'Manifest upload list differs')
 creators=g['metadata'].get('creators',[])
 require(any(x.get('name')=='Kriebel, Alec' and x.get('orcid')=='0009-0001-9320-500X' for x in creators),'Alec ORCID metadata missing')
 rp=base/'ROOT_ACTUAL_READY_CHECKPOINT.json';sealed(rp);r=read(rp)
 require(r.get('PR')==PR and r.get('phase')=='ready' and r.get('Root_recorded_only_after_actual_full_scope_acceptance') is True,'Actual PR204 ready pointer missing')
 checkpoint=child(base,r['directory']);ap=checkpoint/'ACCEPTANCE.json';sealed(ap);ac=read(ap)
 require(pin(ap)==r['acceptance_pin'] and ac.get('PR')==PR and ac.get('case_percent')==90,'Ready90 acceptance identity mismatch')
 for field in ['accepted','every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','QUEUE_native_original_PR_unchanged','mathematical_clearance','source_contract_clearance','priority_clearance','bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','publication_ready']:
  require(ac.get(field) is True,'Incomplete actual full-scope acceptance: '+field)
 require(ac.get('historical_firstness_independence_established') is False,'Historical-priority qualification changed')
 require(ac['checkpoint_commit']==r['checkpoint_commit'] and ac['main_observed']==r['main_observed'],'Actual ready commit/MAIN mismatch')
 mp=checkpoint/'ACCEPTANCE_CURRENT_SELECTED_MAP.json';sealed(mp);require(pin(mp)==ac['actual_current_map_file'],'Accepted map file changed');mapped=read(mp);selected=mapped['selected_files']
 map_digest=digest(json.dumps(selected,sort_keys=True,separators=(',',':')).encode())
 require(len(selected)==ac['selected_files'] and map_digest==mapped['selected_map_sha256']==ac['actual_current_selected_map_sha256'],'Accepted selected map mismatch')
 required={PREFIX+'ROOT_PUBLICATION_GATE_01.json':gp}
 required.update({PREFIX+g['package']+'/'+rel:package/rel for rel in safe})
 for key,p in required.items():require(selected.get(key)==native_identity(p),'Actual ready map does not bind exact gate/package: '+key)
 return dict(base=base,gate_path=gp,gate=g,package=package,manifest=manifest,gate_pin=pin(gp),ready_pointer_pin=pin(rp),ready_acceptance_pin=pin(ap),checkpoint_commit=r['checkpoint_commit'],package_seal=g['package_seal'])

def context_pin(context):
 return {k:context[k] for k in ['gate_pin','ready_pointer_pin','ready_acceptance_pin','checkpoint_commit','package_seal']}|{'package':context['gate']['package'],'manifest_pin':pin(context['manifest'])}
def same_context(base,wanted):
 c=load_context(base);require(context_pin(c)==wanted,'Gate/ready/package changed during operation');return c
def publication_receipt(context):
 p=context['base']/'ROOT_PUBLICATION_RECEIPT.json';sealed(p);r=read(p);g=context['gate']
 for key in ['actual_publication_verified','metadata_exact_verified','all_three_public_download_SHA256_verified']:require(r.get(key) is True,'Publication not actually verified: '+key)
 require(r.get('PR')==PR and r.get('state')=='published' and r.get('gate_sha256')==context['gate_pin']['sha256'] and r.get('package')==g['package'],'Publication not bound to exact gate/package')
 require(r.get('metadata_normalizations')==[] and len(r.get('verified_public_download_names',[]))==3 and set(r.get('verified_public_download_names',[]))==UPLOADS,'Publication verification incomplete')
 require(r.get('doi_resolution',{}).get('http_status')==200 and r['doi_resolution'].get('status')=='resolved','Actual DOI resolution not verified')
 require(type(r.get('id')) is int and r['id']>0 and r.get('doi')=='10.5281/zenodo.'+str(r['id']) and r.get('doi_url')=='https://doi.org/'+r['doi'],'Missing actual assigned DOI/record ID')
 require(r.get('record_url')=='https://zenodo.org/records/'+str(r['id']),'Publication record URL differs')
 files=r.get('files',[]);require(len(files)==3 and {x['name']:{'bytes':x['size'],'sha256':x['sha256']} for x in files}==g['intended_upload_files'],'Publication files differ from gate')
 return p,r
