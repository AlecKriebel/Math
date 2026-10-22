from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys
sys.dont_write_bytecode=True
Q=Path(__file__).resolve().parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(rel,d):(Q/rel).write_text(json.dumps(d,indent=2)+'\n')
assert not (Q/'OUTPUT_MANIFEST.json').exists(),'Do not rewrite an existing review seal'
inputs=json.loads((Q/'INPUT_MANIFEST.json').read_text())['files'];changed=[]
for v in inputs:
 b=(Q/v['path']).read_bytes();assert len(b)==v['bytes'] and sha(b)==v['sha256']
 p=Path(v['source'])
 if not p.exists() or sha(p.read_bytes())!=v['sha256']:changed.append(v['source'])
allowed={str(Q.parent.parent/n) for n in ['STATE.json','rest_inventory.json','dispositions.jsonl']};assert set(changed)<=allowed,changed
save('final_input_recheck.json',dict(at=now(),captures=len(inputs),current_canonical_sources_changed_since_capture=changed,note='Mutablecursor/inventory/journalmayadvance; allcapturedimmutablereceipts/priorreviewsunchanged.'))
if changed:
 p=Q/'REPORT.md';s=p.read_text();s=s.replace('No canonical\ninput captured in this review had changed at its final recheck.','Only the expected mutable cursor/inventory/journal inputs advanced after capture;\nall captured immutable receipts and prior reviews remain unchanged.');p.write_text(s)
outputs=[]
for name,flags in [('normal',[]),('optimized',['-O'])]:
 x=subprocess.run([sys.executable,'-B',*flags,str(Q/'verify_review_evidence.py')],capture_output=True,check=True);(Q/f'verification_{name}.stdout').write_bytes(x.stdout);(Q/f'verification_{name}.stderr').write_bytes(x.stderr);outputs.append(dict(mode=name,result=json.loads(x.stdout),stdout_sha256=sha(x.stdout),stderr_sha256=sha(x.stderr)))
assert outputs[0]['result']==outputs[1]['result']
save('verification_replay.json',dict(at=now(),runs=outputs,scope='Read-onlysaved-evidenceverification; nofreshproviderorproofcertification.'))
log=json.loads((Q/'RESEARCH_LOG.json').read_text());log.append(dict(at=now(),completion_estimate_percent=100,event='Bounded46PRreviewcomplete; scopedPASS,842? no accountingcontrols claimed. Saved-evidence normal/Overificationpasses; immutablecapturessealed.'))
log[-1]['event']='Bounded46PRreviewcomplete; scopedPASS. Saved-evidence normal/Overificationpasses; immutablecapturessealed. No final-sweepcertification.'
save('RESEARCH_LOG.json',log)
files=[];symlinks=[]
for p in sorted(Q.rglob('*')):
 if p.is_symlink():symlinks.append(dict(path=str(p.relative_to(Q)),target=os.readlink(p),resolved_target=str(p.resolve())))
 elif p.is_file():
  b=p.read_bytes();files.append(dict(path=str(p.relative_to(Q)),bytes=len(b),sha256=sha(b)))
m=dict(at=now(),files=files,symlinks=symlinks,note='Everyregularreviewfileexceptthismanifestanditsseparatedigest. Rawledger/account/sourcefulltexts/publicbinariesremainlocal; sanitizedauthoredprojectiononly. No signature/authenticity/proof/priorityclaim.')
save('OUTPUT_MANIFEST.json',m);digest=sha((Q/'OUTPUT_MANIFEST.json').read_bytes());(Q/'OUTPUT_MANIFEST.sha256').write_text(digest+'\n')
for v in files:
 b=(Q/v['path']).read_bytes();assert len(b)==v['bytes'] and sha(b)==v['sha256']
print(json.dumps(dict(verdict='SCOPED_PASS',files=len(files),symlinks=len(symlinks),manifest_sha256=digest)))
