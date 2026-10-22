"""Derive the already checked guard harness and add current-stage controls."""
from pathlib import Path
F=Path(__file__).resolve().parent;A=F.parents[1]
text=(A/'repairs/case_alias01/controls.py').read_text()
text=text.replace('Actual current physical-alias and custody controls; no compiler or service.','Actual post-whole03 terminal/physical-alias/custody controls; no compiler or service.')
text=text.replace('import datetime,hashlib,io,json,os,shutil,subprocess,sys,tempfile,zipfile','import datetime,hashlib,io,json,os,shutil,subprocess,sys,tempfile,zipfile\nfrom contextlib import contextmanager')
anchor='def main():\n'
support='''cleanup=[]
def scratch_pins(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  if p.is_symlink():rows.append({'path':str(p.relative_to(F/'scratch')),'symlink_target':os.readlink(p)})
  elif p.is_file():
   b=p.read_bytes();rows.append({'path':str(p.relative_to(F/'scratch')),'bytes':len(b),'sha256':sha(b)})
 return rows
def freeze_cleanup(root,label):
 rows=scratch_pins(root)
 for row in rows:
  p=F/'scratch'/row['path']
  if 'symlink_target' in row:need(p.is_symlink() and os.readlink(p)==row['symlink_target'],'scratch link changed')
  else:
   b=p.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'scratch changed before cleanup')
 cleanup.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(root.relative_to(F)),'label':label,'rechecked_before_deletion':True,'files':rows})
 dump(F/'OWN_SCRATCH_CLEANUP_LEDGER.json',{'scope':'Only this effort owned scratch; each listed tree is individually hashed/rechecked immediately before its controlled cleanup. Canonical/other-worker inputs never removed.','events':cleanup})
@contextmanager
def owned_temp():
 base=F/'scratch';base.mkdir(exist_ok=True)
 temp=Path(tempfile.mkdtemp(prefix='terminal-controls-',dir=base))
 try:yield str(temp)
 finally:
  freeze_cleanup(temp,'final owned scratch cleanup');shutil.rmtree(temp)
def remove_tree(path):
 freeze_cleanup(path,'owned derivative subtree cleanup');shutil.rmtree(path)
'''
text=text.replace(anchor,support+anchor)
text=text.replace("with tempfile.TemporaryDirectory(prefix='pr1085-case-alias01-',dir='/private/tmp') as td:","with owned_temp() as td:")
text=text.replace("  def fresh(full=False):\n", "  def fresh(full=False):\n   freeze_cleanup(root,'controlled disposable-kit reset')\n")
text=text.replace("and default['new_complete_whole03_required'] and not default['new_complete_whole03_completed']","and not default['new_complete_whole03_required'] and default['new_complete_whole03_completed'] and default['new_whole_reviews']==3 and default['root_terminal_integrity_adoption_required'] and not default['root_terminal_integrity_adopted']")
text=text.replace("shutil.rmtree(outdir)","remove_tree(outdir)").replace("shutil.rmtree(compiler)","remove_tree(compiler)").replace("shutil.rmtree(unicode_parent)","remove_tree(unicode_parent)")
text=text.replace("'scope':'Actual current-repair commands", "'scope':'Actual final-byte post-whole03 commands")
anchor="   for n in ['PAYLOAD_MEMBERS.txt','SUPPORT_MANIFEST.json']:\n"
extra='''   current_name='CURRENT_TERMINAL_ACCOUNTING_20261016.json'
   current_faults=[('schema',True,'current terminal schema'),('pr',1086,'current terminal identity'),('problem_id',True,'current terminal identity'),('status','READY','current terminal stage'),('whole_reviews_completed',2,'current terminal review count'),('minimum_whole_reviews',3,'current terminal review count'),('latest_complete_whole_review',2,'current terminal review count'),('latest_actionable_P0_P1_P2_P3',1,'current terminal review count'),('case_alias_repair_root_adopted',False,'current terminal required adoption/history'),('latest_complete_whole_review_root_adopted',False,'current terminal required adoption/history'),('new_complete_whole03_completed',False,'current terminal required adoption/history'),('root_terminal_integrity_adoption_required',False,'current terminal required adoption/history'),('historical_STATUS_TERMINAL_ACCOUNTING_CASE_REPAIR_preserved',False,'current terminal required adoption/history'),('new_complete_whole03_required',True,'current terminal forbidden promotion/stale hold'),('further_complete_whole_review_currently_required',True,'current terminal forbidden promotion/stale hold'),('root_terminal_integrity_adopted',True,'current terminal forbidden promotion/stale hold'),('publication_ready',True,'current terminal forbidden promotion/stale hold'),('all_actionable_issues_resolved',True,'current terminal forbidden promotion/stale hold'),('issues_resolved',True,'current terminal forbidden promotion/stale hold'),('published',True,'current terminal forbidden promotion/stale hold'),('human_peer_review',True,'current terminal forbidden promotion/stale hold'),('formal_proof_certificate',True,'current terminal forbidden promotion/stale hold'),('services_hold','none','current terminal ordered hold'),('priority','CLEARED','current terminal historical scope'),('novelty','NEW','current terminal historical scope'),('worldwide_open_status','OPEN','current terminal historical scope'),('independent_discovery','YES','current terminal historical scope'),('paper_pdf_sha256','0'*64,'current terminal unchanged paper'),('latest_review_prefix','elsewhere/','current terminal exact evidence interfaces')]
   for key,value,message in current_faults:
    fresh();change(current_name,key,value)
    p=run(root,prefix+['verify_package.py'],label+' coherent current fault '+key,False,message)
    semantic.append({'mode':label,'case':'current '+key,'reached_guard':message,'returncode':p.returncode,'outer_manifest_refreshed':True})
   current_prefix='evidence/terminal_after_whole03/';review_prefix=current_prefix+'reviews/package_03/'
   cmap='CURRENT_TERMINAL_COPY_MAP_20261016.json'
   def coherent_evidence(name,key,value,kind):
    p=root/name;o=json.loads(p.read_text());o[key]=value;dump(p,o)
    if kind=='review_output':
     op=root/(review_prefix+'OUTPUT_PINS.json');oo=json.loads(op.read_text());r=next(r for r in oo['files'] if r['path']==Path(name).name);b=p.read_bytes();r['bytes']=len(b);r['sha256']=sha(b);dump(op,oo)
     sp=root/(review_prefix+'SEAL.json');so=json.loads(sp.read_text());so['output_pins_bytes']=op.stat().st_size;so['output_pins_sha256']=sha(op.read_bytes())
     if Path(name).name=='VERDICT.json':so['verdict_sha256']=sha(p.read_bytes())
     if Path(name).name=='INDEPENDENT_DERIVATION.md':raise ValueError('use JSON only')
     dump(sp,so)
     ap=root/(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json');ao=json.loads(ap.read_text());ao['output_pins_sha256']=so['output_pins_sha256'];dump(ap,ao)
    mp=root/cmap;mo=json.loads(mp.read_text())
    for r in mo['files']:
     b=(root/r['copy']).read_bytes();r['bytes']=len(b);r['sha256']=sha(b)
    dump(mp,mo);repin()
   evidence_faults=[(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','whole_reviews_completed',2,'root','whole03 root adoption semantics'),(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','actionable_P0_P1_P2_P3',1,'root','whole03 root adoption semantics'),(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','terminal_administrative_reconciliation_and_root_final_integrity_required',False,'root','whole03 root adoption semantics'),(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','published',True,'root','whole03 evidence no readiness/service promotion'),(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','services_held_after_pr',1033,'root','whole03 evidence no readiness/service promotion'),(current_prefix+'ROOT_CASE_ALIAS_REPAIR_REVIEW_01.json','status','CLEARED','root','captured root case repair adoption'),(review_prefix+'VERDICT.json','severity_counts',{'P0':0,'P1':0,'P2':0,'P3':1},'review_output','whole03 zero finding verdict semantics'),(review_prefix+'VERDICT.json','human_peer_review',True,'review_output','whole03 evidence no refereeing promotion'),(review_prefix+'VERDICT.json','novelty','NEW','review_output','whole03 evidence historical scope'),(review_prefix+'VERDICT.json','publication_ready',True,'review_output','whole03 evidence no readiness/service promotion'),(review_prefix+'DERIVATION_FREEZE.json','before_prior_review_reasoning',False,'review_output','whole03 frozen independent derivation')]
   for name,key,value,kind,message in evidence_faults:
    fresh();coherent_evidence(name,key,value,kind)
    p=run(root,prefix+['verify_package.py'],label+' coherent current evidence '+Path(name).name+' '+key,False,message)
    semantic.append({'mode':label,'case':name+' '+key,'reached_guard':message,'returncode':p.returncode,'outer_manifest_and_copy_map_refreshed':True,'review_output_manifest_seal_and_root_binding_refreshed':kind=='review_output'})
   for kind in ['membership','bytes','before_locator']:
    fresh();p=root/cmap;o=json.loads(p.read_text())
    if kind=='membership':o['files'].pop();message='current terminal exact copy membership'
    elif kind=='bytes':o['files'][0]['sha256']='0'*64;message='current terminal exact copied bytes'
    else:o['files'][-1]['source_snapshot_relative_audit']='successor/UPLOAD_BINDINGS.json';message='current terminal exact before locator'
    dump(p,o);repin();run(root,prefix+['verify_package.py'],label+' current map fault '+kind,False,message)
   fresh();(root/current_name).write_text('{"schema":1,"schema":1}\\n');repin();run(root,prefix+['verify_package.py'],label+' duplicate current JSON',False,'duplicate JSON key')
'''
if anchor not in text:raise ValueError('control insertion anchor')
text=text.replace(anchor,extra+anchor)
# Pin the actual current ZIP creation result before running controls.
text=text.replace(" physical=[];aliases=[];semantic=[];mode_results=[]", " physical=[];aliases=[];semantic=[];mode_results=[]")
text=text.replace("dump(F/'CONTROL_SUMMARY.json',", "dump(F/'CONTROL_SUMMARY.json',")
(F/'controls.py').write_text(text)
print('Current harness authored; all actual receipts will be retained.')
